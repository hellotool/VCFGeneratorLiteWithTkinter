import argparse
import subprocess
import sysconfig

from scripts.app_metadata import app_version_variants
from scripts.utils import PATH_SOURCE, Path, require_external_tool

APP_DOMAIN = "vcf-generator-lite"

PATH_STD_LIB_SYMBOL = Path(".stdlib_symbol").absolute()
PATH_STD_LIB = sysconfig.get_path("stdlib")
PATH_LOCALES = PATH_SOURCE / "vcf_generator_lite" / "resources" / "locales"
PATH_MSG_POT = PATH_LOCALES / "templates" / f"{APP_DOMAIN}.pot"


def require_babel() -> Path:
    return require_external_tool("pybabel", "Babel")


def extract():
    babel_path = require_babel()
    if PATH_STD_LIB_SYMBOL.exists():
        PATH_STD_LIB_SYMBOL.unlink()
    PATH_STD_LIB_SYMBOL.symlink_to(PATH_STD_LIB, target_is_directory=True)
    try:
        PATH_MSG_POT.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(  # noqa: S603
            [
                babel_path,
                "extract",
                "--output-file",
                PATH_MSG_POT,
                "--no-wrap",
                "--project",
                "VCF Generator Lite",
                "--version",
                app_version_variants.wheel,
                PATH_SOURCE,
                PATH_STD_LIB_SYMBOL / (Path(argparse.__file__).relative_to(PATH_STD_LIB)),
            ],
            check=True,
        )
    finally:
        if PATH_STD_LIB_SYMBOL.exists():
            PATH_STD_LIB_SYMBOL.unlink()


def initialize(locale: str):
    babel_path = require_babel()
    subprocess.run(  # noqa: S603
        [
            babel_path,
            "init",
            "--input-file",
            PATH_MSG_POT,
            "--output-dir",
            PATH_LOCALES,
            "--domain",
            APP_DOMAIN,
            "--no-wrap",
            "--locale",
            locale,
        ],
        check=True,
    )


def update():
    babel_path = require_babel()
    subprocess.run(  # noqa: S603
        [
            babel_path,
            "update",
            "--input-file",
            PATH_MSG_POT,
            "--output-dir",
            PATH_LOCALES,
            "--domain",
            APP_DOMAIN,
            "--no-wrap",
            "--update-header-comment",
        ],
        check=True,
    )


def compile_(locale: str | None):
    babel_path = require_babel()
    dynamic_args = []
    if locale is not None:
        dynamic_args.append("--locale")
        dynamic_args.append(locale)
    subprocess.run(  # noqa: S603
        [
            babel_path,
            "compile",
            "--directory",
            PATH_LOCALES,
            "--use-fuzzy",
            "--domain",
            APP_DOMAIN,
            *dynamic_args,
        ],
        check=True,
    )
