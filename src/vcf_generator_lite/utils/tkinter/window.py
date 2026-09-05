from abc import ABC
from contextlib import contextmanager
from tkinter import Misc, Tk, Toplevel, Wm

from vcf_generator_lite.utils.tkinter.scaling import scale_args

type Window = Tk | Toplevel


class WindowExtension(Misc, Wm, ABC):
    """窗口方法扩展基类"""


type WindowOrExtension = Window | WindowExtension


class GeometryWindowExtension(WindowExtension, ABC):
    """带缩放的窗口尺寸方法扩展"""

    def wm_size(self, width: int, height: int):
        self.wm_geometry(f"{width}x{height}")

    def wm_size_pt(self, width: int, height: int):
        self.wm_size(*scale_args(self, width, height))

    def wm_minsize_pt(self, width: int, height: int):
        self.wm_minsize(*scale_args(self, width, height))

    def wm_maxsize_pt(self, width: int, height: int):
        self.wm_maxsize(*scale_args(self, width, height))


def center_reference_rect(window: Tk | Toplevel, rect_x: int, rect_y: int, rect_width: int, rect_height: int):
    client_x_min = window.winfo_vrootx()
    client_x_max = client_x_min + window.winfo_vrootwidth() - window.winfo_width()
    client_y_min = window.winfo_vrooty()
    client_y_max = client_y_min + window.winfo_vrootheight() - window.winfo_height()
    if window._windowingsystem == "aqua":  # noqa: SLF001
        client_y_min = max(client_y_min, 22)

    client_x = rect_x + (rect_width - window.winfo_width()) // 2
    client_x = max(min(client_x, client_x_max), client_x_min)
    client_y = rect_y + (rect_height - window.winfo_height()) // 2
    client_y = max(min(client_y, client_y_max), client_y_min)
    # 在 Windows 上，winfo_x/y 是窗口坐标，而 winfo_rootx/y 是工作区坐标，geometry 接收窗口坐标，
    # 所以需要将工作区坐标转换为窗口坐标。
    window_x = client_x - window.winfo_rootx() + window.winfo_x()
    window_y = client_y - window.winfo_rooty() + window.winfo_y()
    window.geometry(f"+{window_x}+{window_y}")


def center_reference_screen(window: Tk | Toplevel):
    center_reference_rect(
        window,
        rect_x=0,
        rect_y=0,
        rect_width=window.winfo_screenwidth(),
        rect_height=window.winfo_screenheight(),
    )


def center_reference_master(window: Toplevel):
    center_reference_rect(
        window,
        rect_x=window.master.winfo_rootx(),
        rect_y=window.master.winfo_rooty(),
        rect_width=window.master.winfo_width(),
        rect_height=window.master.winfo_height(),
    )


@contextmanager
def withdraw_cm(wm: Wm):
    """窗口隐藏上下文管理器。

    专门解决 Tkinter 窗口初始化时因设置属性导致的闪烁问题。通过上下文管理器在初始化期间隐藏窗口，
    所有属性配置完成后再显示窗口，避免窗口在左上角短暂闪现的异常现象。
    """
    wm.wm_withdraw()
    yield
    wm.wm_deiconify()
