import unittest

from tools.editorial_manager.checks import check_article, check_articles, publication_check_article, publication_check_articles


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

    def test_publication_check_complete_ready_article_has_only_ok_items(self):
        article = {
            "schema_version": 2,
            "slug": "demo",
            "status": "ready",
            "format": "long",
            "publication": {"order": 1},
            "media": {"hero": {"src": "assets/images/demo.png"}},
            "content": {
                "fr": {
                    "title": "Demo",
                    "dek": "Demo dek.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Demo meta."},
                    "media": {"hero_alt": "Demo alt."},
                },
                "en": {"title": "Demo"},
            },
        }

        items = publication_check_article(article)

        self.assertTrue(items)
        self.assertTrue(all(item.status == "OK" for item in items))

    def test_publication_check_reports_missing_publication_fields(self):
        items = publication_check_article({"slug": "demo", "format": "long"})
        errors = [item.code for item in items if item.status == "ERROR"]
        warnings = [item.code for item in items if item.status == "WARNING"]

        self.assertIn("title-fr", errors)
        self.assertIn("dek-fr", errors)
        self.assertIn("meta-description-fr", errors)
        self.assertIn("hero-image", errors)
        self.assertIn("hero-alt-fr", errors)
        self.assertIn("sections-fr", errors)
        self.assertIn("publication-order", errors)
        self.assertIn("publication-status", warnings)
        self.assertIn("content-en", warnings)

    def test_publication_check_treats_empty_english_as_warning(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {}},
        }

        items = publication_check_article(article)

        self.assertIn("content-en", [item.code for item in items if item.status == "WARNING"])

    def test_publication_check_articles_collects_items_for_all_articles(self):
        items = publication_check_articles([
            {"slug": "one", "status": "ready"},
            {"slug": "two", "status": "unknown-status"},
        ])

        self.assertEqual({item.slug for item in items}, {"one", "two"})
        self.assertIn("publication-status", [item.code for item in items if item.status == "ERROR"])


if __name__ == "__main__":
    unittest.main()
