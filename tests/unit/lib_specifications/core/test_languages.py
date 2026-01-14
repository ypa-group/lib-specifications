"""Tests for languages module."""

import pytest

from lib_specifications.core.languages import (
    Language,
    LanguageEnum,
    get_language_by_id,
    get_language_list,
)


@pytest.mark.unit
class TestLanguageEnum:
    """Tests for LanguageEnum."""

    def test_language_enum_values(self):
        """Test that all expected language enum values exist."""
        assert LanguageEnum.ENGLISH == "en"
        assert LanguageEnum.RUSSIAN == "ru"
        assert LanguageEnum.FRENCH == "fr"
        assert LanguageEnum.SPANISH == "es"
        assert LanguageEnum.ARABIC == "ar"
        assert LanguageEnum.HEBREW == "he"
        assert LanguageEnum.POLISH == "pl"
        assert LanguageEnum.PORTUGUESE == "pt"
        assert LanguageEnum.UKRAINIAN == "uk"
        assert LanguageEnum.CHINESE == "zh"

    def test_get_translations_structure(self):
        """Test that get_translations returns correct structure."""
        translations = LanguageEnum.ENGLISH.get_translations()
        assert isinstance(translations, dict)
        assert LanguageEnum.ENGLISH in translations
        assert LanguageEnum.RUSSIAN in translations
        assert LanguageEnum.FRENCH in translations

    def test_get_translations_content(self):
        """Test that translations contain expected values."""
        translations = LanguageEnum.ENGLISH.get_translations()
        english_translations = translations[LanguageEnum.ENGLISH]
        assert english_translations[LanguageEnum.ENGLISH] == "English"
        assert english_translations[LanguageEnum.RUSSIAN] == "Английский"
        assert english_translations[LanguageEnum.FRENCH] == "Anglais"

    def test_get_display_name_default(self):
        """Test get_display_name with default locale."""
        name = LanguageEnum.ENGLISH.get_display_name()
        assert name == "English"

    def test_get_display_name_custom_locale(self):
        """Test get_display_name with custom locale."""
        name = LanguageEnum.ENGLISH.get_display_name(LanguageEnum.RUSSIAN)
        assert name == "Английский"

        name = LanguageEnum.RUSSIAN.get_display_name(LanguageEnum.ENGLISH)
        assert name == "Russian"

    def test_get_display_name_string_locale(self):
        """Test get_display_name with string locale."""
        name = LanguageEnum.FRENCH.get_display_name("en")
        assert name == "French"

    def test_all_languages_have_translations(self):
        """Test that all languages have translations for all other languages."""
        translations = LanguageEnum.ENGLISH.get_translations()
        for lang in LanguageEnum:
            assert lang in translations
            lang_translations = translations[lang]
            for other_lang in LanguageEnum:
                assert other_lang in lang_translations
                assert isinstance(lang_translations[other_lang], str)
                assert len(lang_translations[other_lang]) > 0


@pytest.mark.unit
class TestLanguage:
    """Tests for Language dataclass."""

    def test_language_creation(self):
        """Test creating a Language instance."""
        lang = Language(id="en", name="English")
        assert lang.id == "en"
        assert lang.name == "English"

    def test_language_empty_id_raises_error(self):
        """Test that empty id raises ValueError."""
        with pytest.raises(ValueError, match="Language id and name must not be empty"):
            Language(id="", name="English")

    def test_language_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Language id and name must not be empty"):
            Language(id="en", name="")

    def test_language_none_id_raises_error(self):
        """Test that None id raises ValueError."""
        with pytest.raises(ValueError, match="Language id and name must not be empty"):
            Language(id=None, name="English")  # type: ignore

    def test_language_none_name_raises_error(self):
        """Test that None name raises ValueError."""
        with pytest.raises(ValueError, match="Language id and name must not be empty"):
            Language(id="en", name=None)  # type: ignore


@pytest.mark.unit
class TestGetLanguageById:
    """Tests for get_language_by_id function."""

    def test_get_language_by_id_valid(self):
        """Test getting a language by valid ID."""
        lang = get_language_by_id("en")
        assert lang is not None
        assert isinstance(lang, Language)
        assert lang.id == "en"
        assert lang.name == "English"

    def test_get_language_by_id_russian(self):
        """Test getting Russian language."""
        lang = get_language_by_id("ru")
        assert lang is not None
        assert lang.id == "ru"
        # get_language_by_id uses default locale "en", so it returns English name
        assert lang.name == "Russian"

    def test_get_language_by_id_invalid(self):
        """Test getting a language by invalid ID."""
        lang = get_language_by_id("invalid")
        assert lang is None

    def test_get_language_by_id_all_enum_values(self):
        """Test that all enum values can be retrieved."""
        for lang_enum in LanguageEnum:
            lang = get_language_by_id(lang_enum.value)
            assert lang is not None
            assert lang.id == lang_enum.value
            assert isinstance(lang.name, str)
            assert len(lang.name) > 0


@pytest.mark.unit
class TestGetLanguageList:
    """Tests for get_language_list function."""

    def test_get_language_list_returns_list(self):
        """Test that get_language_list returns a list."""
        languages = get_language_list()
        assert isinstance(languages, list)

    def test_get_language_list_contains_all_languages(self):
        """Test that all languages are in the list."""
        languages = get_language_list()
        assert len(languages) == len(LanguageEnum)
        language_ids = {lang.id for lang in languages}
        enum_values = {lang.value for lang in LanguageEnum}
        assert language_ids == enum_values

    def test_get_language_list_all_are_language_instances(self):
        """Test that all items in the list are Language instances."""
        languages = get_language_list()
        for lang in languages:
            assert isinstance(lang, Language)
            assert lang.id is not None
            assert lang.name is not None
            assert len(lang.id) > 0
            assert len(lang.name) > 0

    def test_get_language_list_names_match_display_names(self):
        """Test that language names match display names."""
        languages = get_language_list()
        for lang in languages:
            lang_enum = LanguageEnum(lang.id)
            expected_name = lang_enum.get_display_name()
            assert lang.name == expected_name


