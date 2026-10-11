import logging
import math
import os
import platform
import sys
from contextlib import contextmanager, nullcontext, redirect_stderr, redirect_stdout, suppress
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

# 由于需要打猴子补丁，因此请勿全局导入任何依赖 gettext 的模块。

_logger = logging.getLogger(__name__)


def setup_l10n():
    import gettext as gettextlib

    from vcf_generator_lite.utils.i18n.zipapp_gettext import translation
    from vcf_generator_lite.utils.resources import resources_traversable

    app_translation = translation(domain="vcf-generator-lite", localedir=resources_traversable.joinpath("locales"))

    gettextlib.gettext = app_translation.gettext
    gettextlib.ngettext = app_translation.ngettext
    gettextlib.pgettext = app_translation.pgettext
    gettextlib.npgettext = app_translation.npgettext


def setup_logging(quiet: int, verbose: int):
    from gettext import pgettext

    try:
        import colorlog
    except ImportError:
        colorlog = None

    handler = logging.StreamHandler()
    handler.setStream(sys.stdout)
    log_format = "{asctime} {levelname:8} {name:50.50} {message}"
    if colorlog:
        handler.setFormatter(colorlog.ColoredFormatter("{log_color}" + log_format, style="{"))
    else:
        handler.setFormatter(logging.Formatter(log_format, style="{"))

    if quiet >= 2:
        level = logging.ERROR
    elif verbose == 1:
        level = logging.INFO
    elif verbose >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, handlers=[handler])

    if verbose >= 1 and not colorlog:
        print(
            pgettext(
                "startup.colorlog_not_available_warning",
                "⚠️WARNING: Colorlog is not available, using plain text instead. "
                "Please install colorlog to enable colored logging.",
            ),
            file=sys.stderr,
        )


def fix_home_env():
    """Fix HOME environment variable on Windows if it's not set."""
    if sys.platform == "win32":
        with suppress(RuntimeError):
            os.environ["HOME"] = str(Path.home())


def setup_excepthook():

    def excepthook(_type: type[BaseException], value: BaseException, _tb: "TracebackType | None"):
        from vcf_generator_lite.ui.windows.message_boxes.unexpected_error import show_unexpected_error_dialog

        _logger.error("Unexpected error: %s", value, exc_info=value)
        show_unexpected_error_dialog(value)

    sys.excepthook = excepthook


@contextmanager
def stdio_msgbox_if_needed(app_name: str):
    from tkinter.messagebox import OK, Message

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
                Message(
                    title=app_name,
                    message=err_msg or out_msg,
                    icon="error" if err_msg else "info",
                    type=OK,
                ).show()


def require_python():
    from vcf_generator_lite.constants import PYTHON_VERSION_MINIMUM

    if sys.version_info < PYTHON_VERSION_MINIMUM:
        print(
            f"⚠️ERROR: Python {platform.python_version()} is not supported. "
            f"Please upgrade to Python {PYTHON_VERSION_MINIMUM[0]}.{PYTHON_VERSION_MINIMUM[1]} or later.",
            file=sys.stderr,
        )
        sys.exit(1)


def require_tkinter():
    from gettext import pgettext

    from vcf_generator_lite.constants import TK_VERSION_MINIMUM

    try:
        from tkinter import TkVersion

        # 由于 TkVersion 是 float 类型，可能会出现次版本错误的情况。
        # 幸亏 Tcl/Tk 8 的次要版本截至到 6，未超过 10，所以这里可以安全地判断。
        minor_version, major_version = math.modf(TkVersion)
        if (int(major_version), round(minor_version * 10)) < TK_VERSION_MINIMUM:
            print(
                pgettext(
                    "startup.tcltk_unsupported_error",
                    "⚠️ERROR: Tcl/Tk {current_version} is not supported. "
                    "Please upgrade to Tcl/Tk {minimum_version} or later.",
                ).format(
                    current_version=TkVersion,
                    minimum_version=f"{TK_VERSION_MINIMUM[0]}.{TK_VERSION_MINIMUM[1]}",
                ),
                file=sys.stderr,
            )
            sys.exit(1)
    except ImportError:
        print(
            pgettext(
                "startup.tcltk_not_available_error",
                "⚠️ERROR: Tcl/Tk is not available. Please install Tcl/Tk.",
            ),
            file=sys.stderr,
        )
        sys.exit(1)


def launch(*, quiet: int, verbose: int):
    from vcf_generator_lite.ui.windows.main_window import VCFGeneratorLiteApp

    setup_logging(quiet=quiet, verbose=verbose)
    fix_home_env()

    app = VCFGeneratorLiteApp()
    app.mainloop()
