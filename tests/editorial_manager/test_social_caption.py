import unittest

from tools.editorial_manager.social_caption import build_social_caption, social_caption_to_dict


class SocialCaptionTests(unittest.TestCase):
    def test_build_social_caption_uses_french_content_by_default(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "format": "long",
            "publication": {"order": 1},
            "media": {"hero": {"src": "assets/images/demo.png"}},
            "facts": {"location": {"city": "Lille", "country": "France"}},
            "taxonomy": {"style_key": "art-nouveau"},
            "content": {
                "fr": {
                    "title": "Maison Demo",
                    "dek": "Une façade expressive au cœur de Lille.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta FR."},
                    "media": {"hero_alt": "Alt FR."},
                    "practical_items": [
                        {"key": "city", "value": "Lille"},
                        {"key": "style", "value": "Art Nouveau"},
                    ],
                },
                "en": {
                    "title": "Demo House",
                    "dek": "An expressive facade in Lille.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta EN."},
                    "media": {"hero_alt": "Alt EN."},
                },
            },
        }

        caption = build_social_caption(article)

        self.assertEqual(caption.slug, "demo")
        self.assertEqual(caption.requested_locale, "fr")
        self.assertEqual(caption.source_locale, "fr")
        self.assertEqual(caption.locale_status, "en-ready")
        self.assertEqual(caption.title, "Maison Demo")
        self.assertEqual(caption.hook, "À découvrir: Maison Demo")
        self.assertEqual(caption.caption, "Une façade expressive au cœur de Lille.")
        self.assertEqual(caption.cta, "Lire l'article sur le site.")
        self.assertEqual(caption.hashtags, ("#ArtNouveau", "#Lille", "#France", "#Architecture", "#Patrimoine"))

    def test_build_social_caption_uses_english_when_present(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "format": "long",
            "publication": {"order": 1},
            "media": {"hero": {"src": "assets/images/demo.png"}},
            "content": {
                "fr": {
                    "title": "Maison Demo",
                    "dek": "Dek FR.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta FR."},
                    "media": {"hero_alt": "Alt FR."},
                },
                "en": {
                    "title": "Demo House",
                    "dek": "An expressive facade in Lille.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Meta EN."},
                    "media": {"hero_alt": "Alt EN."},
                },
            },
        }

        caption = build_social_caption(article, "en")

        self.assertEqual(caption.requested_locale, "en")
        self.assertEqual(caption.source_locale, "en")
        self.assertEqual(caption.title, "Demo House")
        self.assertEqual(caption.hook, "Look closer: Demo House")
        self.assertEqual(caption.caption, "An expressive facade in Lille.")
        self.assertEqual(caption.cta, "Read the article on the site.")

    def test_build_social_caption_marks_french_fallback_for_missing_english(self):
        article = {
            "slug": "demo",
            "title": "Legacy title",
            "chapeau": "Legacy dek.",
            "city": "Nancy",
            "style": "Art Nouveau",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Alt.",
            "meta_description": "Meta.",
            "publication_order_recommended": 1,
            "content": {"en": {}},
        }

        caption = build_social_caption(article, "en")

        self.assertEqual(caption.requested_locale, "en")
        self.assertEqual(caption.source_locale, "fr")
        self.assertEqual(caption.locale_status, "fr-only")
        self.assertEqual(caption.title, "Legacy title")
        self.assertEqual(caption.hook, "À découvrir: Legacy title")
        self.assertEqual(caption.caption, "Legacy dek.")

    def test_build_social_caption_keeps_caption_short(self):
        article = {
            "slug": "demo",
            "title": "Legacy title",
            "chapeau": (
                "Cette façade concentre un ensemble de détails sculptés, de lignes "
                "souples et de matériaux contrastés qui donnent immédiatement une "
                "lecture urbaine très forte, tout en restant assez discrète dans "
                "la continuité de la rue et de ses bâtiments voisins."
            ),
            "hero_image": "assets/images/demo.png",
            "alt_text": "Alt.",
            "meta_description": "Meta.",
            "publication_order_recommended": 1,
            "content": {"en": {}},
        }

        caption = build_social_caption(article)

        self.assertLessEqual(len(caption.caption), 220)
        self.assertTrue(caption.caption.endswith("..."))

    def test_social_caption_to_dict_keeps_small_automation_payload(self):
        article = {
            "slug": "demo",
            "title": "Legacy title",
            "chapeau": "Legacy dek.",
            "city": "Nancy",
            "style": "Art Nouveau",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Alt.",
            "meta_description": "Meta.",
            "publication_order_recommended": 1,
            "content": {"en": {}},
        }

        payload = social_caption_to_dict(build_social_caption(article, "en"))

        self.assertEqual(payload["slug"], "demo")
        self.assertEqual(payload["requested_locale"], "en")
        self.assertEqual(payload["source_locale"], "fr")
        self.assertEqual(payload["locale_status"], "fr-only")
        self.assertEqual(payload["title"], "Legacy title")
        self.assertEqual(payload["caption"], "Legacy dek.")
        self.assertEqual(payload["hashtags"][:2], ["#ArtNouveau", "#Nancy"])


if __name__ == "__main__":
    unittest.main()
