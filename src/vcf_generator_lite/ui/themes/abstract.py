from abc import ABC, abstractmethod


class ThemePatcher(ABC):
    @abstractmethod
    def patch(self): ...
