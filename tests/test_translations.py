from codebarbuilder.translations import TRANSLATIONS


REQUIRED_KEYS = set(TRANSLATIONS["es"])


def test_spanish_and_english_have_same_translation_keys():
    assert set(TRANSLATIONS["en"]) == REQUIRED_KEYS


def test_translations_do_not_have_empty_values():
    for language, messages in TRANSLATIONS.items():
        for key, value in messages.items():
            assert value.strip(), f"{language}.{key} is empty"
