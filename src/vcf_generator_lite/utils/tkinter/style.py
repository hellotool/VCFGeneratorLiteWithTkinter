import tkinter
from collections.abc import Iterable
from tkinter.font import Font, nametofont
from tkinter.ttk import Style
from typing import Any


def lookup_font(
    style_obj: Style,
    style_name: str,
    option: str,
    state: Iterable[str] | None = None,
    default: Any | None = None,  # ruff: ignore[any-type]
) -> Font:
    """Lookup font from style object and return Font object.

    主题可能以两种形式配置样式字体：

    - 命名字体名（如 ``TkDefaultFont``）：直接引用该命名字体；
    - 字体描述串（如 breeze 主题的 ``Helvetica 10``）：构造临时 Font 解析。
      :meth:`Font.__init__` 会先尝试 ``font configure``（仅命名字体可成功），
      失败后回退 ``font actual`` 解析描述串。
    """
    font_lookup = style_obj.lookup(style=style_name, option=option, state=state, default=default)
    if isinstance(font_lookup, Font):
        return font_lookup
    name = str(font_lookup)
    try:
        return nametofont(name)
    except tkinter.TclError:
        return Font(font=name)
