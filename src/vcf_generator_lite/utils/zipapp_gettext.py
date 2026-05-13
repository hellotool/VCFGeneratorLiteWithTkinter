import locale
import re
from collections.abc import Callable, Iterable
from copy import copy
from functools import cache
from gettext import GNUTranslations, NullTranslations
from importlib.resources.abc import Traversable
from io import Reader
from itertools import chain

__all__ = ["find", "translation"]

COMPONENT_CODESET = 1 << 0
COMPONENT_COUNTRY = 1 << 1
COMPONENT_MODIFIER = 1 << 2

LOCALE_REGEX = re.compile(r"^([^@._]+)(_[^@._]+)?(\.[^@]+)?(@.+)?$")
"""
以 `language_country.codeset@modifier` 格式解析
"""


def _expand_lang(loc: str) -> list[str]:
    """
    Expand a locale string into all possible combinations of language, territory, codeset, and modifier.

    Modified from ``gettext._expand_lang``.
    """
    loc_match = LOCALE_REGEX.match(locale.normalize(loc))
    if loc_match is None:
        return []
    language, country, codeset, modifier = loc_match.groups("")

    mask = 0
    if modifier:
        mask |= COMPONENT_MODIFIER
    if country:
        mask |= COMPONENT_COUNTRY
    if codeset:
        mask |= COMPONENT_CODESET
    ret: list[str] = []
    for i in range(mask + 1):
        if not (i & ~mask):
            val = language
            if i & COMPONENT_COUNTRY:
                val += country
            if i & COMPONENT_CODESET:
                val += codeset
            if i & COMPONENT_MODIFIER:
                val += modifier
            ret.append(val)
    ret.reverse()
    return ret


def find(domain: str, localedir: Traversable, languages: Iterable[str]) -> list[Traversable]:
    """
    Find all translation files for a given domain from a Traversable.

    Modified from ``gettext.find``.
    """
    nelangs: list[str] = []

    for nelang in chain.from_iterable(_expand_lang(lang) for lang in languages):
        if nelang not in nelangs:
            nelangs.append(nelang)

    result: list[Traversable] = []
    for lang in nelangs:
        mofile: Traversable = localedir.joinpath(lang, "LC_MESSAGES", f"{domain}.mo")
        if mofile.is_file():
            result.append(mofile)
    return result


@cache
def _get_translation(class_: Callable[[Reader[bytes]], NullTranslations], mo_file: Traversable) -> NullTranslations:
    with mo_file.open(mode="rb") as io:
        return class_(io)


def translation(
    domain: str,
    localedir: Traversable,
    *,
    languages: Iterable[str],
    class_: Callable[[Reader[bytes]], NullTranslations] | None = None,
) -> NullTranslations:
    """
    Acquire a translation object from a Traversable.

    Modified from ``gettext.translation``.
    """
    if class_ is None:
        class_ = GNUTranslations
    files: list[Traversable] = find(domain, localedir, languages)
    if not files:
        return NullTranslations()

    translations = (copy(_get_translation(class_, file)) for file in files)
    result = next(translations)
    for translation in translations:
        result.add_fallback(translation)
    return result
