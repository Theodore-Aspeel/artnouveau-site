import unittest

from tools.editorial_manager.checks import CheckIssue, PublicationCheckItem
from tools.editorial_manager.reporting import render_check_report, render_publication_check_report, render_summary


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


if __name__ == "__main__":
    unittest.main()
