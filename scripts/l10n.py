import argparse
import os
import subprocess
import sysconfig

from scripts.app_metadata import app_metadata, app_version_variants
from scripts.utils import PATH_SOURCE_RELATIVE, Path, require_external_tool

APP_DOMAIN = "vcf-generator-lite"

PATH_STD_LIB_SYMBOL_RELATIVE = Path(".stdlib_symbol")
PATH_STD_LIB = sysconfig.get_path("stdlib")
PATH_ARG_PARSER_RELATIVE_STD_LIB = Path(argparse.__file__).relative_to(PATH_STD_LIB)
PATH_ARG_PARSER_SYMBOL_RELATIVE = PATH_STD_LIB_SYMBOL_RELATIVE / PATH_ARG_PARSER_RELATIVE_STD_LIB


PATH_LOCALES_RELATIVE = PATH_SOURCE_RELATIVE / "vcf_generator_lite" / "resources" / "locales"
PATH_MSG_POT_RELATIVE = PATH_LOCALES_RELATIVE / "templates" / f"{APP_DOMAIN}.pot"


def require_babel() -> Path:
    return require_external_tool("pybabel", "Babel")


def extract():
    babel_path = require_babel()
    if PATH_STD_LIB_SYMBOL_RELATIVE.exists():
        PATH_STD_LIB_SYMBOL_RELATIVE.unlink()
    PATH_STD_LIB_SYMBOL_RELATIVE.symlink_to(PATH_STD_LIB, target_is_directory=True)
    try:
        PATH_MSG_POT_RELATIVE.parent.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        scripts_root = str(Path(__file__).resolve().parent.parent)
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = scripts_root + (os.pathsep + existing_pythonpath if existing_pythonpath else "")
        dynamic_args = []
        if app_metadata.copyright:
            dynamic_args.append("--copyright-holder")
            dynamic_args.append(app_metadata.author)
        if app_metadata.author_email:
            dynamic_args.append("--msgid-bugs-address")
            dynamic_args.append(app_metadata.author_email)
        subprocess.run(  # noqa: S603
            [
                babel_path,
                "extract",
                "--mapping-file",
                Path("pyproject.toml"),
                "--output-file",
                PATH_MSG_POT_RELATIVE,
                "--no-wrap",
                "--sort-by-file",
                "--project",
                app_metadata.display_name,
                "--version",
                app_version_variants.wheel,
                *dynamic_args,
                PATH_SOURCE_RELATIVE,
                PATH_ARG_PARSER_SYMBOL_RELATIVE,
            ],
            check=True,
            env=env,
        )
    finally:
        if PATH_STD_LIB_SYMBOL_RELATIVE.exists():
            PATH_STD_LIB_SYMBOL_RELATIVE.unlink()


def initialize(locale: str):
    babel_path = require_babel()
    subprocess.run(  # noqa: S603
        [
            babel_path,
            "init",
            "--input-file",
            PATH_MSG_POT_RELATIVE,
            "--output-dir",
            PATH_LOCALES_RELATIVE,
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
            PATH_MSG_POT_RELATIVE,
            "--output-dir",
            PATH_LOCALES_RELATIVE,
            "--domain",
            APP_DOMAIN,
            "--no-wrap",
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
            PATH_LOCALES_RELATIVE,
            "--domain",
            APP_DOMAIN,
            "--statistics",
            *dynamic_args,
        ],
        check=True,
    )
