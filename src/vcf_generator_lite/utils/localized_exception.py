from abc import ABC, abstractmethod


class LocalizedException(BaseException, ABC):
    @property
    @abstractmethod
    def localized_msg(self) -> str: ...


def get_localized_exception_msg(exception: BaseException):
    if isinstance(exception, LocalizedException):
        return exception.localized_msg
    return str(exception)
