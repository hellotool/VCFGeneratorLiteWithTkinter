import logging
import sys

__all__ = ["main"]


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


def launch(*, quiet: int, verbose: int):
    from gettext import pgettext

    from vcf_generator_lite.constants import URL_REPOSITORY
    from vcf_generator_lite.ui.windows.main_window import VCFGeneratorLiteApp
    from vcf_generator_lite.utils.environment import fix_home_env

    setup_logging(quiet=quiet, verbose=verbose)
    fix_home_env()
    if not quiet:
        print(pgettext("startup.source_tip", "💡Tip: Source code is hosted at {url}").format(url=URL_REPOSITORY))

    app = VCFGeneratorLiteApp()
    app.mainloop()


def main():
    # 因为要替换所有 gettext 方法，所以必须在导入主要内容（包括 argparse）之前执行。
    setup_l10n()

    import argparse
    from gettext import pgettext

    from vcf_generator_lite.__version__ import __version__
    from vcf_generator_lite.ui.app_text import app_description, app_name
    from vcf_generator_lite.utils.dpi_aware import enable_dpi_aware
    from vcf_generator_lite.utils.environment import redirect_to_messagebox_if_needed

    enable_dpi_aware()
    parser = argparse.ArgumentParser(
        description=app_description(),
    )
    output_level_group = parser.add_mutually_exclusive_group()
    output_level_group.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help=pgettext("cli.help_option_verbose", "increase output (use -vv for debug level)"),
    )
    output_level_group.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help=pgettext("cli.help_option_quiet", "decrease output (use -qq for errors only)"),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{app_name()} {__version__}",
    )

    with redirect_to_messagebox_if_needed(title=app_name()):
        args = parser.parse_args()

    launch(quiet=args.quiet, verbose=args.verbose)


if __name__ == "__main__":
    main()
