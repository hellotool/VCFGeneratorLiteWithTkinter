import subprocess
from pathlib import Path

from scripts.app_metadata import app_metadata, app_version_variants
from scripts.build_app.pyinstaller import (
    build_with_pyinstaller,
    ensure_pyinstaller_dist,
)
from scripts.build_app.utils import (
    PATH_DIST,
    PATH_PACKAGING,
    PLATFORM_NATIVE,
)
from scripts.utils import require_external_tool

DISTRIBUTION_INSTALLER_BASE_NAME = f"VCFGeneratorLite-v{app_version_variants.wheel}-{PLATFORM_NATIVE}-setup"

PATH_DIST_INSTALLER = PATH_DIST.joinpath(DISTRIBUTION_INSTALLER_BASE_NAME + ".exe")

PATH_PACKAGING_INNO_SETUP = PATH_PACKAGING.joinpath("innosetup")
PATH_INNO_SETUP_ISS = PATH_PACKAGING_INNO_SETUP.joinpath("vcf_generator_lite.iss")


def ensure_installer_dist():
    if not PATH_DIST_INSTALLER.exists():
        build_installer()


def require_iscc() -> Path:
    return require_external_tool("iscc", "InnoSetup", "C:\\Program Files (x86)\\Inno Setup 6\\")


def build_installer(*, force: bool = False):
    iscc_path = require_iscc()
    if force:
        build_with_pyinstaller()
    else:
        ensure_pyinstaller_dist()

    match PLATFORM_NATIVE:
        case "win-amd64":
            architectures_allowed = "x64compatible"
            architectures_install_in64_bit_mode = "win64"
        case "win-arm64":
            architectures_allowed = "arm64"
            architectures_install_in64_bit_mode = "win64"
        case _:
            architectures_allowed = "x86compatible"
            architectures_install_in64_bit_mode = ""

    subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [
            iscc_path,
            "/D" + f"AppName={app_metadata.display_name}",
            "/D" + f"AppPublisher={app_metadata.author}",
            "/D" + f"OutputBaseFilename={DISTRIBUTION_INSTALLER_BASE_NAME}",
            "/D" + f"AppCopyright={app_metadata.copyright}",
            "/D" + f"AppVersion={app_version_variants.wheel}",
            "/D" + f"VersionInfoVersion={app_version_variants.windows}",
            "/D" + f"ArchitecturesAllowed={architectures_allowed}",
            "/D" + f"ArchitecturesInstallIn64BitMode={architectures_install_in64_bit_mode}",
            PATH_INNO_SETUP_ISS,
        ],
        check=True,
    )
