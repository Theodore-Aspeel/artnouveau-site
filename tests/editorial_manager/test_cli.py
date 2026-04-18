import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tools.editorial_manager.cli import main


class CliTests(unittest.TestCase):
    def test_editor_command_starts_local_server(self):
        with patch("tools.editorial_manager.cli.run_editor_server") as run_editor_server:
            exit_code = main(["editor", "--host", "127.0.0.1", "--port", "9000", "--no-browser"])

        self.assertEqual(exit_code, 0)
        run_editor_server.assert_called_once_with("127.0.0.1", 9000, open_browser=False)

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

    def test_locale_report_accepts_prepared_nl_target(self):
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
                "en": {},
            },
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["locale-report", "demo", "--locale", "nl"])

        self.assertEqual(exit_code, 0)
        self.assertIn("fr-only", output.getvalue())

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

    def test_social_caption_json_accepts_internal_nl_preview_locale(self):
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
                exit_code = main(["social-caption", "demo", "--locale", "nl", "--json"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["requested_locale"], "nl")
        self.assertEqual(payload["source_locale"], "fr")

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

    def test_social_package_next_outputs_first_matching_package(self):
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
                exit_code = main(["social-package", "--next", "--locale", "en"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["slug"], "candidate")
        self.assertEqual(payload["requested_locale"], "en")
        self.assertEqual(payload["source_locale"], "en")
        self.assertEqual(payload["queue_status"], "candidate")
        self.assertIn("brief", payload)
        self.assertIn("caption", payload)
        self.assertIn("image_summary", payload)
        self.assertIn("readiness", payload)
        self.assertIn("reasons", payload)

    def test_social_package_next_accepts_queue_filters(self):
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
                    "social-package",
                    "--next",
                    "--status",
                    "needs-review",
                    "--locale-status",
                    "fr-only",
                    "--has-hero",
                    "yes",
                ])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["slug"], "review")
        self.assertEqual(payload["source_locale"], "fr")
        self.assertEqual(payload["queue_status"], "needs-review")
        self.assertEqual(payload["locale_status"]["status"], "fr-only")
        self.assertIn("English content is missing.", payload["reasons"])

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

    def test_social_workflow_command_outputs_local_handoff(self):
        article = {
            "slug": "candidate",
            "status": "ready",
            "format": "long",
            "publication": {"order": 1},
            "media": {"hero": {"src": "assets/images/candidate.png"}},
            "facts": {"location": {"city": "Lille"}},
            "taxonomy": {"style_key": "art-nouveau"},
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
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["social-workflow", "--locale", "en"])

        rendered = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Local social workflow", rendered)
        self.assertIn("Slug: candidate", rendered)
        self.assertIn("Caption draft:", rendered)
        self.assertIn("Hero src: assets/images/candidate.png", rendered)
        self.assertIn(
            "python -m tools.editorial_manager social-package candidate --locale en",
            rendered,
        )


if __name__ == "__main__":
    unittest.main()
