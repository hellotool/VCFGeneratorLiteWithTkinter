import subprocess
from pathlib import Path

import requests

from scripts.app_metadata import app_version_variants
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
from vcf_generator_lite.constants import APP_COPYRIGHT

DISTRIBUTION_INSTALLER_BASE_NAME = f"VCFGeneratorLite-v{app_version_variants.wheel}-{PLATFORM_NATIVE}-setup"

PATH_DIST_INSTALLER = PATH_DIST.joinpath(DISTRIBUTION_INSTALLER_BASE_NAME + ".exe")

PATH_PACKAGING_INNO_SETUP = PATH_PACKAGING.joinpath("innosetup")
PATH_INNO_SETUP_ISS = PATH_PACKAGING_INNO_SETUP.joinpath("vcf_generator_lite.iss")
PATH_INNOSETUP_EXTENSIONS = PATH_PACKAGING_INNO_SETUP.joinpath(".extensions")
PATH_CHINESE_SIMPLIFIED = PATH_INNOSETUP_EXTENSIONS.joinpath("Languages", "ChineseSimplified.isl")

URL_CHINESE_SIMPLIFIED_ISL_URL = (
    "https://raw.github.com/jrsoftware/issrc/main/Files/Languages/Unofficial/ChineseSimplified.isl"
)
URL_CHINESE_SIMPLIFIED_ISL_LATEST = (
    "https://github.com/kira-96/Inno-Setup-Chinese-Simplified-Translation/raw/refs/heads/main/ChineseSimplified.isl"
)


def prepare_innosetup_extensions(
    download_url: str = URL_CHINESE_SIMPLIFIED_ISL_LATEST,
    *,
    verify_ssl: bool = True,
):
    print("Preparing InnoSetup extensions.")
    response = requests.get(download_url, verify=verify_ssl)
    response.raise_for_status()
    PATH_CHINESE_SIMPLIFIED.parent.mkdir(parents=True, exist_ok=True)
    PATH_CHINESE_SIMPLIFIED.write_bytes(response.content)
    print("Downloaded Chinese Simplified ISL.")


def ensure_innosetup_extensions(*, verify_ssl: bool = True):
    if not PATH_INNOSETUP_EXTENSIONS.exists():
        prepare_innosetup_extensions(verify_ssl=verify_ssl)


def ensure_installer_dist():
    if not PATH_DIST_INSTALLER.exists():
        build_installer()


def require_iscc() -> Path:
    return require_external_tool("iscc", "InnoSetup", "C:\\Program Files (x86)\\Inno Setup 6\\")


def build_installer(*, no_verify_ssl: bool = False, force: bool = False, force_download: bool = False):
    iscc_path = require_iscc()
    if force:
        build_with_pyinstaller()
    else:
        ensure_pyinstaller_dist()
    if force_download:
        prepare_innosetup_extensions(verify_ssl=not no_verify_ssl)
    else:
        ensure_innosetup_extensions(verify_ssl=not no_verify_ssl)

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

    subprocess.run(  # noqa: S603
        [
            iscc_path,
            "/D" + f"OutputBaseFilename={DISTRIBUTION_INSTALLER_BASE_NAME}",
            "/D" + f"MyAppCopyright={APP_COPYRIGHT}",
            "/D" + f"MyAppVersion={app_version_variants.wheel}",
            "/D" + f"VersionInfoVersion={app_version_variants.windows}",
            "/D" + f"ArchitecturesAllowed={architectures_allowed}",
            "/D" + f"ArchitecturesInstallIn64BitMode={architectures_install_in64_bit_mode}",
            PATH_INNO_SETUP_ISS,
        ],
        check=True,
    )
