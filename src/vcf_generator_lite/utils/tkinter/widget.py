from tkinter import Label, Misc, Tk
from tkinter.ttk import Label as TtkLabel


def get_root(misc: Misc) -> Tk:
    return misc.nametowidget(".")


def enable_auto_wrap(widget: Label | TtkLabel):
    widget.bind("<Configure>", lambda event: widget.configure(wraplength=event.width), "+")


def needs_sizegrip(parent: Misc) -> bool:
    """判断是否需要显示 Sizegrip。

    仅在 Windows 平台且窗口可调整大小时返回 ``True``。

    X11 平台存在已知 Bug：

    1. 首次拖动时窗口跳回屏幕原点 ``(0, 0)``。
    2. 后续拖动时窗口向下跳跃。

    由于上游 Tkinter 未修复，X11 平台禁用 Sizegrip。

    macOS 平台顶层窗口默认自带内置大小控制柄，无需额外创建。

    详见 `平台特定说明 <https://docs.python.org/zh-cn/3.14/library/tkinter.ttk.html#platform-specific-notes>`_。
    """
    if parent._windowingsystem != "win32":  # noqa: SLF001
        return False

    return any(parent.winfo_toplevel().resizable())
