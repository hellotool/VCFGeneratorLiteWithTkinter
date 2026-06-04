import urllib.parse
from abc import ABC, abstractmethod
from functools import partial
from gettext import pgettext
from tkinter import BooleanVar, Menu, Misc

from vcf_generator_lite.constants import (
    EMAIL_AUTHOR,
    URL_LICENSE,
    URL_RELEASES,
    URL_REPORT,
    URL_REPOSITORY,
)
from vcf_generator_lite.core.phone_format_loader import PhoneFormat
from vcf_generator_lite.ui.actions.external_app import open_url
from vcf_generator_lite.ui.app_text import app_name, third_party_notices_url
from vcf_generator_lite.ui.windows.main_window.constants import (
    ACCELERATOR_GENERATE,
    ACCELERATOR_GENERATE_AQUA,
)
from vcf_generator_lite.ui.windows.main_window.states import GenerationState
from vcf_generator_lite.utils.tkinter.accelerators import get_default_accelerators
from vcf_generator_lite.utils.tkinter.menu import pgettext_menu_label


class MainMenuBar(Menu):
    class Listener(ABC):
        """MainMenuBar listener interface"""

        @abstractmethod
        def on_generate(self): ...

        @abstractmethod
        def on_stop_generation(self): ...

        @abstractmethod
        def on_exit(self): ...

        @abstractmethod
        def on_clean_quotes(self): ...

        @abstractmethod
        def on_toggle_all_phone_formats(self): ...

        @abstractmethod
        def on_toggle_phone_format(self, format_id: str): ...

        @abstractmethod
        def on_about(self): ...

    def __init__(self, parent: Misc | None, phone_formats: list[PhoneFormat], listener: Listener):
        super().__init__(parent, tearoff=False, name="menubar")
        self.phone_formats = phone_formats
        self.listener = listener
        self.phone_formats_select_all_var = BooleanVar(value=False)
        self.phone_format_vars = {phone_format.id: BooleanVar(value=False) for phone_format in self.phone_formats}

        self.add_cascade(
            **pgettext_menu_label("main_window.menu_file", "&File"),
            menu=self._create_file_menu(self),
        )
        self.add_cascade(
            **pgettext_menu_label("main_window.menu_edit", "&Edit"),
            menu=self._create_edit_menu(self),
        )
        self.add_cascade(
            **pgettext_menu_label("main_window.menu_options", "&Options"),
            menu=self._create_options_menu(self),
        )
        self.add_cascade(
            **pgettext_menu_label("main_window.menu_help", "&Help"),
            menu=self._create_help_menu(self),
        )

    def _create_file_menu(self, master: Misc):
        self.file_menu = file_menu = Menu(master, tearoff=False)

        generate_parse_result = pgettext_menu_label("main_window.menu_file_generate", "&Generate file...")
        self.menu_generate_label = generate_parse_result["label"]
        file_menu.add_command(
            **generate_parse_result,
            command=self.listener.on_generate,
            accelerator=ACCELERATOR_GENERATE_AQUA if self._windowingsystem == "aqua" else ACCELERATOR_GENERATE,
        )

        stop_generation_parse_result = pgettext_menu_label("main_window.menu_file_stop_generation", "&Stop generation")
        self.menu_stop_generation_label = stop_generation_parse_result["label"]
        file_menu.add_command(
            **stop_generation_parse_result,
            command=self.listener.on_stop_generation,
            state="disabled",
        )

        file_menu.add_separator()
        # 通常不提供退出的快捷键
        # https://learn.microsoft.com/en-us/windows/win32/uxguide/cmd-menus
        file_menu.add_command(
            **pgettext_menu_label("main_window.menu_file_exit", "E&xit"),
            command=self.listener.on_exit,
        )
        return file_menu

    def _create_edit_menu(self, master: Misc):
        default_accelerators = get_default_accelerators(self.master)

        edit_menu = Menu(master, tearoff=False)
        edit_menu.add_command(
            **pgettext_menu_label("main_window.menu_edit_undo", "&Undo"),
            command=lambda: self._generate_focus_event("<<Undo>>"),
            accelerator=default_accelerators.undo,
        )
        edit_menu.add_command(
            **pgettext_menu_label("main_window.menu_edit_redo", "&Redo"),
            command=lambda: self._generate_focus_event("<<Redo>>"),
            accelerator=default_accelerators.redo,
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            **pgettext_menu_label("main_window.menu_edit_cut", "Cu&t"),
            command=lambda: self._generate_focus_event("<<Cut>>"),
            accelerator=default_accelerators.cut,
        )
        edit_menu.add_command(
            **pgettext_menu_label("main_window.menu_edit_copy", "&Copy"),
            command=lambda: self._generate_focus_event("<<Copy>>"),
            accelerator=default_accelerators.copy,
        )
        edit_menu.add_command(
            **pgettext_menu_label("main_window.menu_edit_paste", "&Paste"),
            command=lambda: self._generate_focus_event("<<Paste>>"),
            accelerator=default_accelerators.paste,
        )
        edit_menu.add_command(
            **pgettext_menu_label("main_window.menu_edit_select_all", "Select &All"),
            command=lambda: self._generate_focus_event("<<SelectAll>>"),
            accelerator=default_accelerators.select_all,
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            **pgettext_menu_label("main_window.menu_edit_clean_quotes", "Remove &Quotes"),
            command=self.listener.on_clean_quotes,
        )
        return edit_menu

    def _create_options_menu(self, master: Misc):
        options_menu = Menu(master, tearoff=False)
        phone_formats_menu = Menu(options_menu, tearoff=False)
        options_menu.add_cascade(
            **pgettext_menu_label("main_window.menu_phone_formats", "&Phone Formats"),
            menu=phone_formats_menu,
        )
        phone_formats_menu.add_checkbutton(
            **pgettext_menu_label("main_window.menu_select_all_phone_formats", "Select &All"),
            variable=self.phone_formats_select_all_var,
            command=self.listener.on_toggle_all_phone_formats,
        )
        phone_formats_menu.add_separator()

        for phone_format in self.phone_formats:
            phone_formats_menu.add_checkbutton(
                label=pgettext(phone_format.name.context, phone_format.name.message),
                variable=self.phone_format_vars[phone_format.id],
                command=partial(self.listener.on_toggle_phone_format, format_id=phone_format.id),
            )

        return options_menu

    def _create_help_menu(self, master: Misc):
        help_menu = Menu(master, tearoff=False, name="help")
        help_menu.add_command(
            **pgettext_menu_label("main_window.menu_help_repository", "Rep&ository"),
            command=lambda: open_url(self, URL_REPOSITORY),
        )
        help_menu.add_command(
            **pgettext_menu_label("main_window.menu_help_release", "&Releases"),
            command=lambda: open_url(self, URL_RELEASES),
        )
        help_menu.add_separator()
        help_menu.add_command(
            **pgettext_menu_label("main_window.menu_help_feedback", "&Feedback"),
            command=lambda: open_url(self, URL_REPORT),
        )
        help_menu.add_command(
            **pgettext_menu_label("main_window.menu_help_contact", "&Contact Author"),
            command=lambda: open_url(
                parent=self,
                url=urllib.parse.SplitResult(
                    scheme="mailto",
                    netloc="",
                    path=EMAIL_AUTHOR,
                    query="",
                    fragment="",
                ).geturl(),
            ),
        )
        help_menu.add_separator()
        help_menu.add_command(
            **pgettext_menu_label("main_window.menu_help_license", "&License"),
            command=lambda: open_url(self, URL_LICENSE),
        )
        help_menu.add_command(
            **pgettext_menu_label("main_window.menu_help_os_notices", "Open Source &Notices"),
            command=lambda: open_url(self, third_party_notices_url()),
        )
        help_menu.add_separator()
        help_parsed_label = pgettext_menu_label("main_window.menu_help_about", "&About {app_name}")
        help_parsed_label["label"] = help_parsed_label["label"].format(app_name=app_name())
        help_menu.add_command(
            **help_parsed_label,
            command=self.listener.on_about,
        )
        return help_menu

    def _generate_focus_event(self, sequence: str):
        if widget := self.focus_get():
            widget.event_generate(sequence)

    def set_generating_state(self, state: GenerationState):
        self.file_menu.entryconfigure(
            self.menu_generate_label,
            state="normal" if state is GenerationState.IDLE else "disabled",
        )
        self.file_menu.entryconfigure(
            self.menu_stop_generation_label,
            state="normal" if state is GenerationState.GENERATING else "disabled",
        )

    def set_phone_formats_selection(self, all_selected: bool, selection: dict[str, bool]):
        self.phone_formats_select_all_var.set(all_selected)
        for format_id, selected in selection.items():
            self.phone_format_vars[format_id].set(selected)
