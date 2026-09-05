import io
from gettext import GNUTranslations, NullTranslations
from importlib.resources.abc import Traversable
import locale
from typing import IO
from unittest.mock import MagicMock, patch

import pytest

from vcf_generator_lite.utils.i18n.zipapp_gettext import (
    _expand_lang,
    _expanded_langs,
    _get_or_create_translation,
    find,
    get_default_locales,
    translation,
)


def normalize(loc: str):
    return loc


@pytest.fixture(autouse=True)
def mock_locale_normalize(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(locale, "normalize", normalize)


class TestExpandLang:
    def test_language_only(self):
        result = list(_expand_lang("xx"))
        assert result == ["xx"]

    def test_language_and_territory(self):
        result = list(_expand_lang("xx_XX"))
        assert result == ["xx_XX", "xx"]

    def test_language_territory_codeset(self):
        result = list(_expand_lang("xx_XX.UTF-8"))
        assert result == ["xx_XX.UTF-8", "xx_XX", "xx.UTF-8", "xx"]

    def test_language_territory_modifier(self):
        result = list(_expand_lang("xx_XX@collation=pinyin"))
        assert result == ["xx_XX@collation=pinyin", "xx@collation=pinyin", "xx_XX", "xx"]

    def test_language_codeset(self):
        result = list(_expand_lang("xx.UTF-8"))
        assert result == ["xx.UTF-8", "xx"]

    def test_language_modifier(self):
        result = list(_expand_lang("xx@collation=pinyin"))
        assert result == ["xx@collation=pinyin", "xx"]

    def test_full_locale(self):
        result = list(_expand_lang("xx_XX.UTF-8@collation=pinyin"))
        expected = [
            "xx_XX.UTF-8@collation=pinyin",
            "xx_XX@collation=pinyin",
            "xx.UTF-8@collation=pinyin",
            "xx@collation=pinyin",
            "xx_XX.UTF-8",
            "xx_XX",
            "xx.UTF-8",
            "xx",
        ]
        assert result == expected

    def test_invalid_locale_returns_none(self):
        result = list(_expand_lang(""))
        assert result == []

    def test_c_locale(self):
        result = list(_expand_lang("C"))
        assert result == ["C"]

    def test_en_us(self):
        result = list(_expand_lang("en_US"))
        assert result == ["en_US", "en"]


class TestExpandedLangs:
    def test_single_language(self):
        result = list(_expanded_langs(["xx_XX"]))
        assert result == ["xx_XX", "xx"]

    def test_multiple_languages(self):
        result = list(_expanded_langs(["xx_XX", "yy_YY"]))
        assert result == ["xx_XX", "xx", "yy_YY", "yy"]

    def test_deduplication(self):
        result = list(_expanded_langs(["xx_XX", "xx"]))
        assert result == ["xx_XX", "xx"]

    def test_c_locale_breaks(self):
        result = list(_expanded_langs(["C", "xx_XX"]))
        assert result == []

    def test_c_locale_in_middle(self):
        result = list(_expanded_langs(["xx_XX", "C", "yy_YY"]))
        assert result == ["xx_XX", "xx"]

    def test_empty_string_skipped(self):
        result = list(_expanded_langs(["xx_XX", "", "yy_YY"]))
        assert result == ["xx_XX", "xx", "yy_YY", "yy"]

    def test_empty_iterable(self):
        result = list(_expanded_langs([]))
        assert result == []


class TestGetDefaultLocales:
    def test_language_env_var(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("LANGUAGE", "xx_XX:yy_YY:zz")
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        with patch("locale.getdefaultlocale", return_value=(None, None)):
            result = list(get_default_locales())
        assert result == ["xx_XX", "yy_YY", "zz"]

    def test_lc_all_env_var(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("LANGUAGE", raising=False)
        monkeypatch.setenv("LC_ALL", "xx_XX.UTF-8")
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        result = list(get_default_locales())
        assert result == ["xx_XX.UTF-8"]

    def test_lc_messages_env_var(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("LANGUAGE", raising=False)
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.setenv("LC_MESSAGES", "xx_XX.UTF-8")
        monkeypatch.delenv("LANG", raising=False)
        result = list(get_default_locales())
        assert result == ["xx_XX.UTF-8"]

    def test_lc_ctype_env_var(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("LANGUAGE", raising=False)
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.setenv("LC_CTYPE", "xx_XX.UTF-8")
        monkeypatch.delenv("LANG", raising=False)
        result = list(get_default_locales())
        assert result == ["xx_XX.UTF-8"]

    def test_lc_vars_priority(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("LANGUAGE", raising=False)
        monkeypatch.setenv("LC_ALL", "aa_AA.UTF-8")
        monkeypatch.setenv("LC_MESSAGES", "xx_XX.UTF-8")
        monkeypatch.delenv("LANG", raising=False)
        result = list(get_default_locales())
        assert result == ["aa_AA.UTF-8"]

    def test_no_env_vars(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("LANGUAGE", raising=False)
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.delenv("LC_CTYPE", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        with patch("locale.getdefaultlocale", return_value=(None, None)):
            result = list(get_default_locales())
        assert result == []

    def test_language_env_with_empty_parts(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("LANGUAGE", "xx_XX::yy_YY")
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        with patch("locale.getdefaultlocale", return_value=(None, None)):
            result = list(get_default_locales())
        assert result == ["xx_XX", "yy_YY"]


class TestFind:
    def _make_traversable(self, existing_files: set[str]) -> Traversable:
        root = MagicMock(spec=Traversable)

        def joinpath(*args: str) -> MagicMock:
            mock = MagicMock(spec=Traversable)
            path = "/".join(args)
            mock.is_file.return_value = path in existing_files
            return mock

        root.joinpath.side_effect = joinpath
        return root

    def test_find_existing_translation(self):
        localedir = self._make_traversable({"xx_XX/LC_MESSAGES/test.mo"})
        result = list(find("test", localedir, ["xx_XX"]))
        assert len(result) == 1

    def test_find_fallback_to_language_only(self):
        localedir = self._make_traversable({"xx/LC_MESSAGES/test.mo"})
        result = list(find("test", localedir, ["xx_XX"]))
        assert len(result) == 1

    def test_find_not_found(self):
        localedir = self._make_traversable(set())
        result = list(find("test", localedir, ["xx_XX"]))
        assert len(result) == 0

    def test_find_multiple_languages(self):
        localedir = self._make_traversable(
            {
                "xx_XX/LC_MESSAGES/test.mo",
                "yy_YY/LC_MESSAGES/test.mo",
            }
        )
        result = list(find("test", localedir, ["xx_XX", "yy_YY"]))
        assert len(result) == 2

    def test_find_uses_default_locales_when_none(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("LANGUAGE", "xx_XX")
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        localedir = self._make_traversable({"xx_XX/LC_MESSAGES/test.mo"})
        result = list(find("test", localedir))
        assert len(result) == 1

    def test_find_c_locale_skipped(self):
        localedir = self._make_traversable({"xx_XX/LC_MESSAGES/test.mo"})
        result = list(find("test", localedir, ["C", "xx_XX"]))
        assert len(result) == 0


class TestGetOrCreateTranslation:
    def test_creates_translation(self):
        mo_data = self._make_minimal_mo()
        mo_file = self._make_mo_traversable(mo_data)

        result = _get_or_create_translation(GNUTranslations, mo_file)
        assert isinstance(result, GNUTranslations)

    def test_caches_result(self):
        mo_data = self._make_minimal_mo()
        mo_file = self._make_mo_traversable(mo_data)

        _get_or_create_translation.cache_clear()
        result1 = _get_or_create_translation(GNUTranslations, mo_file)
        result2 = _get_or_create_translation(GNUTranslations, mo_file)
        assert result1 is result2

    @staticmethod
    def _make_minimal_mo() -> bytes:
        buf = io.BytesIO()
        buf.write(b"\xde\x12\x04\x95")
        buf.write(b"\x00" * 24)
        return buf.getvalue()

    @staticmethod
    def _make_mo_traversable(data: bytes) -> Traversable:
        mock = MagicMock(spec=Traversable)

        def open_(*, mode: str = "r") -> IO[bytes]:
            return io.BytesIO(data)

        mock.open.side_effect = open_
        return mock


class TestTranslation:
    def _make_traversable(self, existing_files: dict[str, bytes]) -> Traversable:
        root = MagicMock(spec=Traversable)

        def joinpath(*args: str) -> MagicMock:
            mock = MagicMock(spec=Traversable)
            path = "/".join(args)
            data = existing_files.get(path)
            if data is not None:
                mock.is_file.return_value = True

                def open_(*, mode: str = "r") -> IO[bytes]:
                    return io.BytesIO(data)

                mock.open.side_effect = open_
            else:
                mock.is_file.return_value = False
            return mock

        root.joinpath.side_effect = joinpath
        return root

    @staticmethod
    def _make_minimal_mo() -> bytes:
        buf = io.BytesIO()
        buf.write(b"\xde\x12\x04\x95")
        buf.write(b"\x00" * 24)
        return buf.getvalue()

    def test_returns_null_translations_when_no_file(self):
        localedir = self._make_traversable({})
        _get_or_create_translation.cache_clear()
        result = translation("test", localedir, languages=["xx_XX"])
        assert isinstance(result, NullTranslations)
        assert not isinstance(result, GNUTranslations)

    def test_returns_translation_when_file_exists(self):
        mo_data = self._make_minimal_mo()
        localedir = self._make_traversable({"xx_XX/LC_MESSAGES/test.mo": mo_data})
        _get_or_create_translation.cache_clear()
        result = translation("test", localedir, languages=["xx_XX"])
        assert isinstance(result, GNUTranslations)

    def test_fallback_chain(self):
        mo_data = self._make_minimal_mo()
        localedir = self._make_traversable(
            {
                "xx_XX/LC_MESSAGES/test.mo": mo_data,
                "yy/LC_MESSAGES/test.mo": mo_data,
            }
        )
        _get_or_create_translation.cache_clear()
        result = translation("test", localedir, languages=["xx_XX", "yy"])
        assert isinstance(result, GNUTranslations)
        assert result._fallback is not None  # pyright: ignore[reportAttributeAccessIssue]

    def test_uses_default_locales_when_none(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("LANGUAGE", "xx_XX")
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_MESSAGES", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        mo_data = self._make_minimal_mo()
        localedir = self._make_traversable({"xx_XX/LC_MESSAGES/test.mo": mo_data})
        _get_or_create_translation.cache_clear()
        result = translation("test", localedir)
        assert isinstance(result, GNUTranslations)

    def test_custom_class(self):
        mo_data = self._make_minimal_mo()
        localedir = self._make_traversable({"xx_XX/LC_MESSAGES/test.mo": mo_data})
        _get_or_create_translation.cache_clear()

        class CustomTranslations(GNUTranslations):
            pass

        result = translation("test", localedir, languages=["xx_XX"], class_=CustomTranslations)
        assert isinstance(result, CustomTranslations)
