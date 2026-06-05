import webbrowser
from gettext import pgettext
from tkinter import Misc, messagebox


def show_open_url_failure_message_box(parent: Misc, url: str):
    messagebox.showerror(
        parent=parent,
        title=pgettext("dialog_open_url_failure.title", "Failed to Open External Application"),
        message=pgettext(
            "dialog_open_url_failure.message",
            "Failed to open external application. Please check your default application settings.",
        ),
        detail=pgettext("dialog_open_url_failure.detail", "Link: {url}").format(url=url),
    )


def open_url(parent: Misc, url: str):
    result = webbrowser.open(url)
    if not result:
        show_open_url_failure_message_box(parent, url)
