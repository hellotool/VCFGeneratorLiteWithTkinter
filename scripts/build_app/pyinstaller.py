import subprocess
import sys

from scripts.build_app.utils import PATH_DIST, PATH_PACKAGING, ensure_dist_dir

PATH_DIST_PYINSTALLER = PATH_DIST.joinpath("vcf_generator_lite")

PATH_PYINSTALLER_SPEC = PATH_PACKAGING.joinpath("pyinstaller", "vcf_generator_lite.spec")


def build_with_pyinstaller():
    ensure_dist_dir()
    subprocess.run([sys.executable, "-m", "PyInstaller", str(PATH_PYINSTALLER_SPEC), "--noconfirm"], check=True)  # noqa: S603


def require_pyinstaller_dist():
    if not PATH_DIST_PYINSTALLER.is_dir():
        raise RuntimeError("PyInstaller build not found.")


def ensure_pyinstaller_dist():
    if not PATH_DIST_PYINSTALLER.exists():
        build_with_pyinstaller()
    require_pyinstaller_dist()
