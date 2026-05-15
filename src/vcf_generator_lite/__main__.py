import logging
import os
import sys
from contextlib import contextmanager, nullcontext, redirect_stderr, redirect_stdout, suppress
from io import StringIO
from pathlib import Path

__all__ = ["main"]

APP_DOMAIN = "vcf-generator-lite"


def setup_l10n():
    import gettext as gettextlib

    from vcf_generator_lite.utils import resources
    from vcf_generator_lite.utils.i18n.zipapp_gettext import translation

    app_translation = translation(domain=APP_DOMAIN, localedir=resources.traversable.joinpath("locales"))

    gettextlib.gettext = app_translation.gettext
    gettextlib.ngettext = app_translation.ngettext
    gettextlib.pgettext = app_translation.pgettext
    gettextlib.npgettext = app_translation.npgettext


def setup_logging(verbose: bool):
    try:
        import colorlog
    except ImportError:
        colorlog = None

    handler = logging.StreamHandler()
    handler.setStream(sys.stdout)
    log_format = "{asctime} {levelname:8} {name:50.50} {message}"
    if colorlog:
        formatter = colorlog.ColoredFormatter("{log_color}" + log_format, style="{")
    else:
        formatter = logging.Formatter(log_format, style="{")

    handler.setFormatter(formatter)
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        handlers=[handler],
    )


def fix_home_env():
    """修复 Tkinter 在 Windows 中无法获取 HOME 的问题"""
    with suppress(RuntimeError):
        os.environ["HOME"] = str(Path.home())


def launch(*, quiet: bool, verbose: bool):
    from gettext import pgettext

    from vcf_generator_lite.constants import URL_REPOSITORY
    from vcf_generator_lite.ui.windows.main_window import create_app

    if quiet:
        sys.stdout = None

    setup_logging(verbose=verbose)
    fix_home_env()

    print(pgettext("startup.source_tip", "💡Tip: Source code is hosted at {url}").format(url=URL_REPOSITORY))

    app, _controller = create_app()
    app.mainloop()


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


def main():
    # 因为要替换所有 gettext 方法，所以必须在导入主要内容（包括 argparse）之前执行。
    setup_l10n()

    import argparse
    from gettext import pgettext

    from vcf_generator_lite.__version__ import __version__
    from vcf_generator_lite.utils.dpi_aware import enable_dpi_aware
    from vcf_generator_lite.utils.strings import get_app_description, get_app_name

    enable_dpi_aware()
    parser = argparse.ArgumentParser(
        description=get_app_description(),
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help=pgettext("cli.help_option_quiet", "quiet mode"),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help=pgettext("cli.help_option_verbose", "show details"),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{get_app_name()} {__version__}",
    )

    with redirect_to_messagebox_if_needed(title=get_app_name()):
        args = parser.parse_args()

    launch(quiet=args.quiet, verbose=args.verbose)


if __name__ == "__main__":
    main()
