import locale
import logging
import os
import re
from collections.abc import Callable, Iterable
from copy import copy
from functools import cache
from gettext import GNUTranslations, NullTranslations
from importlib.resources.abc import Traversable
from itertools import chain
from typing import IO

__all__ = ["find", "get_default_locales", "translation"]

COMPONENT_CODESET = 1 << 0
COMPONENT_TERRITORY = 1 << 1
COMPONENT_MODIFIER = 1 << 2

LOCALE_REGEX = re.compile(r"^([^@._]+)(_[^@._]+)?(\.[^@]+)?(@.+)?$")
"""
以 `language_territory.codeset@modifier` 格式解析
"""

SAFE_LOCALE_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z0-9@._\-]*$")

_logger = logging.getLogger(__name__)


def check_safe_locale(locale_str: str) -> bool:
    """Check if a locale string is safe."""
    return SAFE_LOCALE_REGEX.match(locale_str) is not None


def _expand_lang(loc: str) -> Iterable[str]:
    """
    Expand a locale string into all possible combinations of language, territory, codeset, and modifier.

    Modified from ``gettext._expand_lang``.
    """
    loc_match = LOCALE_REGEX.match(locale.normalize(loc))
    if loc_match is None:
        return
    language, territory, codeset, modifier = loc_match.groups("")

    mask = 0
    if modifier:
        mask |= COMPONENT_MODIFIER
    if territory:
        mask |= COMPONENT_TERRITORY
    if codeset:
        mask |= COMPONENT_CODESET
    for i in range(mask, -1, -1):
        if not (i & ~mask):
            val = language
            if i & COMPONENT_TERRITORY:
                val += territory
            if i & COMPONENT_CODESET:
                val += codeset
            if i & COMPONENT_MODIFIER:
                val += modifier
            yield val


def _expanded_langs(languages: Iterable[str]) -> Iterable[str]:
    yielded_langs: set[str] = set()
    for lang in chain.from_iterable(_expand_lang(lang) for lang in languages):
        if lang == "C":
            break
        if lang and (lang not in yielded_langs):
            yielded_langs.add(lang)
            yield lang


def get_default_locales() -> Iterable[str]:
    language_value = os.environ.get("LANGUAGE")
    if language_value:
        # https://www.gnu.org/software/gettext/manual/html_node/The-LANGUAGE-variable.html
        yield from (loc for loc in language_value.split(":") if loc)

    for env_var in ("LC_ALL", "LC_MESSAGES", "LC_CTYPE"):
        value = os.environ.get(env_var)
        if value:
            yield value
            return
    # 此处不要使用 locale.getlocale() 因为 https://github.com/python/cpython/issues/130796。
    # getdefaultlocale 是在 Windows 中获取 ISO 语言代码的唯一方法。
    # 此函数在 Python 3.15 中已取消弃用。
    default_language, default_encoding = locale.getdefaultlocale(envvars=("LANG",))
    if default_language:
        yield f"{default_language}.{default_encoding}" if default_encoding else default_language


def get_locale_territories(locales: Iterable[str]) -> Iterable[str]:
    for locale_match in (LOCALE_REGEX.match(locale.normalize(locale_)) for locale_ in locales):
        if locale_match:
            _, territory, _, _ = locale_match.groups("")
            if territory:
                yield territory.removeprefix("_")


def find(domain: str, localedir: Traversable, languages: Iterable[str] | None = None) -> Iterable[Traversable]:
    """
    Find all translation files for a given domain from a Traversable.

    Modified from ``gettext.find``.
    """
    if languages is None:
        languages = get_default_locales()
    for lang in _expanded_langs(languages):
        if not check_safe_locale(lang):
            _logger.warning("Unsafe locale string: %s, skipping.", lang)
            continue
        mofile: Traversable = localedir.joinpath(lang, "LC_MESSAGES", f"{domain}.mo")
        if mofile.is_file():
            yield mofile


@cache
def _get_or_create_translation(
    class_: Callable[[IO[bytes]], NullTranslations],
    mo_file: Traversable,
) -> NullTranslations:
    with mo_file.open(mode="rb") as io:
        return class_(io)


def translation(
    domain: str,
    localedir: Traversable,
    *,
    languages: Iterable[str] | None = None,
    class_: Callable[[IO[bytes]], NullTranslations] | None = None,
) -> NullTranslations:
    """
    Acquire a translation object from a Traversable.

    Modified from ``gettext.translation``.
    """
    if class_ is None:
        class_ = GNUTranslations
    files = find(domain, localedir, languages)
    translations = (copy(_get_or_create_translation(class_, file)) for file in files)
    try:
        result = next(translations)
    except StopIteration:
        return NullTranslations()
    for translation in translations:
        result.add_fallback(translation)
    return result
