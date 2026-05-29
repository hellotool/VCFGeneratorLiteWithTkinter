import logging
from abc import ABC
from tkinter import Event, PhotoImage, Tk, Toplevel, Wm
from tkinter.ttk import Style
from types import TracebackType
from typing import TYPE_CHECKING, override

from vcf_generator_lite.ui.themes.default_theme_patcher import DefaultThemePatcher
from vcf_generator_lite.ui.windows.base_window.constants import EVENT_EXIT
from vcf_generator_lite.utils import resources
from vcf_generator_lite.utils.tkinter.window import (
    GeometryWindowExtension,
    WindowExtension,
    center_reference_master,
    center_reference_screen,
    withdraw_cm,
)

if TYPE_CHECKING:
    from vcf_generator_lite.ui.themes.abstract import ThemePatcher

__all__ = ["EnhancedDialog", "EnhancedTk", "EnhancedToplevel"]
_logger = logging.getLogger(__name__)


class AppWindowExtension(
    GeometryWindowExtension,
    WindowExtension,
    ABC,
):
    """应用程序窗口扩展基类，集成多个窗口功能扩展

    特性：
    - 继承 GeometryWindowExtension: 提供基于物理/虚拟像素的窗口尺寸控制
    - 继承 CenterWindowExtension: 实现窗口居中显示功能
    - 继承 WindowExtension: 基础窗口功能扩展
    """

    def __init__(self):
        super().__init__()
        with withdraw_cm(self):
            self._configure_ui_withdraw()
            self.update_idletasks()  # 在 deiconify 前调用可以一定程度上防止首次启动时窗口闪烁
        self._configure_ui()

    def _configure_ui_withdraw(self):
        # 为了在系统主题切换时正确更新背景而浪费系统资源没必要，并且还要其他地方不会更新配色，用户只能重启解决。
        # self.root_frame = Frame(self)  # noqa: ERA001
        # self.root_frame.place(relwidth=1, relheight=1)  # noqa: ERA001
        self.__apply_default_events()

    def _configure_ui(self):
        self.update_idletasks()

    def __apply_default_events(self):
        self.protocol("WM_DELETE_WINDOW", lambda: self.event_generate(EVENT_EXIT))
        self.bind(EVENT_EXIT, lambda _: self.destroy())


def raise_callback_exception(_exc: type[BaseException], val: BaseException, _tb: TracebackType | None = None):
    raise val


class EnhancedTk(Tk, AppWindowExtension, ABC):
    def __init__(self, **kw):
        super().__init__(baseName="vcf_generator_lite", **kw)
        self.previous_patched_theme: str | None = None

        self.theme_patcher: ThemePatcher
        if not hasattr(self, "theme_patcher"):  # 配置文件中可能已定义此属性，防止覆盖配置文件的属性
            self.theme_patcher = DefaultThemePatcher(self)
        _logger.debug("Loaded theme patcher: %s.", self.theme_patcher)

        self.report_callback_exception = raise_callback_exception

        AppWindowExtension.__init__(self)

    @override
    def _configure_ui(self):
        if self._windowingsystem == "win32":
            # 居中于屏幕功能在 Linux 端的多屏下表现得不是很好，因此遵循默认设定。
            center_reference_screen(self)
        super()._configure_ui()

    @override
    def _configure_ui_withdraw(self):
        self.apply_theme_patch()
        super()._configure_ui_withdraw()
        self.__apply_default_icon()
        self.bind("<<ThemeChanged>>", self.__on_theme_changed, "+")

    def __apply_default_icon(self):
        self.iconphoto(True, PhotoImage(master=self, data=resources.read_binary("images/icon-48.png")))

    def apply_theme_patch(self):
        theme_name = Style(self).theme_use()
        if self.previous_patched_theme == theme_name:
            return
        self.previous_patched_theme = theme_name
        self.theme_patcher.patch()

    def __on_theme_changed(self, event: Event):
        if event.widget != self:
            return
        self.apply_theme_patch()


class EnhancedToplevel(Toplevel, AppWindowExtension, ABC):
    def __init__(self, master: Tk | Toplevel, **kw):
        super().__init__(master, **kw)
        AppWindowExtension.__init__(self)

    @override
    def _configure_ui(self):
        center_reference_master(self)
        super()._configure_ui()


class EnhancedDialog(EnhancedToplevel, ABC):
    @override
    def _configure_ui_withdraw(self):
        super()._configure_ui_withdraw()
        self.bind("<Escape>", lambda _: self.event_generate(EVENT_EXIT))

        if isinstance(self.master, Wm):
            self.transient(self.master)
            self.resizable(False, False)
