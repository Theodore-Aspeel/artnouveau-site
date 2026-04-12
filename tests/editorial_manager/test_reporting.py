import unittest

from tools.editorial_manager.reporting import render_summary


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


if __name__ == "__main__":
    unittest.main()
