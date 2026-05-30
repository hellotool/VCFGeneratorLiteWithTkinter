import logging
from ctypes import FormatError, get_last_error, windll

logger = logging.getLogger(__name__)

# ProcessDpiAwareness
# https://learn.microsoft.com/zh-cn/windows/win32/api/shellscalingapi/ne-shellscalingapi-process_dpi_awareness
PROCESS_SYSTEM_DPI_AWARE = 1


def _try_set_process_dpi_awareness() -> bool:
    """
    Windows 8.1 及以上可用。

    `setProcessDpiAwareness 函数 (shellscalingapi.h) <https://learn.microsoft.com/zh-cn/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness>`_。
    """
    if not hasattr(windll.shcore, "SetProcessDpiAwareness"):
        return False
    result: int = windll.shcore.SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
    if result != 0:
        logger.warning("Failed to call SetProcessDpiAwareness: %s", FormatError(result))
    return result == 0


def _try_set_process_dpi_aware() -> bool:
    """
    Windows Vista 及以上可用。

    `setProcessDPIAware 函数 (winuser.h) <https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-setprocessdpiaware>`_。
    """
    if not hasattr(windll.user32, "SetProcessDPIAware"):
        return False
    result = bool(windll.user32.SetProcessDPIAware())
    if not result:
        logger.warning("Failed to call SetProcessDPIAware: %s", FormatError(get_last_error()))
    return result


def enable_dpi_aware() -> bool:
    if _try_set_process_dpi_awareness():
        return True
    return _try_set_process_dpi_aware()
