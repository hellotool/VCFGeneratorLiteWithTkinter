from abc import ABC, abstractmethod
from gettext import pgettext
from tkinter import Misc
from tkinter.ttk import Button, Frame, Label, Progressbar, Sizegrip
from typing import override

from ttk_text.scrolled_text import ScrolledText

from vcf_generator_lite.ui.layouts.vertical_dialog_layout import VerticalDialogLayout
from vcf_generator_lite.ui.widgets.line_number_bar import LineNumberBar
from vcf_generator_lite.ui.widgets.text_menu import TextContextMenu
from vcf_generator_lite.ui.windows.main_window.states import GenerationState
from vcf_generator_lite.utils.tkinter.widget import enable_auto_wrap, needs_sizegrip


class MainLayout(VerticalDialogLayout):
    class Listener(ABC):
        """Main layout listener interface."""

        @abstractmethod
        def on_generate_or_stop(self): ...

    def __init__(self, parent: Misc, listener: Listener):
        super().__init__()
        self.listener = listener
        self._create_widgets(parent)

    @override
    def _create_header(self, parent: Misc):
        description_label = Label(
            parent,
            text=pgettext(
                "window_main.label_usage",
                """Instructions:
1. Copy names and phone numbers in the format "Name Phone Notes" (notes optional) into the edit box below.
2. Click "Generate" and select a path to save the file.
3. You can use the generated vCard file wherever you need it, such as importing it into your phone or email.""",
            ),
            justify="left",
        )
        enable_auto_wrap(description_label)
        description_label.pack(fill="x", padx="8.25p", pady="8.25p")
        return description_label

    @override
    def _create_content(self, parent: Misc):
        self.content_text = ScrolledText(
            parent,
            undo=True,
            tabs="2c",
            tabstyle="wordprocessor",
            maxundo=5,
            width=0,
            height=0,
        )
        self.content_text.insert(
            0.0,
            pgettext(
                "window_main.entry_content",
                """Qu Yuan\t13333333333\tPoet of the Warring States period
Cao Cao\t13444444444
Tao Y.M.\t13555555555
Xie Lingyun\t13666666666
""",
            ),
        )
        self.content_text.edit_reset()
        self.content_text.pack(fill="both", expand=True, padx="8.25p", pady=0)

        self.line_numbers = LineNumberBar(self.content_text.frame)
        self.line_numbers.bind_text(self.content_text.text_proxy())
        self.line_numbers.grid(row=1, column=0, sticky="ns")
        self.__update_line_numbers_padding()
        self.content_text.frame.bind_widget(self.line_numbers, penetration_state=True)
        self.content_text.bind("<<ThemeChanged>>", lambda _: self.__update_line_numbers_padding(), "+")

        text_context_menu = TextContextMenu(self.content_text)
        text_context_menu.bind_to_widget()
        return self.content_text

    def __update_line_numbers_padding(self):
        self.line_numbers.grid(pady=self.content_text.text_proxy().grid_info().get("pady", None))

    @override
    def _create_footer(self, parent: Misc):
        footer_frame = Frame(parent)
        if needs_sizegrip(parent):
            sizegrip = Sizegrip(footer_frame)
            sizegrip.place(relx=1, rely=1, anchor="se")

        self.progress_bar = Progressbar(footer_frame, orient="horizontal", length=200, mode="determinate", maximum=1)
        self.progress_label = Label(master=footer_frame, text=pgettext("window_main.label_generating", "Generating..."))

        self.generate_or_stop_button = Button(
            footer_frame,
            text=pgettext("window_main.button_generate", "Generate"),
            default="active",
            command=self.listener.on_generate_or_stop,
        )
        self.generate_or_stop_button.pack(side="right", padx="8.25p", pady="8.25p")
        return footer_frame

    def set_text_content(self, content: str):
        self.content_text.replace(1.0, "end", content)

    def get_text_content(self) -> str:
        return self.content_text.get(1.0, "end")[:-1]

    def show_progress(self):
        self.progress_bar.pack(side="left", padx="8.25p", pady="8.25p")
        self.progress_label.pack(side="left", padx=(0, "8.25p"), pady="8.25p")

    def hide_progress(self):
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()

    def set_progress(self, progress: float):
        self.progress_bar.configure(value=progress)

    def set_progress_determinate(self, value: bool):
        # 需要添加 str()，因为 https://github.com/python/cpython/issues/126008
        previous_value: bool = str(self.progress_bar.cget("mode")) == "determinate"
        if value == previous_value:
            return
        if value:
            self.progress_bar.configure(mode="determinate", maximum=1)
            self.progress_bar.stop()
        else:
            self.progress_bar.configure(mode="indeterminate", maximum=10)
            self.progress_bar.start()

    def set_generating(self, state: GenerationState):
        if state is GenerationState.IDLE:
            self.generate_or_stop_button.configure(
                text=pgettext("window_main.button_generate", "Generate"), state="normal"
            )
            self.hide_progress()
        elif state is GenerationState.GENERATING:
            self.generate_or_stop_button.configure(text=pgettext("window_main.button_stop", "Stop"), state="normal")
            self.progress_label.configure(text=pgettext("window_main.label_generating", "Generating..."))
            self.show_progress()
        elif state is GenerationState.STOPPING:
            self.generate_or_stop_button.configure(text=pgettext("window_main.button_stop", "Stop"), state="disabled")
            self.progress_label.configure(text=pgettext("window_main.label_stopping", "Stopping..."))
            self.show_progress()
            self.set_progress_determinate(False)
