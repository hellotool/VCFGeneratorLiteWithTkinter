import shutil
import subprocess
import zipapp
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.app_metadata import app_version_variants
from scripts.build_app.common import PATH_DIST, ensure_dist_dir
from scripts.build_app.wheel import ensure_wheel_dist
from scripts.utils import require_uv

DISTRIBUTION_ZIPAPP_NAME = f"VCFGeneratorLite-v{app_version_variants.wheel}-py3.pyzw"

PATH_DIST_ZIPAPP = PATH_DIST.joinpath(DISTRIBUTION_ZIPAPP_NAME)


def build_zipapp():
    ensure_dist_dir()
    uv_path = require_uv()

    whl_path = ensure_wheel_dist()

    with TemporaryDirectory() as zipapp_build_path_str:
        zipapp_build_path = Path(zipapp_build_path_str)
        site_packages_path = zipapp_build_path / "site-packages"

        subprocess.run(  # noqa: S603
            [
                uv_path,
                "pip",
                "install",
                whl_path,
                "--no-cache",
                "--target",
                site_packages_path,
            ],
            text=True,
            check=True,
        )

        # 清理无用内容
        if (bin_path := site_packages_path / "bin").is_dir():
            shutil.rmtree(bin_path)
        site_packages_path.joinpath(".lock").unlink()

        for info_dir_paths in site_packages_path.glob("*.dist-info"):
            for file in info_dir_paths.iterdir():
                if file.name not in ("METADATA", "licenses"):
                    if file.is_file():
                        file.unlink()
                    else:
                        shutil.rmtree(file)

        if PATH_DIST_ZIPAPP.exists():
            PATH_DIST_ZIPAPP.unlink()
        zipapp.create_archive(
            site_packages_path,
            target=PATH_DIST_ZIPAPP,
            main="vcf_generator_lite.__main__:main",
            interpreter="/usr/bin/env python3",
            compressed=True,
        )
