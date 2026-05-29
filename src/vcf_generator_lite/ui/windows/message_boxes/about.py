import platform
import tkinter
from tkinter import Misc, messagebox

from vcf_generator_lite.__version__ import __version__
from vcf_generator_lite.constants import APP_COPYRIGHT
from vcf_generator_lite.ui.actions.external_app import pgettext


def show_about_message_box(parent: Misc):
    messagebox.showinfo(
        parent=parent,
        title=pgettext("about_message_box.title", "About VCF Generator Lite"),
        message=pgettext("about_message_box.message", "VCF Generator Lite v{version}").format(
            version=__version__,
        ),
        detail=pgettext(
            "about_message_box.detail",
            """{copyright}

Environment Information:
Python: {python_info}
Tcl: {tcl_info}
Tk: {tk_info}""",
        ).format(
            copyright=APP_COPYRIGHT,
            python_info=f"{platform.python_implementation()} v{platform.python_version()}",
            tcl_info=f"v{tkinter.TclVersion}",
            tk_info=f"v{tkinter.TkVersion}",
        ),
    )
