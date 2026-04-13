from abc import ABC, abstractmethod


class ThemePatcher(ABC):
    @abstractmethod
    def patch(self): ...

    @abstractmethod
    def get_last_patched_theme(self) -> str | None: ...
