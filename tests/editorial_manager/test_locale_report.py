import unittest

from tools.editorial_manager.locale_report import analyze_article_locale, analyze_articles_locale


def article_with_english(english):
    return {
        "slug": "demo",
        "schema_version": 2,
        "content": {
            "fr": {
                "title": "Titre",
                "dek": "Chapeau.",
                "sections": [{"heading": "A", "body": "B"}],
                "seo": {"meta_description": "Meta FR."},
                "media": {"hero_alt": "Alt FR."},
            },
            "en": english,
        },
    }


class LocaleReportTests(unittest.TestCase):
    def test_article_without_real_english_is_fr_only(self):
        item = analyze_article_locale(article_with_english({"title": "  ", "sections": []}))

        self.assertEqual(item.status, "fr-only")
        self.assertIn("title", item.missing_fields)
        self.assertIn("sections", item.missing_fields)

    def test_article_with_missing_main_english_fields_is_partial(self):
        item = analyze_article_locale(article_with_english({
            "title": "Demo",
            "sections": [{"heading": "A", "body": ""}],
            "seo": {"meta_description": "Meta EN."},
        }))

        self.assertEqual(item.status, "en-partial")
        self.assertIn("dek", item.missing_fields)
        self.assertIn("media.hero_alt", item.missing_fields)
        self.assertIn("sections[1].body", item.missing_fields)

    def test_article_with_main_english_fields_is_ready(self):
        item = analyze_article_locale(article_with_english({
            "title": "Demo",
            "dek": "Dek.",
            "sections": [{"heading": "A", "body": "B"}],
            "seo": {"meta_description": "Meta EN."},
            "media": {"hero_alt": "Alt EN."},
        }))

        self.assertEqual(item.status, "en-ready")
        self.assertEqual(item.missing_fields, ())

    def test_article_with_target_locale_fields_is_ready(self):
        article = article_with_english({"title": "Demo"})
        article["content"]["nl"] = {
            "title": "Demo NL",
            "dek": "Dek NL.",
            "sections": [{"heading": "A", "body": "B"}],
            "seo": {"meta_description": "Meta NL."},
            "media": {"hero_alt": "Alt NL."},
        }

        item = analyze_article_locale(article, "nl")

        self.assertEqual(item.status, "nl-ready")
        self.assertEqual(item.missing_fields, ())

    def test_missing_prepared_target_locale_stays_fr_only(self):
        item = analyze_article_locale(article_with_english({"title": "Demo"}), "nl")

        self.assertEqual(item.status, "fr-only")
        self.assertIn("title", item.missing_fields)

    def test_articles_locale_preserves_one_item_per_article(self):
        items = analyze_articles_locale([
            article_with_english({"title": "Demo"}),
            {"slug": "other", "content": {"fr": {"title": "Autre"}, "en": {}}},
        ])

        self.assertEqual([item.slug for item in items], ["demo", "other"])


if __name__ == "__main__":
    unittest.main()
