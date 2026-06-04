from gettext import pgettext
from typing import TypedDict

UNDERLINE_MARKER = "&"


class ParsedLabel(TypedDict):
    label: str
    underline: int


def parse_menu_label(label: str) -> ParsedLabel:
    """解析标签字符串，将标签字符串中的快捷键标识符设置为对应的快捷键键值"""
    return ParsedLabel(
        label=label.replace(UNDERLINE_MARKER, "", 1),
        underline=label.find(UNDERLINE_MARKER),
    )


def pgettext_menu_label(context: str, message: str, /) -> ParsedLabel:
    """获取翻译后的字符串，并解析快捷键"""
    return parse_menu_label(pgettext(context, message))
