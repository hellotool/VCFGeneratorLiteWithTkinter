import platform
from gettext import pgettext
from tkinter import Misc, messagebox

from vcf_generator_lite.__version__ import __version__
from vcf_generator_lite.ui.app_text import app_copyright, app_description, app_name


def show_about_message_box(parent: Misc):

    messagebox.showinfo(
        parent=parent,
        title=pgettext("dialog_about.title", "About {app_name}").format(app_name=app_name()),
        message=pgettext("dialog_about.message", "{app_name} v{version}").format(
            app_name=app_name(),
            version=__version__,
        ),
        detail=pgettext(
            "dialog_about.detail",
            """{description}

{copyright}

Environment Information:
Python: {python_info}
Tcl/Tk: {tcltk_info}""",
        ).format(
            description=app_description(),
            copyright=app_copyright(),
            python_info=f"{platform.python_implementation()} {platform.python_version()}",
            tcltk_info=parent.info_patchlevel(),
        ),
    )
