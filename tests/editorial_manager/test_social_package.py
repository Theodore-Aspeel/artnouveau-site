import unittest

from tools.editorial_manager.social_package import build_social_package, social_package_to_dict


def ready_article() -> dict:
    return {
        "slug": "demo",
        "status": "ready",
        "format": "long",
        "publication": {"order": 1},
        "media": {
            "hero": {
                "src": "assets/images/demo.png",
                "caption": "Stable hero caption.",
            },
            "support": [
                {
                    "src": "assets/images/support.png",
                    "caption": "Stable support caption.",
                },
            ],
        },
        "facts": {"location": {"city": "Lille", "country": "France"}},
        "taxonomy": {"style_key": "art-nouveau"},
        "content": {
            "fr": {
                "title": "Maison Demo",
                "dek": "Dek FR.",
                "sections": [{"heading": "A", "body": "B"}],
                "seo": {"meta_description": "Meta FR."},
                "media": {
                    "hero_alt": "Alt FR.",
                    "hero_caption": "Caption FR.",
                    "support_alt": ["Support alt FR."],
                    "support_captions": ["Support caption FR."],
                },
                "practical_items": [
                    {"key": "city", "value": "Lille"},
                    {"key": "style", "value": "Art Nouveau"},
                ],
            },
            "en": {
                "title": "Demo House",
                "dek": "Dek EN.",
                "sections": [{"heading": "A", "body": "B"}],
                "seo": {"meta_description": "Meta EN."},
                "media": {
                    "hero_alt": "Alt EN.",
                    "hero_caption": "Caption EN.",
                    "support_alt": ["Support alt EN."],
                    "support_captions": ["Support caption EN."],
                },
            },
        },
    }


class SocialPackageTests(unittest.TestCase):
    def test_social_package_combines_existing_social_payloads(self):
        package = build_social_package(ready_article(), "en")
        payload = social_package_to_dict(package)

        self.assertEqual(payload["slug"], "demo")
        self.assertEqual(payload["requested_locale"], "en")
        self.assertEqual(payload["source_locale"], "en")
        self.assertEqual(payload["locale_status"]["status"], "en-ready")
        self.assertEqual(payload["queue_status"], "candidate")
        self.assertEqual(payload["brief"]["slug"], "demo")
        self.assertEqual(payload["brief"]["title_fr"], "Maison Demo")
        self.assertEqual(payload["caption"]["title"], "Demo House")
        self.assertEqual(payload["image_summary"], {
            "has_hero": True,
            "hero_src": "assets/images/demo.png",
            "support_count": 1,
        })
        self.assertEqual(payload["media"], {
            "hero": {
                "src": "assets/images/demo.png",
                "alt": "Alt EN.",
                "caption": "Caption EN.",
            },
            "support": [
                {
                    "src": "assets/images/support.png",
                    "alt": "Support alt EN.",
                    "caption": "Support caption EN.",
                },
            ],
        })
        self.assertEqual(payload["links"]["article_fr_path"], "article.html?slug=demo")
        self.assertEqual(payload["links"]["article_en_preview_path"], "article.html?slug=demo&previewLocale=en")
        self.assertEqual(payload["links"]["preview_paths"]["nl"], "article.html?slug=demo&previewLocale=nl")
        self.assertEqual(payload["readiness"]["status"], "ready")
        self.assertEqual(payload["reasons"], [
            "Publication checklist is ready.",
            "English content is ready.",
            "Hero image is present.",
        ])

    def test_social_package_reports_french_source_when_english_is_missing(self):
        article = ready_article()
        article["content"]["en"] = {}

        payload = social_package_to_dict(build_social_package(article, "en"))

        self.assertEqual(payload["requested_locale"], "en")
        self.assertEqual(payload["source_locale"], "fr")
        self.assertEqual(payload["locale_status"]["status"], "fr-only")
        self.assertEqual(payload["queue_status"], "needs-review")
        self.assertEqual(payload["caption"]["title"], "Maison Demo")
        self.assertEqual(payload["media"]["hero"]["alt"], "Alt FR.")
        self.assertEqual(payload["media"]["hero"]["caption"], "Caption FR.")
        self.assertIn("English content is missing.", payload["reasons"])

    def test_social_package_media_uses_stable_fallbacks_and_keeps_support_order(self):
        article = ready_article()
        article["content"]["fr"]["media"] = {
            "hero_alt": "Alt FR.",
            "support_alt": ["First alt."],
            "support_captions": ["First caption."],
        }
        article["media"]["support"] = [
            {"src": "assets/images/first.png"},
            {"src": ""},
            {
                "src": "assets/images/second.png",
                "alt": "Second stable alt.",
                "caption": "Second stable caption.",
            },
        ]

        payload = social_package_to_dict(build_social_package(article, "fr"))

        self.assertEqual(payload["media"]["hero"], {
            "src": "assets/images/demo.png",
            "alt": "Alt FR.",
            "caption": "Stable hero caption.",
        })
        self.assertEqual(payload["media"]["support"], [
            {
                "src": "assets/images/first.png",
                "alt": "First alt.",
                "caption": "First caption.",
            },
            {
                "src": "assets/images/second.png",
                "alt": "Second stable alt.",
                "caption": "Second stable caption.",
            },
        ])

    def test_social_package_links_encode_slug_and_keep_relative_paths(self):
        article = ready_article()
        article["slug"] = "demo/lille ete"

        payload = social_package_to_dict(build_social_package(article, "fr"))

        self.assertEqual(payload["links"]["article_fr_path"], "article.html?slug=demo%2Flille%20ete")
        self.assertEqual(
            payload["links"]["article_en_preview_path"],
            "article.html?slug=demo%2Flille%20ete&previewLocale=en",
        )
        self.assertEqual(
            payload["links"]["preview_paths"]["nl"],
            "article.html?slug=demo%2Flille%20ete&previewLocale=nl",
        )


if __name__ == "__main__":
    unittest.main()
