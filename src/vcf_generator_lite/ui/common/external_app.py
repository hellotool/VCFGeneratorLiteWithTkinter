import webbrowser
from tkinter import Misc, messagebox

from vcf_generator_lite.utils.i18n.app_l10n import pgettext


def show_open_url_failure_message_box(parent: Misc, url: str):
    messagebox.showerror(
        parent=parent,
        title=pgettext("open_url_failure_message_box.title", "Failed to Open External Application"),
        message=pgettext(
            "open_url_failure_message_box.message",
            "Failed to open external application. Please check your default application settings.",
        ),
        detail=pgettext("open_url_failure_message_box.detail", "Link: {url}").format(url=url),
    )


def open_url_with_fallback(parent: Misc, url: str):
    result = webbrowser.open(url)
    if not result:
        show_open_url_failure_message_box(parent, url)
