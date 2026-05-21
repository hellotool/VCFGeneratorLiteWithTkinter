from typing import NamedTuple, override


class LazyPgettext(NamedTuple):
    """惰性翻译对象。必须按位置参数调用：LazyPgettext(context, message)。"""

    context: str
    message: str

    @override
    def __str__(self) -> str:
        return self.message
