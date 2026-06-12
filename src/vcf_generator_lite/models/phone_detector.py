from dataclasses import dataclass, replace
from re import Pattern

from vcf_generator_lite.models.lazy import LazyPgettext


@dataclass
class PhoneRule:
    length: range | int | set[int] | None
    """粗略长度检查，包含国际区号的总长度。

    - :class:`int`：固定长度，如 ``11`` 表示恰好 11 位。
    - :class:`set[int]`：多个可选长度，如 ``{11, 14}``` 匹配带/不带国际区号。
    - :class:`range`：长度范围，如 ``range(10, 16)`` 匹配 10~15 位（上限为开区间）。
    - :const:`None`：不限制长度，仅用正则匹配。
    """
    regex: Pattern[str]

    def test(self, phone: str) -> bool:
        phone_length = len(phone)
        if isinstance(self.length, int):
            if phone_length != self.length:
                return False
        elif self.length is not None and phone_length not in self.length:
            return False
        return self.regex.match(phone) is not None


@dataclass(frozen=True)
class PhoneDetector:
    id: str
    locale_territories: set[str]
    """ISO 3166-1 二位地区代码集合。一个检测器可适用于多个地区。"""
    name: LazyPgettext
    rules: list[PhoneRule]

    def __add__(self, other: "PhoneDetector") -> "PhoneDetector":
        """合并两个相同 ``id`` 的检测器。"""
        if self.id != other.id:
            raise ValueError(f"Id mismatch: {self.id} != {other.id}")
        return replace(
            self,
            locale_territories=self.locale_territories | other.locale_territories,
            rules=self.rules + other.rules,
        )
