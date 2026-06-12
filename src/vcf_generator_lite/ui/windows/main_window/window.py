import dataclasses
import logging
import signal
from gettext import pgettext
from itertools import chain
from pathlib import Path
from tkinter import Event, filedialog
from types import FrameType
from typing import TYPE_CHECKING, NamedTuple, TextIO, override

from vcf_generator_lite.core.phone_detector_loader import load_country_phone_detectors
from vcf_generator_lite.core.vcf_generator import GenerateResult, InvalidItem, PhoneRule, VCFGeneratorTask
from vcf_generator_lite.ui.app_text import app_name
from vcf_generator_lite.ui.windows.base_window import EnhancedTk
from vcf_generator_lite.ui.windows.base_window.constants import EVENT_EXIT
from vcf_generator_lite.ui.windows.main_window.layout import MainLayout
from vcf_generator_lite.ui.windows.main_window.menu_bar import MainMenuBar
from vcf_generator_lite.ui.windows.main_window.message_boxes import (
    show_generation_success_dialog,
    show_save_file_os_error_dialog,
    show_save_file_permission_denied_dialog,
)
from vcf_generator_lite.ui.windows.main_window.states import GenerationState
from vcf_generator_lite.ui.windows.message_boxes.about import show_about_message_box
from vcf_generator_lite.ui.windows.message_boxes.unexpected_error import show_unexpected_error_dialog
from vcf_generator_lite.utils.i18n.zipapp_gettext import get_default_locales, get_locale_territories
from vcf_generator_lite.utils.text import clean_quotes
from vcf_generator_lite.utils.tkinter.text import search_line, select_text

if TYPE_CHECKING:
    from vcf_generator_lite.models.phone_detector import PhoneDetector

_logger = logging.getLogger(__name__)


class Generation(NamedTuple):
    generator: VCFGeneratorTask
    file: Path
    file_io: TextIO


