from tkinter import Misc
from tkinter.font import Font, nametofont


def extend_font_scale(scale: float, origin_name: str | Font = "TkDefaultFont", root: Misc | None = None):
    font = copy_font(origin_name, root=root)
    font.configure(size=round(int(font["size"]) * scale))
    return font


def copy_font(origin_name: str | Font, new_name: str | None = None, root: Misc | None = None) -> Font:
    """使用原始配置复制字体。

    原始 `font#copy()` 是有问题的，因为其内部会调用`font#actual()`，这是错误的。

    在 Linux 中，`font#actual("size")` 会返回缩放后的字体大小，
    再次传入字体对象时会造成双倍缩放，使用此方法规避该问题。
    """
    origin_font = nametofont(origin_name, root=root) if isinstance(origin_name, str) else origin_name
    return Font(root, name=new_name, **origin_font.config())  # pyright: ignore[reportCallIssue]
