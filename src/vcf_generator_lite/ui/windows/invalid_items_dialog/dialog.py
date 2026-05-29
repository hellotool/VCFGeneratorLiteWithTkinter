from collections.abc import Callable
from gettext import pgettext
from tkinter import Event, EventType, Tk, Toplevel
from typing import override

from vcf_generator_lite.core.vcf_generator import InvalidItem
from vcf_generator_lite.ui.app_text import error_for
from vcf_generator_lite.ui.windows.base_window import EnhancedDialog
from vcf_generator_lite.ui.windows.invalid_items_dialog.layout import InvalidItemsDialogLayout


class InvalidItemsDialog(EnhancedDialog):
    def __init__(
        self,
        master: Tk | Toplevel,
        display_path: str,
        invalid_items: list[InvalidItem],
        line_enter_listener: Callable[[int, str], None] | None = None,
    ):
        self._line_enter_listener: Callable[[int, str], None] | None = line_enter_listener
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
        self.layout = InvalidItemsDialogLayout(self, self)
        self.set_invalid_items(self.invalid_items)

        self.bind("<Return>", self.on_return)

    @override
    def _configure_ui(self):
        super()._configure_ui()
        self.bell()
        self.update()

    def set_invalid_items(self, items: list[InvalidItem]):
        self.layout.content_tree.delete(*self.layout.content_tree.get_children())
        for item in items:
            self.layout.content_tree.insert(
                parent="",
                index="end",
                id=item.row_position,
                values=(
                    pgettext("vcf_generate_invalid_dialog.cell_row", "Row {row}").format(row=item.row_position),
                    item.raw_content,
                    error_for(item.exception),
                ),
            )

    def set_line_enter_listener(self, listener: Callable[[int, str], None] | None):
        self._line_enter_listener = listener

    def on_return(self, event: Event):
        if event.widget is self.layout.content_tree:
            return
        self.layout.ok_button.invoke()

    def on_tree_view_enter(self, event: Event):
        selection = self.layout.content_tree.selection()
        if (
            self._line_enter_listener
            and len(selection) > 0
            and (
                self.layout.content_tree.identify_region(event.x, event.y) == "cell"
                or event.type != EventType.ButtonPress
            )
        ):
            line = int(selection[0])
            data = self.layout.content_tree.item(line, "values")[1]
            self._line_enter_listener(line, data)
