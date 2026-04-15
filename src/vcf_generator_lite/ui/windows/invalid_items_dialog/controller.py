from collections.abc import Callable
from tkinter import Event, EventType

from vcf_generator_lite.core.vcf_generator import InvalidItem
from vcf_generator_lite.ui.windows.invalid_items_dialog.dialog import InvalidItemsDialog


class InvalidItemsController:
    def __init__(
        self,
        window: InvalidItemsDialog,
        display_path: str,
        invalid_items: list[InvalidItem],
    ):
        self.window = window
        self.__line_enter_listener: Callable[[int, str], None] | None = None
        window.bind("<Return>", self.__on_return)

        window.set_display_path(display_path)

        window.content_tree.bind("<Double-Button-1>", self.__on_tree_view_enter)
        window.content_tree.bind("<Return>", self.__on_tree_view_enter)

        window.update()
        window.set_invalid_items(invalid_items)

    def __on_return(self, event: Event):
        if event.widget is self.window.content_tree:
            return
        self.window.ok_button.invoke()

    def __on_tree_view_enter(self, event: Event):
        selection = self.window.content_tree.selection()
        if (
            self.__line_enter_listener
            and len(selection) > 0
            and (
                self.window.content_tree.identify_region(event.x, event.y) == "cell"
                or event.type != EventType.ButtonPress
            )
        ):
            line = int(selection[0])
            data = self.window.content_tree.item(line, "values")[1]
            self.__line_enter_listener(line, data)

    def set_line_enter_listener(self, listener: Callable[[int, str], None] | None):
        self.__line_enter_listener = listener
