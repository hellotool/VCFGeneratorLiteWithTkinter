from gettext import pgettext
from tkinter import Misc
from tkinter.ttk import Button, Frame, Label, Sizegrip
from typing import TYPE_CHECKING, override

from vcf_generator_lite.ui.layouts.vertical_dialog_layout import VerticalDialogLayout
from vcf_generator_lite.ui.widgets.scrolled_treeview import ScrolledTreeview
from vcf_generator_lite.ui.windows.base_window.constants import EVENT_EXIT
from vcf_generator_lite.utils.tkinter.font import extend_font_scale
from vcf_generator_lite.utils.tkinter.scaling import scale_kw
from vcf_generator_lite.utils.tkinter.widget import enable_auto_wrap, needs_sizegrip

if TYPE_CHECKING:
    from vcf_generator_lite.ui.windows.invalid_items_dialog.dialog import InvalidItemsDialog


class InvalidItemsDialogLayout(VerticalDialogLayout):
    def __init__(self, parent: Misc, window: "InvalidItemsDialog"):
        super().__init__()
        self.window = window
        self._create_widgets(parent)

    @override
    def _create_header(self, parent: Misc):
        header_frame = Frame(parent, style="DialogHeader.TFrame")
        header_icon = Label(
            header_frame,
            text="\u26a0",
            font=extend_font_scale(24 / 9),
            style="DialogHeaderContent.TLabel",
            foreground="orange",
        )
        # 图标间距未严格遵循 Windows 的设计，因为那样会显得过于拥挤
        header_icon.pack(side="left", padx="8.25p", pady="8.25p", anchor="n")
        header_label = Label(
            header_frame,
            style="DialogHeaderContent.TLabel",
            text=pgettext(
                "vcf_generate_invalid_dialog.message", "File exported to {path}, invalid numbers have been ignored."
            ).format(path=self.window.display_path),
        )
        enable_auto_wrap(header_label)
        header_label.pack(fill="x", padx=(0, "8.25p"), pady="8.25p", anchor="center", expand=True)
        return header_frame

    @override
    def _create_content(self, parent: Misc):
        content_frame = Frame(parent)
        content_label = Label(
            content_frame, text=pgettext("vcf_generate_invalid_dialog.label_invalid_numbers", "Invalid numbers: ")
        )
        content_label.pack(fill="x", padx="8.25p", pady=("8.25p", "2p"))
        self.content_tree = ScrolledTreeview(
            content_frame,
            columns=("row", "original", "reason"),
            show="headings",
            selectmode="browse",
            height=0,
        )
        self.content_tree.column(
            column="row",
            anchor="w",
            stretch=False,
            **scale_kw(
                parent,
                width=60,
                minwidth=45,
            ),
        )
        # Tk 在创建窗口时调整 TreeView 列宽时不会考虑右侧 padding，添加 width=0 防止列溢出到滚动条区域。
        self.content_tree.column("original", anchor="w", width=0)
        self.content_tree.column("reason", anchor="w", width=0)
        self.content_tree.heading(
            "row",
            text=pgettext("vcf_generate_invalid_dialog.heading_row", "Position"),
            anchor="w",
        )
        self.content_tree.heading(
            "original",
            text=pgettext("vcf_generate_invalid_dialog.heading_original", "Original Content"),
            anchor="w",
        )
        self.content_tree.heading(
            "reason",
            text=pgettext("vcf_generate_invalid_dialog.heading_reason", "Reason"),
            anchor="w",
        )
        # 添加一个提示，告知用户正在加载中。
        self.content_tree.insert(
            "",
            "end",
            id="loading_tip",
            values=(
                "",
                pgettext("vcf_generate_invalid_dialog.cell_loading", "Loading..."),
                "",
            ),
        )
        self.content_tree.pack(fill="both", expand=True, padx="8.25p")

        self.content_tree.bind("<Double-Button-1>", self.window.on_tree_view_enter)
        self.content_tree.bind("<Return>", self.window.on_tree_view_enter)
        return content_frame

    @override
    def _create_footer(self, parent: Misc):
        footer_frame = Frame(parent)
        if needs_sizegrip(parent):
            sizegrip = Sizegrip(footer_frame)
            sizegrip.place(relx=1, rely=1, anchor="se")

        self.ok_button = Button(
            footer_frame,
            text=pgettext("common.button_ok", "OK"),
            default="active",
            command=lambda: self.window.event_generate(EVENT_EXIT),
        )
        self.ok_button.pack(side="right", padx="8.25p", pady="8.25p")
        return footer_frame
