import locale
from gettext import NullTranslations

from vcf_generator_lite.utils.i18n.zipapp_gettext import translation as translation_from_package
from vcf_generator_lite.utils.resources import traversable

__all__ = ["gettext", "pgettext"]

APP_DOMAIN = "vcf-generator-lite"


def _get_locales() -> list[str]:
    locales: list[str] = []
    # 不要使用 locale.getlocale() 因为 https://github.com/python/cpython/issues/130796。
    # getdefaultlocale 在 Python 3.15 中已取消弃用。
    language, encoding = locale.getdefaultlocale()
    if language and encoding:
        locales.append(f"{language}.{encoding}")
    elif language:
        locales.append(language)
    return locales


_translation: NullTranslations = translation_from_package(
    domain=APP_DOMAIN,
    localedir=traversable.joinpath("locales"),
    languages=_get_locales(),
)


def gettext(message: str) -> str:
    return _translation.gettext(message)


def pgettext(context: str, message: str) -> str:
    return _translation.pgettext(context, message)
