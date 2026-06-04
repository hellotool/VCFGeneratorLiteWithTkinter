from abc import ABC
from tkinter import Tk
from tkinter.ttk import Style

from vcf_generator_lite.ui.themes.abstract import ThemePatcher


class BaseThemePatcher(ThemePatcher, ABC):
    def __init__(self, app: Tk):
        self.app: Tk = app
        self.style: Style = Style(app)
