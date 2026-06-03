from gettext import pgettext
from tkinter.messagebox import showerror


def show_unexpected_error_dialog(error: BaseException) -> None:
    showerror(
        title=pgettext("unexpected_error_dialog.title", "Unexpected Error"),
        message=pgettext(
            "unexpected_error_dialog.message",
            "An unexpected error occurred, please report this error to the maintainer.",
        ),
        detail=pgettext("unexpected_error_dialog.detail", "Error message: {error}").format(error=str(error)),
    )
