import os
import shutil
import sys
import sysconfig
from pathlib import Path

PYTHON_VERSION = sysconfig.get_python_version()
PLATFORM_PYTHON = f"{sys.implementation.name}-{PYTHON_VERSION}"
PLATFORM_NATIVE = sysconfig.get_platform()

PATH_DIST: Path = Path("dist").resolve()
PATH_BUILD: Path = Path("build").resolve()
PATH_PACKAGING: Path = Path("packaging").resolve()


class ToolNotFoundError(Exception):
    def __init__(self, display_name: str):
        super().__init__(f"{display_name} not found.")


def ensure_dist_dir():
    if not PATH_DIST.is_dir():
        PATH_DIST.mkdir(parents=True, exist_ok=True)


def require_external_tool(executable: str, display_name: str, fallback_path: str | None = None) -> Path:
    path = os.environ["PATH"]
    if fallback_path is not None:
        path += os.pathsep + fallback_path
    executable_path = shutil.which(executable, path=path)
    if executable_path is None:
        raise ToolNotFoundError(display_name)
    return Path(executable_path)


def require_uv() -> Path:
    return require_external_tool("uv", "uv")
