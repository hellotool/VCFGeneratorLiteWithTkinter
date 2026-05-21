from typing import NamedTuple, override


class LazyPgettext(NamedTuple):
    """惰性翻译对象，持有翻译上下文和原文，供 Babel 提取和运行时翻译。"""

    context: str
    message: str

    @override
    def __str__(self) -> str:
        """直接转换为字符串时返回原文，保持向后兼容。"""
        return self.message
