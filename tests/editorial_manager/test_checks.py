import unittest

from tools.editorial_manager.checks import check_article, check_articles


class CheckTests(unittest.TestCase):
    def test_complete_v1_article_has_no_issues(self):
        article = {
            "slug": "demo",
            "title": "Demo",
            "hero_image": "assets/images/demo.png",
            "meta_description": "Demo meta.",
            "publication_order_recommended": 1,
        }

        self.assertEqual(check_article(article), [])

    def test_missing_required_editorial_fields_are_errors(self):
        issues = check_article({})

        self.assertEqual([issue.code for issue in issues[:4]], [
            "missing-slug",
            "missing-title-fr",
            "missing-hero-image",
            "missing-meta-description-fr",
        ])
        self.assertTrue(all(issue.severity == "ERROR" for issue in issues[:4]))

    def test_empty_v2_english_content_is_a_warning(self):
        article = {
            "schema_version": 2,
            "slug": "demo",
            "publication": {"order": 1},
            "media": {"hero": {"src": "assets/images/demo.png"}},
            "content": {
                "fr": {"title": "Demo", "seo": {"meta_description": "Demo meta."}},
                "en": {},
            },
        }

        issues = check_article(article)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "WARNING")
        self.assertEqual(issues[0].code, "missing-content-en")

    def test_missing_publication_order_is_a_warning(self):
        article = {
            "slug": "demo",
            "title": "Demo",
            "hero_image": "assets/images/demo.png",
            "meta_description": "Demo meta.",
        }

        issues = check_article(article)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "WARNING")
        self.assertEqual(issues[0].code, "missing-publication-order")

    def test_check_articles_collects_all_issues(self):
        issues = check_articles([
            {"slug": "one"},
            {
                "slug": "two",
                "title": "Two",
                "hero_image": "assets/images/two.png",
                "meta_description": "Two meta.",
                "publication_order_recommended": 2,
            },
        ])

        self.assertGreater(len(issues), 0)
        self.assertTrue(all(issue.slug == "one" for issue in issues))


if __name__ == "__main__":
    unittest.main()
