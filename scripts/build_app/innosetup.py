import subprocess
import sys
from pathlib import Path

import requests

from scripts.app_metadata import app_version_variants
from scripts.build_app.common import (
    PATH_DIST,
    PATH_PACKAGING,
    PLATFORM_NATIVE,
    require_external_tool,
)
from scripts.build_app.pyinstaller import ensure_pyinstaller_dist
from vcf_generator_lite.constants import APP_COPYRIGHT

DISTRIBUTION_INSTALLER_BASE_NAME = f"VCFGeneratorLite-v{app_version_variants.wheel}-{PLATFORM_NATIVE}-setup"

PATH_DIST_INSTALLER = PATH_DIST.joinpath(DISTRIBUTION_INSTALLER_BASE_NAME + ".exe")
PATH_INNOSETUP_EXTENSIONS = Path("packaging", "innosetup", ".extensions").absolute()
PATH_CHINESE_SIMPLIFIED = PATH_INNOSETUP_EXTENSIONS.joinpath("Languages", "ChineseSimplified.isl")

URL_CHINESE_SIMPLIFIED_ISL_URL = (
    "https://raw.github.com/jrsoftware/issrc/main/Files/Languages/Unofficial/ChineseSimplified.isl"
)
URL_CHINESE_SIMPLIFIED_ISL_LATEST = (
    "https://github.com/kira-96/Inno-Setup-Chinese-Simplified-Translation/raw/refs/heads/main/ChineseSimplified.isl"
)


def prepare_innosetup_extensions(
    download_url: str = URL_CHINESE_SIMPLIFIED_ISL_LATEST,
):
    print("Preparing InnoSetup extensions.")
    response = requests.get(download_url)
    if response.status_code != 200:
        print(
            f"Failed to download Chinese Simplified ISL: {response.status_code}",
            file=sys.stderr,
        )
        sys.exit(1)
    file_text = response.text
    # 获取到的内容是 CRLF 换行的，但是 python 只能识别 LF 换行，所以需要替换一下
    file_text = file_text.replace("\r", "")

    PATH_CHINESE_SIMPLIFIED.parent.mkdir(parents=True, exist_ok=True)
    with PATH_CHINESE_SIMPLIFIED.open("w", encoding=response.encoding, newline="\r\n") as f:
        f.write(file_text)
    print("Downloaded Chinese Simplified ISL.")


def ensure_innosetup_extensions():
    if not PATH_INNOSETUP_EXTENSIONS.exists():
        prepare_innosetup_extensions()


def ensure_installer_dist():
    if not PATH_DIST_INSTALLER.exists():
        build_installer()


def build_installer():
    iscc_path = require_external_tool("iscc", "InnoSetup", "C:\\Program Files (x86)\\Inno Setup 6\\")
    ensure_pyinstaller_dist()
    ensure_innosetup_extensions()

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
            PATH_PACKAGING.joinpath("innosetup", "vcf_generator_lite.iss").absolute(),
        ],
        check=True,
    )
