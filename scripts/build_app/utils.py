import sys
import sysconfig
from pathlib import Path

PYTHON_VERSION = sysconfig.get_python_version()
PLATFORM_PYTHON = f"{sys.implementation.name}-{PYTHON_VERSION}"
PLATFORM_NATIVE = sysconfig.get_platform()

PATH_DIST: Path = Path("dist").resolve()
PATH_BUILD: Path = Path("build").resolve()
PATH_PACKAGING: Path = Path("packaging").resolve()


def ensure_dist_dir():
    if not PATH_DIST.is_dir():
        PATH_DIST.mkdir(parents=True, exist_ok=True)
