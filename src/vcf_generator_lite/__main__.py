from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import ArgumentParser

__all__ = ["main"]


def get_args_parser() -> "ArgumentParser":
    import argparse
    from gettext import pgettext

    from vcf_generator_lite.__version__ import __version__
    from vcf_generator_lite.ui.app_text import app_description, app_name

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
    return parser


def main():
    from vcf_generator_lite.bootstrap import (
        launch,
        redirect_stdio_to_messagebox_if_needed,
        setup_excepthook,
        setup_l10n,
    )

    # 因为要替换所有 gettext 方法，所以必须在导入主要内容（包括 argparse）之前执行。
    setup_l10n()
    from vcf_generator_lite.ui.app_text import app_name
    from vcf_generator_lite.utils.dpi_aware import enable_dpi_aware

    enable_dpi_aware()
    setup_excepthook()

    with redirect_stdio_to_messagebox_if_needed(app_name=app_name()):
        args = get_args_parser().parse_args()

    launch(quiet=args.quiet, verbose=args.verbose)


if __name__ == "__main__":
    main()
