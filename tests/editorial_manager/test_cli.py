import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tools.editorial_manager.cli import main


class CliTests(unittest.TestCase):
    def test_locale_report_slug_command_runs(self):
        article = {
            "slug": "demo",
            "schema_version": 2,
            "content": {
                "fr": {
                    "title": "Demo",
                    "dek": "Demo dek.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Demo meta."},
                    "media": {"hero_alt": "Demo alt."},
                },
                "en": {
                    "title": "Demo",
                    "dek": "Demo dek.",
                    "sections": [{"heading": "A", "body": "B"}],
                    "seo": {"meta_description": "Demo meta."},
                    "media": {"hero_alt": "Demo alt."},
                },
            },
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["locale-report", "demo"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Locale report", output.getvalue())
        self.assertIn("en-ready", output.getvalue())

    def test_publication_check_slug_command_runs(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo"}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["publication-check", "demo"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Publication checklist", output.getvalue())
        self.assertIn("Articles checked: 1", output.getvalue())

    def test_social_brief_slug_command_runs(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo EN", "dek": "Demo dek EN."}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-brief", "demo"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Social publication brief", output.getvalue())
        self.assertIn("Slug: demo", output.getvalue())
        self.assertIn("Title EN: Demo EN", output.getvalue())

    def test_social_brief_json_command_runs(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo EN", "dek": "Demo dek EN."}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-brief", "demo", "--json"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["slug"], "demo")
        self.assertEqual(payload["title_en"], "Demo EN")
        self.assertIn("locale_status", payload)
        self.assertIn("image_summary", payload)
        self.assertIn("readiness", payload)

    def test_social_caption_command_runs(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "city": "Lille",
            "style": "Art Nouveau",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo EN", "dek": "Demo dek EN."}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-caption", "demo"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Social caption proposal", output.getvalue())
        self.assertIn("Slug: demo", output.getvalue())
        self.assertIn("Hook: À découvrir: Demo", output.getvalue())
        self.assertIn("#ArtNouveau #Lille", output.getvalue())

    def test_social_caption_json_command_accepts_locale(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "city": "Lille",
            "style": "Art Nouveau",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo EN", "dek": "Demo dek EN."}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-caption", "demo", "--locale", "en", "--json"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["slug"], "demo")
        self.assertEqual(payload["requested_locale"], "en")
        self.assertEqual(payload["source_locale"], "en")
        self.assertEqual(payload["title"], "Demo EN")
        self.assertEqual(payload["cta"], "Read the article on the site.")

    def test_social_package_command_outputs_json_payload(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "city": "Lille",
            "style": "Art Nouveau",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo EN", "dek": "Demo dek EN."}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-package", "demo", "--locale", "en"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["slug"], "demo")
        self.assertEqual(payload["requested_locale"], "en")
        self.assertEqual(payload["source_locale"], "en")
        self.assertIn("brief", payload)
        self.assertIn("caption", payload)
        self.assertIn("image_summary", payload)
        self.assertIn("readiness", payload)
        self.assertIn("reasons", payload)

    def test_social_queue_command_runs(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo EN", "dek": "Demo dek EN."}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-queue"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Social publication queue", output.getvalue())
        self.assertIn("Articles checked: 1", output.getvalue())
        self.assertIn("demo", output.getvalue())

    def test_social_queue_json_command_runs(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo EN", "dek": "Demo dek EN."}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-queue", "--json"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["total"], 1)
        self.assertEqual(payload["items"][0]["slug"], "demo")
        self.assertIn("queue_status", payload["items"][0])

    def test_social_queue_json_command_accepts_filters(self):
        articles = [
            {
                "slug": "candidate",
                "status": "ready",
                "format": "long",
                "publication": {"order": 1},
                "media": {"hero": {"src": "assets/images/candidate.png"}},
                "content": {
                    "fr": {
                        "title": "Candidat",
                        "dek": "Dek FR.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta FR."},
                        "media": {"hero_alt": "Alt FR."},
                    },
                    "en": {
                        "title": "Candidate",
                        "dek": "Dek EN.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta EN."},
                        "media": {"hero_alt": "Alt EN."},
                    },
                },
            },
            {
                "slug": "blocked",
                "status": "ready",
                "format": "long",
                "publication": {"order": 2},
                "media": {"hero": {"src": ""}},
                "content": {
                    "fr": {
                        "title": "Bloque",
                        "dek": "Dek FR.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta FR."},
                        "media": {"hero_alt": "Alt FR."},
                    },
                    "en": {},
                },
            },
        ]
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=articles):
            with redirect_stdout(output):
                exit_code = main([
                    "social-queue",
                    "--status",
                    "candidate",
                    "--locale-status",
                    "en-ready",
                    "--has-hero",
                    "yes",
                    "--limit",
                    "1",
                    "--json",
                ])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["total"], 1)
        self.assertEqual(payload["items"][0]["slug"], "candidate")
        self.assertEqual(payload["items"][0]["queue_status"], "candidate")

    def test_social_next_command_runs(self):
        articles = [
            {
                "slug": "blocked",
                "status": "ready",
                "format": "long",
                "publication": {"order": 1},
                "media": {"hero": {"src": ""}},
                "content": {
                    "fr": {
                        "title": "Bloque",
                        "dek": "Dek FR.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta FR."},
                        "media": {"hero_alt": "Alt FR."},
                    },
                    "en": {},
                },
            },
            {
                "slug": "candidate",
                "status": "ready",
                "format": "long",
                "publication": {"order": 2},
                "media": {"hero": {"src": "assets/images/candidate.png"}},
                "content": {
                    "fr": {
                        "title": "Candidat",
                        "dek": "Dek FR.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta FR."},
                        "media": {"hero_alt": "Alt FR."},
                    },
                    "en": {
                        "title": "Candidate",
                        "dek": "Dek EN.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta EN."},
                        "media": {"hero_alt": "Alt EN."},
                    },
                },
            },
        ]
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=articles):
            with redirect_stdout(output):
                exit_code = main(["social-next"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Social next article", output.getvalue())
        self.assertIn("Slug: candidate", output.getvalue())
        self.assertIn("Queue status: candidate", output.getvalue())

    def test_social_next_json_command_accepts_filters(self):
        articles = [
            {
                "slug": "candidate",
                "status": "ready",
                "format": "long",
                "publication": {"order": 1},
                "media": {"hero": {"src": "assets/images/candidate.png"}},
                "content": {
                    "fr": {
                        "title": "Candidat",
                        "dek": "Dek FR.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta FR."},
                        "media": {"hero_alt": "Alt FR."},
                    },
                    "en": {
                        "title": "Candidate",
                        "dek": "Dek EN.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta EN."},
                        "media": {"hero_alt": "Alt EN."},
                    },
                },
            },
            {
                "slug": "review",
                "status": "ready",
                "format": "long",
                "publication": {"order": 2},
                "media": {"hero": {"src": "assets/images/review.png"}},
                "content": {
                    "fr": {
                        "title": "A revoir",
                        "dek": "Dek FR.",
                        "sections": [{"heading": "A", "body": "B"}],
                        "seo": {"meta_description": "Meta FR."},
                        "media": {"hero_alt": "Alt FR."},
                    },
                    "en": {},
                },
            },
        ]
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=articles):
            with redirect_stdout(output):
                exit_code = main([
                    "social-next",
                    "--status",
                    "needs-review",
                    "--locale-status",
                    "fr-only",
                    "--json",
                ])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["next"]["slug"], "review")
        self.assertEqual(payload["next"]["queue_status"], "needs-review")


if __name__ == "__main__":
    unittest.main()
