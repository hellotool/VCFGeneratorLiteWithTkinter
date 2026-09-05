import binascii
import logging
import time
from collections.abc import Callable
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
from contextlib import suppress
from dataclasses import dataclass
from io import StringIO
from threading import Event, RLock, Thread
from typing import IO, override

from vcf_generator_lite.core.contact_parser import parse_contact
from vcf_generator_lite.models.contact import Contact, MissingNumberError
from vcf_generator_lite.models.phone_detector import PhoneRule
from vcf_generator_lite.utils.deque_queue import DequeQueue, ShutDownError

_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InvalidItem:
    row_position: int
    raw_content: str
    exception: BaseException


@dataclass(frozen=True)
class GenerationResult:
    invalid_items: list[InvalidItem]
    exception: BaseException | None
    time_elapsed: float
    saved_count: int


@dataclass(frozen=False)
class _GenerationProgress:
    total: int = 0
    processed: int = 0
    saved_count: int = 0
    determinate: bool = False


def utf8_to_qp(text: str) -> str:
    return binascii.b2a_qp(text.encode("utf-8")).decode("utf-8")


def serialize_to_vcard(contact: Contact):
    items: list[str | None] = [
        "BEGIN:VCARD",
        "VERSION:2.1",
        f"FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{utf8_to_qp(contact.name)}" if contact.name else None,
        f"TEL;CELL:{contact.phone}",
        f"NOTE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{utf8_to_qp(contact.note)}" if contact.note else None,
        "END:VCARD",
    ]
    filtered_items = (item for item in items if item is not None)
    return "\n".join(filtered_items)


class VCFGeneratorTask(Thread):
    """在两个工作线程中并发地解析输入并写入 vCard。

    详情请参考 docs/dev/architecture/core.md
    """

    def __init__(
        self,
        input_io: IO[str] | str,
        output_io: IO[str],
        *,
        phone_rules: list[PhoneRule],
        progress_listener: Callable[[int, int, bool], None] | None = None,
        result_listener: Callable[[GenerationResult], None] | None = None,
        part_delimiter: str | None = None,
    ):
        super().__init__()
        self._progress_listener = progress_listener
        self._result_listener = result_listener
        self._input_io = input_io
        self._output_io = output_io
        self._phone_rules = phone_rules
        self._part_delimiter = part_delimiter

        self._progress = _GenerationProgress()

        self._invalid_items: list[InvalidItem] = []

        self._progress_lock = RLock()
        self._progress_event = Event()

        self.__stopping: bool = False
        self.__all_done: bool = False
        # 使用 deque 会比原生的 queue 性能高
        self._write_queue: DequeQueue[str | None] = DequeQueue(10)
        self.result: GenerationResult | None = None

    @property
    def is_stopping(self) -> bool:
        return self.__stopping

    def stop(self):
        self.__stopping = True
        self._write_queue.shutdown()
        self._progress_event.set()

    @override
    def run(self):
        _logger.info("Starting vcf generate task.")
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="VCFGenerator") as pipeline_executor:
            write_future = pipeline_executor.submit(self._write_output)
            parse_future = pipeline_executor.submit(self._parse_input)
            notify_future = pipeline_executor.submit(self._notify_progress)

            done, _ = wait([parse_future, write_future, notify_future], return_when=FIRST_EXCEPTION)
            self.stop()
        end_time = time.time()
        time_elapsed = end_time - start_time
        _logger.info(
            "Finished vcf generate task, processed %s items, saved %s items, time elapsed: %ss",
            self._progress.processed,
            self._progress.saved_count,
            time_elapsed,
        )

        exception: BaseException | None = None
        for future in done:
            if (future_exception := future.exception()) and not isinstance(future_exception, ShutDownError):
                exception = future_exception
                _logger.exception("An error occurred during VCF generation.", exc_info=exception)

        self.result = result = GenerationResult(
            invalid_items=self._invalid_items,
            exception=exception,
            time_elapsed=time_elapsed,
            saved_count=self._progress.saved_count,
        )
        if self._result_listener:
            try:
                self._result_listener(result)
            except Exception:
                _logger.exception("Result listener callback failed.")

    def _parse_input(self) -> None:
        try:
            if isinstance(self._input_io, str):
                text = self._input_io
                total_lines = (text.count("\n") + (0 if text.endswith("\n") else 1)) if text else 0
                self._update_total(total_lines)
                input_io = StringIO(self._input_io)
            else:
                input_io = self._input_io

            for position, line in enumerate((line.strip() for line in input_io), 1):
                if self.__stopping:
                    break

                if not line:
                    # 当前总数是基于换行计算来的，但空行不计入总数，因此需要减少总数。
                    self._skip_item()
                    continue

                try:
                    contact = parse_contact(
                        contact_text=line,
                        rules=self._phone_rules,
                        delimiter=self._part_delimiter,
                    )
                    vcard = serialize_to_vcard(contact)
                except MissingNumberError as e:
                    _logger.debug("Phone not found at line %s.", position)

                    # list 的 append 方法是原子的，因此不需要加锁
                    # https://docs.python.org/zh-cn/3/library/threadsafety.html#thread-safety-list
                    self._invalid_items.append(
                        InvalidItem(
                            row_position=position,
                            raw_content=line,
                            exception=e.with_traceback(None),
                        )
                    )
                    self._finish_item(success=False)
                else:
                    self._write_queue.put(vcard)
        finally:
            with suppress(ShutDownError):
                self._write_queue.put(None)  # 结束信号

    def _write_output(self):
        try:
            while (item := self._write_queue.get()) is not None:
                try:
                    self._output_io.write(item)
                    self._output_io.write("\n\n")
                except BaseException:
                    self._finish_item(success=False)
                    raise
                else:
                    self._finish_item(success=True)
        finally:
            self.__all_done = True
            self._progress_event.set()
            self._output_io.flush()

    def _notify_progress(self):
        if self._progress_listener is None:
            return
        while not self.__all_done or self._progress_event.is_set():
            self._progress_event.wait()
            self._progress_event.clear()
            processed, total, determinate = self._progress.processed, self._progress.total, self._progress.determinate
            _logger.debug("Notifying progress: processed %s, total %s, determinate %s", processed, total, determinate)
            self._progress_listener(processed, total, determinate)

    def _skip_item(self):
        if not self._progress.determinate:
            return
        with self._progress_lock:
            self._progress.total -= 1
        self._progress_event.set()

    def _finish_item(self, *, success: bool = True):
        with self._progress_lock:
            self._progress.processed += 1
            if success:
                self._progress.saved_count += 1
        self._progress_event.set()

    def _update_total(self, total: int):
        with self._progress_lock:
            self._progress.total = total
            self._progress.determinate = True
        self._progress_event.set()
