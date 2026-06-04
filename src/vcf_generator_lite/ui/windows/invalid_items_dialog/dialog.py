from collections.abc import Callable
from gettext import pgettext
from tkinter import Event, Tk, Toplevel
from typing import override

from vcf_generator_lite.core.vcf_generator import InvalidItem
from vcf_generator_lite.ui.windows.base_window import EnhancedDialog
from vcf_generator_lite.ui.windows.base_window.constants import EVENT_EXIT
from vcf_generator_lite.ui.windows.invalid_items_dialog.layout import InvalidItemsLayout


class InvalidItemsDialog(EnhancedDialog, InvalidItemsLayout.Listener):
    def __init__(
        self,
        master: Tk | Toplevel,
        *,
        display_path: str,
        invalid_items: list[InvalidItem],
        line_enter_listener: Callable[[InvalidItem], None] | None = None,
    ):
        self._line_enter_listener: Callable[[InvalidItem], None] | None = line_enter_listener
        self.display_path = display_path
        self.invalid_items = invalid_items
        super().__init__(master)

    @override
    def _configure_ui_withdraw(self):
        super()._configure_ui_withdraw()
        self.title(pgettext("vcf_generate_invalid_dialog.title", "vCard File Generation Complete"))
        self.resizable(True, True)
        self.wm_size_pt(360, 320)
        self.wm_minsize_pt(225, 225)

        self.layout = InvalidItemsLayout(self, self.display_path, self)
        self.layout.set_invalid_items(self.invalid_items)

        self.bind("<Return>", self.on_return)

    @override
    def _configure_ui(self):
        super()._configure_ui()
        self.bell()
        self.update()

    def on_return(self, event: Event):
        if event.widget is self.layout.content_tree:
            return
        self.layout.ok_button.invoke()

    @override
    def on_ok(self):
        self.event_generate(EVENT_EXIT)

    @override
    def on_tree_view_enter(self, id_: int):
        if self._line_enter_listener:
            self._line_enter_listener(next(item for item in self.invalid_items if item.row_position == id_))
