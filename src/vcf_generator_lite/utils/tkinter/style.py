from collections.abc import Iterable
from tkinter.font import Font, nametofont
from tkinter.ttk import Style
from typing import Any


def lookup_font(
    style_obj: Style,
    style_name: str,
    option: str,
    state: Iterable[str] | None = None,
    default: Any | None = None,  # noqa: ANN401
) -> Font:
    """Lookup font from style object and return Font object"""
    treeview_font_lookup = style_obj.lookup(
        style=style_name,
        option=option,
        state=state,
        default=default,
    )
    if isinstance(treeview_font_lookup, Font):
        return treeview_font_lookup
    return nametofont(str(treeview_font_lookup))
