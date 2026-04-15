from tkinter import Misc
from tkinter.ttk import Scrollbar, Style, Treeview

from vcf_generator_lite.utils.graphics import FPixelPadding, parse_ttk_padding


class ScrolledTreeview(Treeview):
    def __init__(self, master: Misc | None = None, *, vertical: bool = True, **kw):
        super().__init__(master, **kw)
        self.vbar: Scrollbar | None = None
        self._style = Style(self)
        self._border_padding: FPixelPadding = parse_ttk_padding(
            self,
            value=self._style.lookup(
                style=self["style"] or "Treeview",
                option="borderwidth",
                default=1,
            ),
        )
        self._padding: FPixelPadding = FPixelPadding()
        if vertical:
            self._create_vertical_scrollbar()

    @property
    def padding(self) -> FPixelPadding:
        return self._get_current_padding()

    @padding.setter
    def padding(self, padding: FPixelPadding):
        self.configure(padding=padding.to_tuple())

    def _create_vertical_scrollbar(self):
        if not self.vbar:
            self.vbar = Scrollbar(self, orient="vertical")
            self.vbar.configure(command=self.yview)
            internal_padding = self.padding
            place_padding = self._border_padding + internal_padding
            self.vbar.pack(
                side="right",
                fill="y",
                pady=place_padding.to_pady(),
                padx=(0, place_padding.right),
            )
            self.configure(yscrollcommand=self.vbar.set)
            self.padding += FPixelPadding(right=self.vbar.winfo_reqwidth() + internal_padding.right)

    def _get_current_padding(self) -> FPixelPadding:
        padding = self.cget("padding")
        if not padding:
            padding = Style(self).lookup(self.cget("style") or "Treeview", "padding")
        if not padding:
            padding = 0
        return parse_ttk_padding(self, padding)
