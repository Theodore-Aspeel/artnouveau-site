import unittest

from tools.editorial_manager.reel_pilot import build_reel_pilot


def ready_article() -> dict:
    return {
        "slug": "demo",
        "status": "ready",
        "format": "long",
        "publication": {"order": 1},
        "media": {
            "hero": {"src": "assets/images/demo.png"},
            "support": [{"src": "assets/images/related.png"}],
        },
        "facts": {"location": {"city": "Lille", "country": "France"}},
        "taxonomy": {"style_key": "art_nouveau"},
        "content": {
            "fr": {
                "title": "Maison Demo",
                "dek": "Une lecture attentive de la rue.",
                "epigraph": "Une façade change la rue.",
                "sections": [
                    {"heading": "Lire la façade", "body": "A"},
                    {"heading": "Regarder le seuil", "body": "B"},
                ],
                "seo": {"meta_description": "Meta FR."},
                "media": {
                    "hero_alt": "Façade de la Maison Demo.",
                    "support_alt": ["Un bâtiment voisin."],
                },
            },
            "en": {
                "title": "Demo House",
                "dek": "A close reading of the street.",
                "epigraph": "A facade changes the street.",
                "sections": [
                    {"heading": "Read the facade", "body": "A"},
                    {"heading": "Look at the threshold", "body": "B"},
                ],
                "seo": {"meta_description": "Meta EN."},
                "media": {
                    "hero_alt": "Facade of Demo House.",
                    "support_alt": ["A nearby building."],
                },
            },
        },
    }


class ReelPilotTests(unittest.TestCase):
    def test_builds_review_only_reel_contract_from_source_content(self):
        payload = build_reel_pilot(ready_article(), "fr")

        self.assertEqual(payload["contract"], {
            "name": "artnouveau.reel_pilot",
            "version": 1,
            "kind": "read_only_reel_pilot_handoff",
        })
        self.assertEqual(payload["pilot_status"], "ready_for_human_storyboard_review")
        self.assertEqual(payload["format"]["aspect_ratio"], "9:16")
        self.assertEqual(payload["format"]["target_duration_seconds"], 24)
        self.assertEqual(
            [hook["source"] for hook in payload["creative"]["hook_options"]],
            ["social_hook", "article_epigraph", "first_section_heading"],
        )
        self.assertEqual(len(payload["creative"]["storyboard"]), 5)
        self.assertTrue(all(
            scene["source_image"] == "assets/images/demo.png"
            for scene in payload["creative"]["storyboard"]
        ))
        self.assertFalse(payload["automation_limits"]["publishes_to_instagram"])

    def test_keeps_related_images_out_of_default_storyboard(self):
        payload = build_reel_pilot(ready_article(), "fr")

        contextual = payload["media_plan"]["contextual_images"]
        self.assertTrue(payload["media_plan"]["default_storyboard_uses_primary_only"])
        self.assertEqual(contextual[0]["role"], "related_place_context")
        self.assertFalse(contextual[0]["use_in_default_storyboard"])

    def test_builds_traceable_locale_aware_url(self):
        payload = build_reel_pilot(
            ready_article(),
            "en",
            "https://theodore-aspeel.github.io/artnouveau-site/",
        )

        link = payload["link_plan"]
        self.assertEqual(link["destination_locale"], "en")
        self.assertTrue(link["tracked_url"].startswith(
            "https://theodore-aspeel.github.io/artnouveau-site/en/articles/demo/?"
        ))
        self.assertEqual(link["utm"]["utm_source"], "instagram")
        self.assertEqual(link["utm"]["utm_medium"], "organic_social")
        self.assertEqual(link["utm"]["utm_content"], "en_pilot")

    def test_marks_draft_article_as_needing_upstream_review(self):
        article = ready_article()
        article["status"] = "draft"

        payload = build_reel_pilot(article, "fr")

        self.assertEqual(payload["pilot_status"], "needs_upstream_review")
        self.assertEqual(payload["upstream"]["queue_status"], "needs-review")
        self.assertEqual(payload["human_gates"][-1]["status"], "blocked_until_explicit_approval")

    def test_rejects_invalid_public_base_url(self):
        with self.assertRaisesRegex(ValueError, "absolute http"):
            build_reel_pilot(ready_article(), "fr", "/relative")


if __name__ == "__main__":
    unittest.main()
