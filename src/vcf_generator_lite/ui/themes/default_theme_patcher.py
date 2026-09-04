import sys
from typing import override

from vcf_generator_lite.ui.themes.base import BaseThemePatcher
from vcf_generator_lite.utils.tkinter.style import lookup_font


class DefaultThemePatcher(BaseThemePatcher):
    @override
    def patch(self):
        self._patch_builtin_theme_common()

        theme_name = self.style.theme_use()
        if theme_name in ("vista", "winnative", "xpnative"):
            self._patch_vista_theme()
        elif theme_name in ("clam", "alt", "default", "classic"):
            self._patch_builtin_cross_platform_theme()
        self._patch_legacy_widgets()

    def _patch_legacy_widgets(self) -> None:
        background = self.style.lookup(".", "background")
        foreground = self.style.lookup(".", "foreground")
        select_background = self.style.lookup(".", "selectbackground")
        select_foreground = self.style.lookup(".", "selectforeground")

        self.app.configure(background=background)

        self.app.option_add("*Menu.background", background, "startupFile")
        self.app.option_add("*Menu.foreground", foreground, "startupFile")
        self.app.option_add("*Menu.activeBackground", select_background, "startupFile")
        self.app.option_add("*Menu.activeForeground", select_foreground, "startupFile")
        self.app.option_add("*Toplevel.background", background, "startupFile")

        if sys.platform == "win32":
            # Windows 7 中菜单默认不使用 TkMenuFont，因此需要手动设置字体。
            self.app.option_add("*Menu.font", "TkMenuFont", "startupFile")

    def _patch_builtin_theme_common(self) -> None:
        treeview_font = lookup_font(self.style, "Treeview", "font", default="TkDefaultFont")
        treeview_font_metrics = treeview_font.metrics()

        # 重写部分配置以适配高分屏
        self.style.configure("TButton", padding="2.5p")
        self.style.configure("TMenubutton", padding="2.5p")
        self.style.configure("Treeview", rowheight=treeview_font_metrics["linespace"] + self.app.winfo_pixels("2.5p"))
        self.style.configure("Heading", padding="1.5p")

    def _patch_vista_theme(self) -> None:
        self.style.configure(
            "ThemedText.TEntry",
            padding=0,
            borderwidth="1.5p",
        )
        # 使输入框在没有获取焦点时也显示选择的文字
        self.style.map("ThemedText.TEntry", selectbackground=[], selectforeground=[])

        # 对话框头部为白色
        self.style.configure("DialogHeader.TFrame", background="systemWindow")
        self.style.configure("DialogHeaderContent.TFrame", background="systemWindow")
        self.style.configure("DialogHeaderContent.TLabel", background="systemWindow")

    def _patch_builtin_cross_platform_theme(self) -> None:
        self.style.configure("Vertical.TScrollbar", arrowsize="9p")
        self.style.configure("Horizontal.TScrollbar", arrowsize="9p")  # 选择文件时使用
