import logging
import os
import sys
import tkinter.messagebox
import traceback
from contextlib import contextmanager, nullcontext, redirect_stderr, redirect_stdout, suppress
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from tkinter.messagebox import Message, showerror
from types import TracebackType

_logger = logging.getLogger(__name__)


def setup_l10n():
    import gettext as gettextlib

    from vcf_generator_lite.utils import resources
    from vcf_generator_lite.utils.i18n.zipapp_gettext import translation

    app_translation = translation(domain="vcf-generator-lite", localedir=resources.traversable.joinpath("locales"))

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
    from vcf_generator_lite.utils.environment import is_windows

    if is_windows:
        with suppress(RuntimeError):
            os.environ["HOME"] = str(Path.home())


def setup_excepthook(app_name: str):
    prev_excepthook = sys.excepthook

    def excepthook(type_: type[BaseException], value: BaseException, tb: TracebackType | None):
        from gettext import pgettext

        prev_excepthook(type_, value, tb)

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            suffix=".log",
            prefix="vcf-generator-lite-error-",
        ) as f:
            traceback.print_exception(type_, value, tb, file=f)
            log_path = f.name
        showerror(
            title=app_name,
            message=pgettext("startup.unexpected_error.message", "An unexpected error occurred."),
            detail=pgettext(
                "startup.unexpected_error.detail",
                "Error: {error}\n\nError details saved to:\n{path}\n\nPlease send this file to the developer.",
            ).format(path=log_path, error=str(value)),
        )

    sys.excepthook = excepthook


@contextmanager
def redirect_stdio_to_messagebox_if_needed(app_name: str):
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
                    type=tkinter.messagebox.OK,
                ).show()


def launch(*, quiet: int, verbose: int):
    from gettext import pgettext

    from vcf_generator_lite.constants import URL_REPOSITORY
    from vcf_generator_lite.ui.windows.main_window import VCFGeneratorLiteApp

    setup_logging(quiet=quiet, verbose=verbose)
    fix_home_env()
    if not quiet:
        print(pgettext("startup.source_tip", "💡Tip: Source code is hosted at {url}").format(url=URL_REPOSITORY))

    app = VCFGeneratorLiteApp()
    app.mainloop()