class VCFGeneratorLiteApp(EnhancedTk, MainMenuBar.Listener, MainLayout.Listener):
    def __init__(self):
        self.is_exiting = False
        self.current_generation: Generation | None = None
        self.save_vcf_file_name: str = pgettext("window_save_vcf.default_file_name", "My Contacts.vcf")
        self.phone_detectors_dict: dict[str, PhoneDetector] = load_country_phone_detectors()
        self.phone_detectors_list: list[PhoneDetector] = sorted(
            self.phone_detectors_dict.values(),
            key=lambda phone_detector: phone_detector.id,
        )
        locale_territories = set(get_locale_territories(get_default_locales()))
        self.phone_detectors_ids = set(self.phone_detectors_dict.keys())
        self.selected_phone_detectors_ids: set[str] = {
            phone_detector.id
            for phone_detector in self.phone_detectors_list
            if phone_detector.locale_territories & locale_territories
        }

        if not self.selected_phone_detectors_ids and self.phone_detectors_list:
            self.selected_phone_detectors_ids.add(self.phone_detectors_list[0].id)

        super().__init__(className="VCFGeneratorLite")

    @override
    def _configure_ui_withdraw(self):
        super()._configure_ui_withdraw()
        self.title(app_name())
        self.wm_minsize_pt(300, 300)
        self.wm_size_pt(450, 450)
        self.layout = MainLayout(self, self)
        self.menu_bar = MainMenuBar(self, self.phone_detectors_list, self)
        self.menu_bar.set_phone_detectors_selection(
            self.is_all_phone_detectors_selected(),
            {id_: self.is_phone_detector_selected(id_) for id_ in self.phone_detectors_ids},
        )
        self.configure(menu=self.menu_bar)

        self.bind("<Control-Lock-G>", self.on_generate)
        self.bind("<Control-g>", self.on_generate)
        self.bind("<Return>", self.on_return)
        self.bind(EVENT_EXIT, self.on_exit)

        signal.signal(signal.SIGINT, self._handle_sigint)

    @override
    def _configure_ui(self):
        super()._configure_ui()
        self.layout.content_text.focus_set()

    @override
    def on_about(self):
        show_about_message_box(self)

    @override
    def on_clean_quotes(self):
        self._clean_quotes()

    @override
    def on_generate(self, _event: Event | None = None):
        self._generate_file()

    @override
    def on_stop_generation(self):
        self._stop_generation()

    @override
    def on_generate_or_stop(self, _event: Event | None = None):
        if self.current_generation:
            self.on_stop_generation()
        else:
            self.on_generate()

    @override
    def on_exit(self, _event: Event | None = None):
        self.is_exiting = True
        if self.current_generation:
            self._stop_generation()
        else:
            self.destroy()

    def on_return(self, event: Event):
        if str(self.layout.content_text.frame).startswith(str(event.widget)):
            return
        self.layout.generate_or_stop_button.invoke()

    @override
    def on_toggle_phone_detector(self, detector_id: str):
        new_state = not self.is_phone_detector_selected(detector_id)
        if new_state:
            self.selected_phone_detectors_ids.add(detector_id)
        else:
            self.selected_phone_detectors_ids.discard(detector_id)
        self.menu_bar.set_phone_detectors_selection(self.is_all_phone_detectors_selected(), {detector_id: new_state})

    @override
    def on_toggle_all_phone_detectors(self):
        new_state = not self.is_all_phone_detectors_selected()
        if new_state:
            self.selected_phone_detectors_ids.update(self.phone_detectors_ids)
        else:
            self.selected_phone_detectors_ids.clear()
        self.menu_bar.set_phone_detectors_selection(new_state, dict.fromkeys(self.phone_detectors_ids, new_state))

    def _generate_file(self):
        if self.current_generation:
            return
        pick_result = self._pick_and_open_file()
        if not pick_result:
            return
        file, file_io = pick_result
        input_text = self.layout.get_text_content()
        selected_rules = self._get_selected_rules()
        self._prepare_ui_for_generation()
        self._start_generation_task(input_text, selected_rules, file, file_io)

    def _pick_and_open_file(self) -> None | tuple[Path, TextIO]:
        file_path_str = filedialog.asksaveasfilename(
            title=pgettext("window_save_vcf.title", "Select File Save Location"),
            parent=self,
            initialfile=self.save_vcf_file_name,
            filetypes=[(pgettext("window_save_vcf.label_type_vcf", "vCard File (*.vcf)"), ".vcf")],
            defaultextension=".vcf",
        )
        if not file_path_str:
            return None
        generation_file = Path(file_path_str)
        self.save_vcf_file_name = generation_file.name
        try:
            file_io = generation_file.open("w", encoding="utf-8", newline="\r\n")
        except PermissionError:
            show_save_file_permission_denied_dialog(self)
            return None
        except OSError as e:
            show_save_file_os_error_dialog(self, e)
            return None
        return generation_file, file_io

    def _stop_generation(self):
        generation = self.current_generation
        if generation is None or generation.generator.is_stopping or not generation.generator.is_alive():
            return

        self.layout.set_generating(GenerationState.STOPPING)
        generation.generator.stop()

    def _prepare_ui_for_generation(self):
        self.layout.content_text.edit_modified(False)
        self.layout.set_progress(progress=0)
        self.layout.set_progress_determinate(False)
        self.layout.set_generating(GenerationState.GENERATING)
        self.menu_bar.set_generating_state(GenerationState.GENERATING)
        self.update()

    def _start_generation_task(self, input_text: str, rules: list[PhoneRule], file: Path, file_io: TextIO):
        generator = VCFGeneratorTask(
            input_text=input_text,
            output_io=file_io,
            progress_listener=self.on_generation_update_progress,
            result_listener=self.on_generation_result,
            phone_rules=rules,
        )
        self.current_generation = Generation(generator=generator, file=file, file_io=file_io)
        generator.start()

    def _get_selected_rules(self) -> list[PhoneRule]:
        return list(
            chain.from_iterable(
                self.phone_detectors_dict[detector_id].rules for detector_id in self.selected_phone_detectors_ids
            )
        )

    def _clean_quotes(self):
        self.layout.set_text_content(clean_quotes(self.layout.get_text_content()))

    def _show_generation_done_dialog(self, display_path: str, generate_result: GenerateResult):
        if generate_result.exception:
            if isinstance(generate_result.exception, OSError):
                show_save_file_os_error_dialog(self, generate_result.exception)
            else:
                show_unexpected_error_dialog(generate_result.exception)
        elif len(generate_result.invalid_items) > 0:
            self._show_generation_invalid_dialog(display_path, generate_result.invalid_items)
        else:
            show_generation_success_dialog(self, display_path, generate_result)

    def _show_generation_invalid_dialog(self, display_path: str, invalid_items: list[InvalidItem]):
        from vcf_generator_lite.ui.windows.invalid_items_dialog import InvalidItemsDialog

        InvalidItemsDialog(
            self,
            display_path=display_path,
            invalid_items=invalid_items,
            line_enter_listener=self._on_select_invalid_line,
        )

    def on_generation_update_progress(self, progress: float, determinate: bool):
        generation = self._require_generation()
        if generation.generator.is_stopping:
            return

        self.layout.set_progress_determinate(determinate)
        if determinate:
            self.layout.set_progress(progress)

    def on_generation_done(self, result: GenerateResult):
        generation = self._require_generation()
        self.current_generation = None
        self.layout.set_generating(GenerationState.IDLE)
        self.menu_bar.set_generating_state(GenerationState.IDLE)
        self.update()

        if not self.is_exiting:
            self._show_generation_done_dialog(
                display_path=str(generation.file),
                generate_result=result,
            )
        else:
            self.destroy()

    def on_generation_result(self, result: GenerateResult):
        generation = self._require_generation()
        try:
            generation.file_io.close()
        except OSError as e:
            _logger.exception("Failed to close file after generation: %s", generation.file)
            if result.exception is None:
                result = dataclasses.replace(result, exception=e)

        self.after_idle(self.on_generation_done, result)

    def is_all_phone_detectors_selected(self):
        return (self.selected_phone_detectors_ids & self.phone_detectors_ids) == self.phone_detectors_ids

    def is_phone_detector_selected(self, detector_id: str):
        if detector_id not in self.phone_detectors_dict:
            raise ValueError(f"Unknown phone detector: {detector_id}")
        return detector_id in self.selected_phone_detectors_ids

    def _require_generation(self) -> Generation:
        if not self.current_generation:
            raise RuntimeError("Invoke callback without generating.")
        return self.current_generation

    def _on_select_invalid_line(self, item: InvalidItem):
        actual_line = search_line(self.layout.content_text, item.raw_content, near_row=item.row_position, strip=True)

        if actual_line is not None:
            self.deiconify()
            self.lift()
            self.layout.content_text.focus_set()
            select_text(self.layout.content_text, f"{actual_line}.0", f"{actual_line}.end")

    def _handle_sigint(self, sig_num: int, _frame: FrameType | None):
        if sig_num == signal.SIGINT:
            self.on_exit()
