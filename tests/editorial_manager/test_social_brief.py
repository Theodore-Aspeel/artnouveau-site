import unittest

from tools.editorial_manager.social_brief import build_social_brief, social_brief_to_dict


class SocialBriefTests(unittest.TestCase):
    def test_build_social_brief_collects_publication_fields(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "format": "long",
            "publication": {"order": 1},
            "media": {
                "hero": {"src": "assets/images/demo.png"},
                "support": [
                    {"src": "assets/images/support-one.png"},
                    {"src": "  "},
                    {"src": "assets/images/support-two.png"},
                ],
            },
            "sources": {
                "quote": {
                    "text": {"fr": "Citation FR.", "en": "Quote EN."},
                    "author": "Demo Author",
                    "attribution": {"fr": "Source FR.", "en": "Source EN."},
                }
            },
            "content": {
                "fr": {
                    "title": "Titre FR",
                    "dek": "Dek FR.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta FR."},
                    "media": {"hero_alt": "Alt FR."},
                    "practical_items": [
                        {"key": "city", "value": "Lille"},
                        {"key": "style", "value": "Art Nouveau"},
                    ],
                },
                "en": {
                    "title": "Title EN",
                    "dek": "Dek EN.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta EN."},
                    "media": {"hero_alt": "Alt EN."},
                },
            },
        }

        brief = build_social_brief(article)

        self.assertEqual(brief.slug, "demo")
        self.assertEqual(brief.title_fr, "Titre FR")
        self.assertEqual(brief.title_en, "Title EN")
        self.assertEqual(brief.locale_status.status, "en-ready")
        self.assertEqual(brief.dek_fr, "Dek FR.")
        self.assertEqual(brief.dek_en, "Dek EN.")
        self.assertIsNotNone(brief.quote)
        self.assertEqual(brief.quote.author, "Demo Author")
        self.assertEqual([item.key for item in brief.practical_items], ["city", "style"])
        self.assertTrue(brief.images.has_hero)
        self.assertEqual(brief.images.support_count, 2)
        self.assertEqual(brief.readiness.status, "ready")

    def test_build_social_brief_keeps_missing_english_empty(self):
        article = {
            "slug": "demo",
            "title": "Legacy title",
            "chapeau": "Legacy dek.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Alt.",
            "meta_description": "Meta.",
            "publication_order_recommended": 1,
            "content": {"en": {}},
        }

        brief = build_social_brief(article)

        self.assertEqual(brief.title_fr, "Legacy title")
        self.assertEqual(brief.title_en, "")
        self.assertEqual(brief.dek_en, "")
        self.assertEqual(brief.locale_status.status, "fr-only")
        self.assertEqual(brief.readiness.status, "needs review")

    def test_social_brief_to_dict_keeps_automation_fields_simple(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "format": "long",
            "publication": {"order": 1},
            "media": {
                "hero": {"src": "assets/images/demo.png"},
                "support": [{"src": "assets/images/support.png"}],
            },
            "sources": {
                "quote": {
                    "text": {"fr": "Citation FR.", "en": "Quote EN."},
                    "author": "Demo Author",
                    "attribution": {"fr": "Source FR.", "en": "Source EN."},
                }
            },
            "content": {
                "fr": {
                    "title": "Titre FR",
                    "dek": "Dek FR.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta FR."},
                    "media": {"hero_alt": "Alt FR."},
                    "practical_items": [{"key": "city", "value": "Lille"}],
                },
                "en": {
                    "title": "Title EN",
                    "dek": "Dek EN.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta EN."},
                    "media": {"hero_alt": "Alt EN."},
                },
            },
        }

        payload = social_brief_to_dict(build_social_brief(article))

        self.assertEqual(payload["slug"], "demo")
        self.assertEqual(payload["locale_status"]["status"], "en-ready")
        self.assertEqual(payload["title_fr"], "Titre FR")
        self.assertEqual(payload["title_en"], "Title EN")
        self.assertEqual(payload["dek_fr"], "Dek FR.")
        self.assertEqual(payload["dek_en"], "Dek EN.")
        self.assertEqual(payload["quote"]["author"], "Demo Author")
        self.assertEqual(payload["practical_items"], [{"key": "city", "value": "Lille"}])
        self.assertEqual(payload["image_summary"]["hero_src"], "assets/images/demo.png")
        self.assertEqual(payload["image_summary"]["support_count"], 1)
        self.assertEqual(payload["readiness"]["status"], "ready")


if __name__ == "__main__":
    unittest.main()
