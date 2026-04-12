import unittest

from tools.editorial_manager.article_access import (
    article_hero_alt,
    article_hero_image,
    article_meta_description,
    article_model,
    article_publication_order,
    article_sections_count,
    article_taxonomy,
    article_title,
    has_english_content,
)


class ArticleAccessTests(unittest.TestCase):
    def test_detects_v1_article(self):
        self.assertEqual(article_model({"slug": "demo", "title": "Demo"}), "v1")

    def test_detects_v2_article_from_schema_version(self):
        self.assertEqual(article_model({"schema_version": 2, "slug": "demo"}), "v2")

    def test_detects_v2_article_from_content(self):
        self.assertEqual(article_model({"slug": "demo", "content": {"fr": {}}}), "v2")

    def test_title_prefers_v2_french_content(self):
        article = {
            "title": "Legacy title",
            "content": {"fr": {"title": "Titre v2"}},
        }
        self.assertEqual(article_title(article), "Titre v2")

    def test_hero_image_supports_v1_and_v2(self):
        v1 = {"hero_image": "assets/images/demo.png"}
        v2 = {"media": {"hero": {"src": "assets/images/v2.png"}}}

        self.assertEqual(article_hero_image(v1), "assets/images/demo.png")
        self.assertEqual(article_hero_image(v2), "assets/images/v2.png")

    def test_hero_alt_supports_v1_and_v2(self):
        v1 = {"alt_text": "Legacy alt"}
        v2 = {"content": {"fr": {"media": {"hero_alt": "Alt v2"}}}}

        self.assertEqual(article_hero_alt(v1), "Legacy alt")
        self.assertEqual(article_hero_alt(v2), "Alt v2")

    def test_meta_description_supports_v1_and_v2(self):
        v1 = {"meta_description": "Legacy meta"}
        v2 = {"content": {"fr": {"seo": {"meta_description": "Meta v2"}}}}

        self.assertEqual(article_meta_description(v1), "Legacy meta")
        self.assertEqual(article_meta_description(v2), "Meta v2")

    def test_publication_order_supports_v1_and_v2(self):
        self.assertEqual(article_publication_order({"publication_order_recommended": 3}), 3)
        self.assertEqual(article_publication_order({"publication": {"order": 4}}), 4)

    def test_taxonomy_supports_v1_and_v2(self):
        v1 = {"style": "Art Nouveau", "city": "Tournai", "country": "Belgique"}
        v2 = {
            "taxonomy": {"style_key": "art_nouveau"},
            "facts": {"location": {"city": "Lille", "country": "France"}},
        }
        self.assertEqual(article_taxonomy(v1)["city"], "Tournai")
        self.assertEqual(article_taxonomy(v2)["style"], "art_nouveau")

    def test_taxonomy_uses_legacy_fallbacks_field_by_field(self):
        article = {
            "style": "Art Deco",
            "city": "Bruxelles",
            "country": "Belgique",
            "taxonomy": {},
            "facts": {"location": {"city": "  "}},
        }

        taxonomy = article_taxonomy(article)

        self.assertEqual(taxonomy["style"], "Art Deco")
        self.assertEqual(taxonomy["city"], "Bruxelles")
        self.assertEqual(taxonomy["country"], "Belgique")

    def test_sections_count_and_english_content(self):
        article = {
            "content": {
                "fr": {"sections": [{"heading": "A", "body": "B"}]},
                "en": {},
            }
        }
        self.assertEqual(article_sections_count(article), 1)
        self.assertFalse(has_english_content(article))

    def test_english_content_ignores_whitespace_only_strings(self):
        article = {"content": {"en": {"title": "   ", "dek": "\n\t"}}}

        self.assertFalse(has_english_content(article))

    def test_english_content_detects_real_text(self):
        article = {"content": {"en": {"title": "  English title  "}}}

        self.assertTrue(has_english_content(article))


if __name__ == "__main__":
    unittest.main()
