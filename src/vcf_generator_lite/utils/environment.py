import os
import sys
from contextlib import contextmanager, nullcontext, redirect_stderr, redirect_stdout, suppress
from io import StringIO
from pathlib import Path

script_path = sys.path[0]

frozen = getattr(sys, "frozen", False)

is_windows = sys.platform == "win32"


def fix_home_env():
    """修复 Windows 下 Tkinter 无法获取 HOME 的问题"""
    if is_windows:
        with suppress(RuntimeError):
            os.environ["HOME"] = str(Path.home())


@contextmanager
def redirect_to_messagebox_if_needed(title: str | None = None):
    with (
        redirect_stderr(StringIO()) if not sys.stderr else nullcontext() as err_io,
        redirect_stdout(StringIO()) if not sys.stdout else nullcontext() as out_io,
    ):
        try:
            yield
        finally:
            err_msg = err_io and err_io.getvalue()
            out_msg = out_io and out_io.getvalue()
            if err_msg or out_msg:
                import tkinter.messagebox

                tkinter.messagebox.Message(
                    title=title,
                    message=err_msg or out_msg,
                    icon="error" if err_msg else "info",
                    type=tkinter.messagebox.OK,
                ).show()
