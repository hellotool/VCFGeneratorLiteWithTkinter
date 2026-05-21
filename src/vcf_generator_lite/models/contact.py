from typing import NamedTuple


class MissingNumberError(ValueError):
    def __init__(self) -> None:
        super().__init__("Missing number or number is incorrect.")


class Contact(NamedTuple):
    phone: str
    name: str | None = None
    note: str | None = None
