from typing import override

from vcf_generator_lite.ui.themes.base import BaseThemePatcher
from vcf_generator_lite.utils.tkinter.style import lookup_font


class DefaultThemePatcher(BaseThemePatcher):
    @override
    def patch(self):
        super().patch()
        self._patch_theme_common()
        theme_name = self.style.theme_use()
        if theme_name in ("vista", "winnative", "xpnative"):
            self._patch_vista_theme()
        elif theme_name in ("clam", "alt", "default", "classic"):
            self._patch_builtin_platform_independence_theme()

    def _patch_theme_common(self) -> None:
        background = self.style.lookup("TFrame", "background")

        # 使用 Sizegrip 调节窗口大小时可能会露出窗口背景，需要单独修改窗口背景色以避免露出破绽。
        self.app.configure(background=background)
        self.app.option_add("*Toplevel.background", background, "startupFile")

    def _patch_builtin_theme_common(self) -> None:
        treeview_font = lookup_font(self.style, "Treeview", "font", default="TkDefaultFont")
        treeview_font_metrics = treeview_font.metrics()

        # 重写部分配置以适配高分屏
        self.style.configure("TButton", padding="2.5p")
        self.style.configure("Treeview", rowheight=treeview_font_metrics["linespace"] + self.app.winfo_pixels("2.5p"))
        self.style.configure("Heading", padding="1.5p")

    def _patch_vista_theme(self) -> None:
        self._patch_builtin_theme_common()

        # 自定义组件
        self.style.configure("ThemedText.TEntry", padding=0, borderwidth="1.5p")
        self.style.configure("DialogHeader.TFrame", background="systemWindow")
        self.style.configure("DialogHeaderContent.TFrame", background="systemWindow")
        self.style.configure("DialogHeaderContent.TLabel", background="systemWindow")

        select_background = self.style.lookup("TEntry", "selectbackground", ["focus"])
        self.app.option_add("*ThemedText.Text.inactiveSelectBackground", select_background, "startupFile")

        # Windows 7 中菜单默认不使用 TkMenuFont，因此需要手动设置字体。
        self.app.option_add("*Menu.font", "TkMenuFont", "startupFile")

    def _patch_builtin_platform_independence_theme(self) -> None:
        self._patch_builtin_theme_common()

        self.style.configure("TButton", width=-8)
        self.style.configure("Vertical.TScrollbar", arrowsize="9p")
