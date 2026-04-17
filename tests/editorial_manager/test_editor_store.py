import json
from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.editor_store import (
    build_editor_article_payload,
    save_article_changes,
    validate_changes,
)


def sample_article():
    return {
        "schema_version": 2,
        "id": "demo",
        "slug": "demo",
        "status": "draft",
        "format": "long",
        "publication": {"order": 1},
        "media": {"hero": {"src": "assets/images/demo.png"}, "support": []},
        "content": {
            "fr": {
                "title": "Demo FR",
                "dek": "Dek FR.",
                "epigraph": "Epigraph FR.",
                "sections": [{"heading": "Heading FR", "body": "Body FR."}],
                "seo": {"meta_description": "Meta FR."},
                "media": {"hero_alt": "Alt FR."},
                "around": {"note": "Around FR."},
            },
            "en": {
                "title": "Demo EN",
                "dek": "Dek EN.",
                "epigraph": "Epigraph EN.",
                "sections": [{"heading": "Heading EN", "body": "Body EN."}],
                "seo": {"meta_description": "Meta EN."},
                "media": {"hero_alt": "Alt EN."},
                "around": {"note": "Around EN."},
            },
        },
    }


class EditorStoreTests(unittest.TestCase):
    def test_editor_payload_contains_only_editable_fields(self):
        payload = build_editor_article_payload(sample_article())
        field_paths = [field["path"] for field in payload["fields"]]

        self.assertIn("status", field_paths)
        self.assertIn("content.fr.title", field_paths)
        self.assertIn("content.en.media.hero_alt", field_paths)
        self.assertNotIn("slug", field_paths)
        self.assertNotIn("taxonomy.style_key", field_paths)
        self.assertNotIn("content.fr.sections", field_paths)

    def test_validate_changes_rejects_non_whitelisted_field(self):
        errors = validate_changes(sample_article(), [{"field": "slug", "value": "new-slug"}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_reports_required_safe_field(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.title", "value": ""}])

        self.assertIn("required-field", [item["code"] for item in errors])

    def test_save_article_changes_writes_allowed_field(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "articles.json"
            write_payload(path, [sample_article()])

            result = save_article_changes(
                "demo",
                [{"field": "content.fr.title", "value": "Updated FR"}],
                path=path,
                validator=lambda: (True, []),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(result["ok"])
        self.assertEqual(payload["articles"][0]["content"]["fr"]["title"], "Updated FR")
        self.assertEqual(payload["articles"][0]["slug"], "demo")

    def test_save_article_changes_rolls_back_when_validation_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "articles.json"
            write_payload(path, [sample_article()])

            result = save_article_changes(
                "demo",
                [{"field": "content.fr.title", "value": "Updated FR"}],
                path=path,
                validator=lambda: (False, ["Validation failed."]),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(result["ok"])
        self.assertTrue(result["rolled_back"])
        self.assertEqual(payload["articles"][0]["content"]["fr"]["title"], "Demo FR")


def write_payload(path: Path, articles):
    path.write_text(json.dumps({"articles": articles}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()

