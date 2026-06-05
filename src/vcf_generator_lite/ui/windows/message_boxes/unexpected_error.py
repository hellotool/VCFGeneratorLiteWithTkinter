from gettext import pgettext
from tkinter.messagebox import showerror


def show_unexpected_error_dialog(error: BaseException) -> None:
    showerror(
        title=pgettext("dialog_unexpected_error.title", "Unexpected Error"),
        message=pgettext(
            "dialog_unexpected_error.message",
            "An unexpected error occurred, please report this error to the maintainer.",
        ),
        detail=pgettext("dialog_unexpected_error.detail", "Error message: {error}").format(error=str(error)),
    )
