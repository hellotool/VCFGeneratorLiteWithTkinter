import subprocess
from pathlib import Path

from scripts.app_metadata import app_version_variants
from scripts.build_app.common import PATH_DIST, require_external_tool

PATH_DIST_WHEE = PATH_DIST.joinpath(f"vcf_generator_lite-{app_version_variants.wheel}-py3-none-any.whl")


def build_wheel():
    uv_path = require_external_tool("uv", "uv")
    subprocess.run([uv_path, "build", "--wheel"], text=True, check=True)  # noqa: S603


def require_wheel_dist() -> Path:
    try:
        return next(PATH_DIST.glob("*.whl"))
    except StopIteration:
        pass
    raise RuntimeError("Wheel build not found.")


def ensure_wheel_dist() -> Path:
    try:
        return next(PATH_DIST.glob("*.whl"))
    except StopIteration:
        build_wheel()

    return require_wheel_dist()
