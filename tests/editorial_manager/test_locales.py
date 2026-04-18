import unittest

from tools.editorial_manager.locales import (
    DEFAULT_LOCALE,
    editable_locale_specs,
    locale_status_choices,
    normalize_locale,
    preview_locale_codes,
    public_locale_codes,
    required_locale_codes,
)


class LocaleContractTests(unittest.TestCase):
    def test_locale_contract_prepares_internal_nl_without_public_locale(self):
        self.assertEqual(DEFAULT_LOCALE, "fr")
        self.assertEqual(required_locale_codes(), ("fr",))
        self.assertIn("en", preview_locale_codes())
        self.assertIn("nl", preview_locale_codes())
        self.assertNotIn("nl", public_locale_codes())
        self.assertEqual([locale.code for locale in editable_locale_specs()], ["fr", "en"])

    def test_normalize_locale_accepts_language_regions(self):
        self.assertEqual(normalize_locale("nl-BE"), "nl")
        self.assertEqual(normalize_locale("unknown"), "fr")

    def test_status_choices_include_prepared_optional_locales(self):
        self.assertIn("en-ready", locale_status_choices())
        self.assertIn("nl-partial", locale_status_choices())


if __name__ == "__main__":
    unittest.main()
