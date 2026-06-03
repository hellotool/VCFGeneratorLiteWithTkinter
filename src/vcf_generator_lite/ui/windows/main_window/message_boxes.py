from tkinter import Misc, messagebox

from vcf_generator_lite.core.vcf_generator import GenerateResult
from vcf_generator_lite.ui.actions.external_app import pgettext


def show_save_file_os_error_dialog(parent: Misc, error: OSError):
    messagebox.showerror(
        parent=parent,
        title=pgettext("save_file_os_error_dialog.title", "Save Failed"),
        message=str(error),
    )


def show_save_file_permission_denied_dialog(parent: Misc):
    messagebox.showerror(
        parent=parent,
        title=pgettext("save_file_permission_denied_dialog.title", "Save Failed"),
        message=pgettext(
            "save_file_permission_denied_dialog.message", "Permission denied, please grant permission again."
        ),
    )


def show_generation_success_dialog(parent: Misc, display_path: str, generate_result: GenerateResult):
    messagebox.showinfo(
        parent=parent,
        title=pgettext("vcf_generate_success_msg_box.title", "Generation Successful"),
        message=pgettext("vcf_generate_success_msg_box.message", "File exported to {path}.").format(path=display_path),
        detail=pgettext(
            "vcf_generate_success_msg_box.detail",
            """Count: {count:n}
Time elapsed: {time:.3f}s""",
        ).format(
            count=generate_result.saved_count,
            time=generate_result.time_elapsed,
        ),
    )
