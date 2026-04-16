import json
import unittest

from tools.editorial_manager.checks import CheckIssue, PublicationCheckItem
from tools.editorial_manager.locale_report import LocaleReportItem
from tools.editorial_manager.reporting import (
    render_check_report,
    render_locale_report,
    render_publication_check_report,
    render_social_brief,
    render_social_brief_json,
    render_social_next,
    render_social_next_json,
    render_social_queue,
    render_social_queue_json,
    render_summary,
)
from tools.editorial_manager.social_brief import (
    ImagePresence,
    PracticalItem,
    ReadinessBrief,
    SocialBrief,
)
from tools.editorial_manager.social_queue import SocialQueueItem


class ReportingTests(unittest.TestCase):
    def test_summary_counts_mixed_models(self):
        articles = [
            {"slug": "one", "title": "One"},
            {"slug": "two", "schema_version": 2, "content": {"fr": {"title": "Two"}, "en": {}}},
        ]

        output = render_summary(articles)

        self.assertIn("Total articles: 2", output)
        self.assertIn("v1 articles: 1", output)
        self.assertIn("v2 articles: 1", output)
        self.assertIn("v2 without English content: 1", output)

    def test_check_report_groups_errors_and_warnings(self):
        output = render_check_report(
            [
                CheckIssue("ERROR", "missing-title-fr", "demo", "French title is missing."),
                CheckIssue("WARNING", "missing-content-en", "demo", "content.en is missing or empty."),
            ],
            checked_count=1,
        )

        self.assertIn("Articles checked: 1", output)
        self.assertIn("Errors: 1", output)
        self.assertIn("Warnings: 1", output)
        self.assertIn("Errors:", output)
        self.assertIn("[missing-title-fr] demo", output)
        self.assertIn("Warnings:", output)
        self.assertIn("[missing-content-en] demo", output)

    def test_publication_check_report_renders_checklist_items(self):
        output = render_publication_check_report(
            [
                PublicationCheckItem("OK", "title-fr", "demo", "French title is present."),
                PublicationCheckItem("WARNING", "content-en", "demo", "English content is missing or empty."),
                PublicationCheckItem("ERROR", "hero-image", "demo", "hero image is missing."),
            ],
            checked_count=1,
        )

        self.assertIn("Publication checklist", output)
        self.assertIn("Articles checked: 1", output)
        self.assertIn("OK: 1", output)
        self.assertIn("Errors: 1", output)
        self.assertIn("Warnings: 1", output)
        self.assertIn("Article: demo", output)
        self.assertIn("OK [title-fr]", output)
        self.assertIn("WARNING [content-en]", output)
        self.assertIn("ERROR [hero-image]", output)

    def test_locale_report_renders_status_counts_and_missing_fields(self):
        output = render_locale_report([
            LocaleReportItem("one", "fr-only", ("title", "sections")),
            LocaleReportItem("two", "en-partial", ("media.hero_alt",)),
            LocaleReportItem("three", "en-ready", ()),
        ])

        self.assertIn("Locale report", output)
        self.assertIn("Articles checked: 3", output)
        self.assertIn("fr-only: 1", output)
        self.assertIn("en-partial: 1", output)
        self.assertIn("en-ready: 1", output)
        self.assertIn("media.hero_alt", output)
        self.assertIn("three", output)

    def test_social_brief_renders_terminal_readable_sections(self):
        output = render_social_brief(SocialBrief(
            slug="demo",
            title_fr="Titre FR",
            title_en="Title EN",
            locale_status=LocaleReportItem("demo", "en-ready", ()),
            dek_fr="Dek FR.",
            dek_en="Dek EN.",
            quote=None,
            practical_items=(PracticalItem("city", "Lille"),),
            images=ImagePresence(True, "assets/images/demo.png", 0),
            readiness=ReadinessBrief("ready", 8, 0, 0, ()),
        ))

        self.assertIn("Social publication brief", output)
        self.assertIn("Slug: demo", output)
        self.assertIn("Locale status: en-ready", output)
        self.assertIn("Title FR: Titre FR", output)
        self.assertIn("Title EN: Title EN", output)
        self.assertIn("Practical items:", output)
        self.assertIn("city: Lille", output)
        self.assertIn("hero: yes", output)
        self.assertIn("status: ready", output)

    def test_social_brief_json_renders_structured_payload(self):
        output = render_social_brief_json(SocialBrief(
            slug="demo",
            title_fr="Titre FR",
            title_en="Title EN",
            locale_status=LocaleReportItem("demo", "en-ready", ()),
            dek_fr="Dek FR.",
            dek_en="Dek EN.",
            quote=None,
            practical_items=(PracticalItem("city", "Lille"),),
            images=ImagePresence(True, "assets/images/demo.png", 0),
            readiness=ReadinessBrief("ready", 8, 0, 0, ()),
        ))

        payload = json.loads(output)

        self.assertEqual(payload["slug"], "demo")
        self.assertEqual(payload["locale_status"], {"status": "en-ready", "missing_fields": []})
        self.assertEqual(payload["practical_items"], [{"key": "city", "value": "Lille"}])
        self.assertEqual(payload["image_summary"]["has_hero"], True)
        self.assertEqual(payload["readiness"]["ok_count"], 8)

    def test_social_queue_renders_terminal_readable_table(self):
        output = render_social_queue([
            SocialQueueItem("demo", "Titre FR", "Title EN", "en-ready", "ready", True, "candidate"),
            SocialQueueItem("draft", "Brouillon", "", "fr-only", "needs review", True, "needs-review"),
        ])

        self.assertIn("Social publication queue", output)
        self.assertIn("Articles checked: 2", output)
        self.assertIn("candidate: 1", output)
        self.assertIn("needs-review: 1", output)
        self.assertIn("Queue", output)
        self.assertIn("Title FR", output)
        self.assertIn("Reasons", output)
        self.assertIn("demo", output)
        self.assertIn("yes", output)

    def test_social_queue_json_renders_structured_payload(self):
        output = render_social_queue_json([
            SocialQueueItem("demo", "Titre FR", "Title EN", "en-ready", "ready", True, "candidate"),
        ])

        payload = json.loads(output)

        self.assertEqual(payload["summary"]["total"], 1)
        self.assertEqual(payload["summary"]["candidate"], 1)
        self.assertEqual(payload["items"][0]["slug"], "demo")
        self.assertEqual(payload["items"][0]["queue_status"], "candidate")
        self.assertEqual(payload["items"][0]["reasons"], [])

    def test_social_next_renders_terminal_readable_summary(self):
        output = render_social_next(
            SocialQueueItem("demo", "Titre FR", "Title EN", "en-ready", "ready", True, "candidate")
        )

        self.assertIn("Social next article", output)
        self.assertIn("Queue status: candidate", output)
        self.assertIn("Slug: demo", output)
        self.assertIn("Title FR: Titre FR", output)
        self.assertIn("Reasons:", output)
        self.assertIn("Brief command: python -m tools.editorial_manager social-brief demo", output)

    def test_social_next_renders_empty_state(self):
        output = render_social_next(None)

        self.assertIn("Social next article", output)
        self.assertIn("No matching article found.", output)

    def test_social_next_json_renders_simple_payload(self):
        output = render_social_next_json(
            SocialQueueItem("demo", "Titre FR", "Title EN", "en-ready", "ready", True, "candidate")
        )

        payload = json.loads(output)

        self.assertEqual(payload["next"]["slug"], "demo")
        self.assertEqual(payload["next"]["queue_status"], "candidate")
        self.assertEqual(payload["next"]["reasons"], [])


if __name__ == "__main__":
    unittest.main()
