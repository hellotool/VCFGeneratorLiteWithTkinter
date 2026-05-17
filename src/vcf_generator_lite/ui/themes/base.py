from tkinter import Tk
from tkinter.ttk import Style
from typing import override

from vcf_generator_lite.ui.themes.abstract import ThemePatcher


class BaseThemePatcher(ThemePatcher):
    def __init__(self, app: Tk):
        self.app: Tk = app
        self.style: Style = Style(app)
        self.last_patched_theme: str | None = None

    @override
    def patch(self):
        self.last_patched_theme = self.style.theme_use()

    @override
    def get_last_patched_theme(self) -> str | None:
        return self.last_patched_theme
