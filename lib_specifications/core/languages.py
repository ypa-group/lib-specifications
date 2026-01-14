from dataclasses import dataclass
from enum import Enum


class LanguageEnum(str, Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"
    FRENCH = "fr"
    SPANISH = "es"
    ARABIC = "ar"
    HEBREW = "he"
    POLISH = "pl"
    PORTUGUESE = "pt"
    UKRAINIAN = "uk"
    CHINESE = "zh"

    def get_translations(self) -> dict["LanguageEnum", dict["LanguageEnum", str]]:
        return {
            LanguageEnum.ENGLISH: {
                LanguageEnum.ENGLISH: "English",
                LanguageEnum.RUSSIAN: "Английский",
                LanguageEnum.FRENCH: "Anglais",
                LanguageEnum.SPANISH: "Inglés",
                LanguageEnum.ARABIC: "إنجليزية",
                LanguageEnum.HEBREW: "אנגלית",
                LanguageEnum.POLISH: "Angielski",
                LanguageEnum.PORTUGUESE: "Inglês",
                LanguageEnum.UKRAINIAN: "Англійська",
                LanguageEnum.CHINESE: "英语",
            },
            LanguageEnum.RUSSIAN: {
                LanguageEnum.ENGLISH: "Russian",
                LanguageEnum.RUSSIAN: "Русский",
                LanguageEnum.FRENCH: "Russe",
                LanguageEnum.SPANISH: "Ruso",
                LanguageEnum.ARABIC: "روسية",
                LanguageEnum.HEBREW: "רוסית",
                LanguageEnum.POLISH: "Rosyjski",
                LanguageEnum.PORTUGUESE: "Russo",
                LanguageEnum.UKRAINIAN: "Руська",
                LanguageEnum.CHINESE: "俄语",
            },
            LanguageEnum.FRENCH: {
                LanguageEnum.ENGLISH: "French",
                LanguageEnum.RUSSIAN: "Французский",
                LanguageEnum.FRENCH: "Français",
                LanguageEnum.SPANISH: "Francés",
                LanguageEnum.ARABIC: "فرنسية",
                LanguageEnum.HEBREW: "צרפתית",
                LanguageEnum.POLISH: "Francuski",
                LanguageEnum.PORTUGUESE: "Francês",
                LanguageEnum.UKRAINIAN: "Французька",
                LanguageEnum.CHINESE: "法语",
            },
            LanguageEnum.SPANISH: {
                LanguageEnum.ENGLISH: "Spanish",
                LanguageEnum.RUSSIAN: "Испанский",
                LanguageEnum.FRENCH: "Espagnol",
                LanguageEnum.SPANISH: "Español",
                LanguageEnum.ARABIC: "إسبانية",
                LanguageEnum.HEBREW: "ספרדית",
                LanguageEnum.POLISH: "Hiszpański",
                LanguageEnum.PORTUGUESE: "Espanhol",
                LanguageEnum.UKRAINIAN: "Іспанська",
                LanguageEnum.CHINESE: "西班牙语",
            },
            LanguageEnum.ARABIC: {
                LanguageEnum.ENGLISH: "Arabic",
                LanguageEnum.RUSSIAN: "Арабский",
                LanguageEnum.FRENCH: "Arabe",
                LanguageEnum.SPANISH: "Árabe",
                LanguageEnum.ARABIC: "عربية",
                LanguageEnum.HEBREW: "ערבית",
                LanguageEnum.POLISH: "Arabski",
                LanguageEnum.PORTUGUESE: "Árabe",
                LanguageEnum.UKRAINIAN: "Арабська",
                LanguageEnum.CHINESE: "阿拉伯语",
            },
            LanguageEnum.HEBREW: {
                LanguageEnum.ENGLISH: "Hebrew",
                LanguageEnum.RUSSIAN: "Иврит",
                LanguageEnum.FRENCH: "Hébreu",
                LanguageEnum.SPANISH: "Hebreo",
                LanguageEnum.ARABIC: "عربية",
                LanguageEnum.HEBREW: "ערבית",
                LanguageEnum.POLISH: "Hebrajski",
                LanguageEnum.PORTUGUESE: "Hebraico",
                LanguageEnum.UKRAINIAN: "Іврит",
                LanguageEnum.CHINESE: "希伯来语",
            },
            LanguageEnum.POLISH: {
                LanguageEnum.ENGLISH: "Polish",
                LanguageEnum.RUSSIAN: "Польский",
                LanguageEnum.FRENCH: "Polonais",
                LanguageEnum.SPANISH: "Polaco",
                LanguageEnum.ARABIC: "بولندية",
                LanguageEnum.HEBREW: "פולנית",
                LanguageEnum.POLISH: "Polski",
                LanguageEnum.PORTUGUESE: "Polonês",
                LanguageEnum.UKRAINIAN: "Польська",
                LanguageEnum.CHINESE: "波兰语",
            },
            LanguageEnum.PORTUGUESE: {
                LanguageEnum.ENGLISH: "Portuguese",
                LanguageEnum.RUSSIAN: "Португальский",
                LanguageEnum.FRENCH: "Portugais",
                LanguageEnum.SPANISH: "Portugués",
                LanguageEnum.ARABIC: "بورتغالية",
                LanguageEnum.HEBREW: "פורטוגזית",
                LanguageEnum.POLISH: "Portugalski",
                LanguageEnum.PORTUGUESE: "Português",
                LanguageEnum.UKRAINIAN: "Португальська",
                LanguageEnum.CHINESE: "葡萄牙语",
            },
            LanguageEnum.UKRAINIAN: {
                LanguageEnum.ENGLISH: "Ukrainian",
                LanguageEnum.RUSSIAN: "Украинский",
                LanguageEnum.FRENCH: "Ukrainien",
                LanguageEnum.SPANISH: "Ucraniano",
                LanguageEnum.ARABIC: "أوكرانية",
                LanguageEnum.HEBREW: "אוקראינית",
                LanguageEnum.POLISH: "Ukraiński",
                LanguageEnum.PORTUGUESE: "Ucraniano",
                LanguageEnum.UKRAINIAN: "Українська",
                LanguageEnum.CHINESE: "乌克兰语",
            },
            LanguageEnum.CHINESE: {
                LanguageEnum.ENGLISH: "Chinese",
                LanguageEnum.RUSSIAN: "Китайский",
                LanguageEnum.FRENCH: "Chinois",
                LanguageEnum.SPANISH: "Chino",
                LanguageEnum.ARABIC: "صينية",
                LanguageEnum.HEBREW: "סינית",
                LanguageEnum.POLISH: "Chiński",
                LanguageEnum.PORTUGUESE: "Chinês",
                LanguageEnum.UKRAINIAN: "Китайська",
                LanguageEnum.CHINESE: "中文",
            },
        }

    def get_display_name(self, locale: "LanguageEnum" = "en") -> str:
        return self.get_translations()[self][LanguageEnum(locale)]


@dataclass
class Language:
    id: str
    name: str

    def __post_init__(self) -> None:
        """Validate Language invariants."""
        if not self.id or not self.name:
            raise ValueError("Language id and name must not be empty")


def get_language_by_id(language_id: str) -> Language | None:
    try:
        return Language(
            id=language_id,
            name=LanguageEnum(language_id).get_display_name(),
        )
    except ValueError:
        return None


def get_language_list() -> list[Language]:
    languages = [
        Language(
            id=language.value,
            name=language.get_display_name(),
        )
        for language in LanguageEnum
    ]
    return languages
