from tkinter import Misc
from typing import Any, overload

from vcf_generator_lite.utils.tkinter.widget import get_root

__all__ = ["get_scaling", "scale", "scale_args", "scale_kw"]

_ATTR_SCALING_CACHED = "_scaling_cached"


def get_scaling(master: Misc) -> float:
    """获取 GUI 缩放比例因子

    与 ``tk scaling`` 相同。

    - Tk 手册页：https://www.tcl-lang.org/man/tcl8.6/TkCmd/tk.htm
    """
    root = get_root(master)
    if hasattr(root, _ATTR_SCALING_CACHED):
        return getattr(root, _ATTR_SCALING_CACHED)

    factor = master.tk.call("tk", "scaling")
    setattr(root, _ATTR_SCALING_CACHED, factor)
    return factor


@overload
def scale(master: Misc, value: int) -> int: ...
@overload
def scale(master: Misc, value: float) -> float: ...
def scale(master: Misc, value: float) -> float:
    scaled = get_scaling(master) * value
    return int(scaled) if isinstance(value, int) else float(scaled)


@overload
def scale_args(master: Misc, *args: int) -> tuple[int, ...]: ...
@overload
def scale_args(master: Misc, *args: float) -> tuple[float, ...]: ...
def scale_args(master: Misc, *args: float) -> tuple[float, ...]:
    return tuple(scale(master, value) for value in args)


def scale_kw(master: Misc, **kwargs: float) -> dict[str, Any]:
    return {key: scale(master, value) for key, value in kwargs.items()}
