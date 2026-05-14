import locale
import os
from gettext import NullTranslations

from vcf_generator_lite.utils.i18n.zipapp_gettext import translation as translation_from_package
from vcf_generator_lite.utils.resources import traversable

__all__ = ["gettext", "pgettext"]

APP_DOMAIN = "vcf-generator-lite"


def _get_locales() -> list[str]:
    locales: list[str] = []
    # 不要使用 locale.getlocale() 因为 https://github.com/python/cpython/issues/130796。
    # getdefaultlocale 在 Python 3.15 中已取消弃用。
    default_language, default_encoding = locale.getdefaultlocale(envvars=("LANG",))
    if default_language == "C":
        locales.append("C")
        return locales

    language_env = os.environ.get("LANGUAGE")
    if language_env:
        # https://www.gnu.org/software/gettext/manual/html_node/The-LANGUAGE-variable.html
        locales.extend(locale for locale in language_env.split(":") if locale)

    if not locales:
        for env_var in ("LC_ALL", "LC_MESSAGES", "LC_CTYPE"):
            language_env = os.environ.get(env_var)
            if language_env:
                locales.append(language_env)
                break

    if default_language and default_encoding:
        locales.append(f"{default_language}.{default_encoding}")
    elif default_language:
        locales.append(default_language)
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
