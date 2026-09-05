import os
import shutil
from pathlib import Path

PATH_SOURCE_RELATIVE: Path = Path("src")


class ToolNotFoundError(Exception):
    def __init__(self, display_name: str):
        super().__init__(f"{display_name} not found.")


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
