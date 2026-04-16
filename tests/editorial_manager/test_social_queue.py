import unittest

from tools.editorial_manager.social_queue import build_social_queue, social_queue_to_dict


def ready_article(slug: str, order: int = 1) -> dict:
    return {
        "slug": slug,
        "status": "ready",
        "format": "long",
        "publication": {"order": order},
        "media": {"hero": {"src": f"assets/images/{slug}.png"}},
        "content": {
            "fr": {
                "title": f"Titre {slug}",
                "dek": "Dek FR.",
                "sections": [{"heading": "A", "body": "B"}],
                "seo": {"meta_description": "Meta FR."},
                "media": {"hero_alt": "Alt FR."},
            },
            "en": {
                "title": f"Title {slug}",
                "dek": "Dek EN.",
                "sections": [{"heading": "A", "body": "B"}],
                "seo": {"meta_description": "Meta EN."},
                "media": {"hero_alt": "Alt EN."},
            },
        },
    }


class SocialQueueTests(unittest.TestCase):
    def test_build_social_queue_marks_candidate_when_ready(self):
        item = build_social_queue([ready_article("demo")])[0]

        self.assertEqual(item.slug, "demo")
        self.assertEqual(item.title_fr, "Titre demo")
        self.assertEqual(item.title_en, "Title demo")
        self.assertEqual(item.locale_status, "en-ready")
        self.assertEqual(item.readiness, "ready")
        self.assertTrue(item.has_hero)
        self.assertEqual(item.queue_status, "candidate")

    def test_build_social_queue_marks_needs_review_for_missing_english(self):
        article = ready_article("demo")
        article["content"]["en"] = {}

        item = build_social_queue([article])[0]

        self.assertEqual(item.locale_status, "fr-only")
        self.assertEqual(item.readiness, "needs review")
        self.assertEqual(item.queue_status, "needs-review")

    def test_build_social_queue_marks_blocked_for_publication_errors(self):
        article = ready_article("demo")
        article["media"]["hero"]["src"] = ""

        item = build_social_queue([article])[0]

        self.assertFalse(item.has_hero)
        self.assertEqual(item.readiness, "blocked")
        self.assertEqual(item.queue_status, "blocked")

    def test_build_social_queue_keeps_publication_order(self):
        items = build_social_queue([
            ready_article("second", order=2),
            ready_article("first", order=1),
        ])

        self.assertEqual([item.slug for item in items], ["first", "second"])

    def test_social_queue_to_dict_keeps_summary_and_items(self):
        article = ready_article("demo")
        payload = social_queue_to_dict(build_social_queue([article]))

        self.assertEqual(payload["summary"], {
            "total": 1,
            "candidate": 1,
            "needs_review": 0,
            "blocked": 0,
        })
        self.assertEqual(payload["items"][0]["slug"], "demo")
        self.assertEqual(payload["items"][0]["queue_status"], "candidate")
        self.assertEqual(payload["items"][0]["has_hero"], True)


if __name__ == "__main__":
    unittest.main()
