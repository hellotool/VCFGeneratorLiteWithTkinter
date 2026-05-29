import traceback
from tkinter import Misc, messagebox

from vcf_generator_lite.core.vcf_generator import GenerateResult
from vcf_generator_lite.ui.actions.external_app import pgettext


def show_save_os_error_message(parent: Misc, error: OSError):
    messagebox.showerror(
        parent=parent,
        title=pgettext("save_vcf_os_error_message_box.title", "Save Failed"),
        message=pgettext("save_vcf_os_error_message_box.message", "System error: {reason}").format(reason=str(error)),
    )


def show_save_permission_denied_message(parent: Misc):
    messagebox.showerror(
        parent=parent,
        title=pgettext("save_vcf_permission_denied_message_box.title", "Save Failed"),
        message=pgettext(
            "save_vcf_permission_denied_message_box.message", "Permission denied, please grant permission again."
        ),
    )


def show_generation_error_dialog(parent: Misc, exception: BaseException):
    messagebox.showerror(
        parent=parent,
        title=pgettext("vcf_generate_error_message_box.title", "Failed to Generate vCard File"),
        message=pgettext(
            "vcf_generate_error_message_box.message",
            "An unknown error occurred while generating the vCard file:\n\n{exception}",
        ).format(
            exception="\n".join(traceback.format_exception(exception)),
        ),
    )


def show_generation_success_dialog(parent: Misc, display_path: str, generate_result: GenerateResult):
    messagebox.showinfo(
        parent=parent,
        title=pgettext("vcf_generate_success_message_box.title", "vCard File Generated Successfully"),
        message=pgettext("vcf_generate_success_message_box.message", "File exported to {path}.").format(
            path=display_path
        ),
        detail=pgettext(
            "vcf_generate_success_message_box.detail",
            """Number of contacts: {count:n}
Time elapsed: {time:.3f} seconds""",
        ).format(
            count=generate_result.saved_count,
            time=generate_result.time_elapsed,
        ),
    )
