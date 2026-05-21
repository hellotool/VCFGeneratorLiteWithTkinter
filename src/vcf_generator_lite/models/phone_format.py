from dataclasses import dataclass, replace
from re import Pattern

from vcf_generator_lite.models.lazy import LazyPgettext


@dataclass
class PhoneRule:
    length: range | int | list[int] | None
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
class CountryPhoneFormat:
    id: str
    locale_territories: set[str]
    name: LazyPgettext
    rules: list[PhoneRule]

    def __add__(self, other: "CountryPhoneFormat") -> "CountryPhoneFormat":
        """Merge two CountryPhoneFormat instances"""
        if self.id != other.id:
            raise ValueError(f"Id mismatch: {self.id} != {other.id}")
        return replace(
            self,
            locale_territories=self.locale_territories | other.locale_territories,
            rules=self.rules + other.rules,
        )
