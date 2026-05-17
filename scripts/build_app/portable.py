from zipfile import ZipFile

from scripts.app_metadata import app_version_variants
from scripts.build_app.pyinstaller import (
    PATH_DIST_PYINSTALLER,
    build_with_pyinstaller,
    ensure_pyinstaller_dist,
)
from scripts.build_app.utils import PATH_DIST, PLATFORM_NATIVE

DISTRIBUTION_PORTABLE_NAME = f"VCFGeneratorLite-v{app_version_variants.wheel}-{PLATFORM_NATIVE}-portable.zip"

PATH_DIST_PORTABLE = PATH_DIST.joinpath(DISTRIBUTION_PORTABLE_NAME)


def build_portable(*, force: bool = False):
    if force:
        build_with_pyinstaller()
    else:
        ensure_pyinstaller_dist()
    with ZipFile(PATH_DIST_PORTABLE, "w") as zip_file:
        for file_path in PATH_DIST_PYINSTALLER.rglob("*"):
            zip_file.write(file_path, file_path.relative_to(str(PATH_DIST)))
