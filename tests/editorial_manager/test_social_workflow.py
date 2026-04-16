import unittest

from tools.editorial_manager.social_queue import SocialQueueFilters
from tools.editorial_manager.social_workflow import build_social_workflow


def ready_article(slug: str, order: int = 1) -> dict:
    return {
        "slug": slug,
        "status": "ready",
        "format": "long",
        "publication": {"order": order},
        "media": {"hero": {"src": f"assets/images/{slug}.png"}},
        "facts": {"location": {"city": "Lille"}},
        "taxonomy": {"style_key": "art-nouveau"},
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


class SocialWorkflowTests(unittest.TestCase):
    def test_social_workflow_selects_next_article_and_builds_package(self):
        blocked = ready_article("blocked", order=1)
        blocked["media"]["hero"]["src"] = ""
        candidate = ready_article("candidate", order=2)

        workflow = build_social_workflow([candidate, blocked], locale="en")

        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.selected.slug, "candidate")
        self.assertEqual(workflow.package.slug, "candidate")
        self.assertEqual(workflow.package.requested_locale, "en")
        self.assertEqual(workflow.package.source_locale, "en")
        self.assertEqual(workflow.package.caption.title, "Title candidate")

    def test_social_workflow_returns_none_when_no_article_matches_filters(self):
        article = ready_article("candidate")

        workflow = build_social_workflow(
            [article],
            filters=SocialQueueFilters(status="blocked"),
        )

        self.assertIsNone(workflow)


if __name__ == "__main__":
    unittest.main()
