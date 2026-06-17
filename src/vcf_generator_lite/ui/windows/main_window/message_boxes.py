from tkinter import Misc, messagebox

from vcf_generator_lite.core.vcf_generator import GenerateResult
from vcf_generator_lite.ui.actions.external_app import pgettext


def show_save_file_os_error_dialog(parent: Misc, error: OSError):
    messagebox.showerror(
        parent=parent,
        title=pgettext("dialog_save_file_os_error.title", "Save Failed"),
        message=str(error),
    )


def show_save_file_permission_denied_dialog(parent: Misc):
    messagebox.showerror(
        parent=parent,
        title=pgettext("dialog_save_file_permission_denied.title", "Save Failed"),
        message=pgettext(
            "dialog_save_file_permission_denied.message", "Permission denied, please grant permission again."
        ),
    )


def show_generation_success_dialog(parent: Misc, display_path: str, generate_result: GenerateResult):
    messagebox.showinfo(
        parent=parent,
        title=pgettext("dialog_generate_success.title", "Generation Successful"),
        message=pgettext("dialog_generate_success.message", "File exported to {path}.").format(path=display_path),
        detail=pgettext(
            "dialog_generate_success.detail",
            """Count: {count:n}
Time elapsed: {time:.3f}s""",
        ).format(
            count=generate_result.saved_count,
            time=generate_result.time_elapsed,
        ),
    )


def show_no_phone_formats_selected_dialog(parent: Misc):
    messagebox.showinfo(
        parent=parent,
        title=pgettext("dialog_no_phone_formats_selected.title", "No Phone Formats Selected"),
        message=pgettext("dialog_no_phone_formats_selected.message", "Please select at least one phone format."),
    )
