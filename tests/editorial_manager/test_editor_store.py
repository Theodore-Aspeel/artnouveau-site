import json
from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.editor_store import (
    build_editor_article_payload,
    save_article_changes,
    validate_changes,
)


VALID_HERO_SRC = "assets/images/articles/maison-coilliot-lille-hector-guimard.png"
VALID_SUPPORT_SRC = "assets/images/articles/lhuitriere-lille-art-deco.png"


def sample_article(hero_src=VALID_HERO_SRC, support=None):
    if support is None:
        support = []
    return {
        "schema_version": 2,
        "id": "demo",
        "slug": "demo",
        "status": "draft",
        "format": "long",
        "publication": {"order": 1},
        "media": {"hero": {"src": hero_src}, "support": support},
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
        payload = build_editor_article_payload(sample_article(support=[{"src": VALID_SUPPORT_SRC}]))
        field_paths = [field["path"] for field in payload["fields"]]

        self.assertTrue(payload["image_options"])
        self.assertIn(VALID_HERO_SRC, [image["src"] for image in payload["image_options"]])
        self.assertEqual(payload["support_images"], [{"index": 0, "src": VALID_SUPPORT_SRC}])
        self.assertIn("status", field_paths)
        self.assertIn("media.hero.src", field_paths)
        self.assertIn("media.support.0.src", field_paths)
        self.assertIn("content.fr.title", field_paths)
        self.assertIn("content.en.media.hero_alt", field_paths)
        self.assertIn("content.fr.sections.0.heading", field_paths)
        self.assertIn("content.fr.sections.0.body", field_paths)
        self.assertIn("content.en.sections.0.heading", field_paths)
        self.assertIn("content.en.sections.0.body", field_paths)
        self.assertNotIn("slug", field_paths)
        self.assertNotIn("taxonomy.style_key", field_paths)
        self.assertNotIn("content.fr.sections", field_paths)

    def test_section_fields_are_grouped_for_non_technical_editor(self):
        payload = build_editor_article_payload(sample_article(support=[{"src": VALID_SUPPORT_SRC}]))
        fields = {field["path"]: field for field in payload["fields"]}

        self.assertEqual(fields["media.hero.src"]["label"], "Image principale")
        self.assertEqual(fields["media.hero.src"]["group"], "Image principale")
        self.assertEqual(fields["media.hero.src"]["control"], "image-select")
        self.assertTrue(fields["media.hero.src"]["required"])
        self.assertEqual(fields["media.support.0.src"]["label"], "Image support 1")
        self.assertEqual(fields["media.support.0.src"]["group"], "Images support")
        self.assertEqual(fields["media.support.0.src"]["control"], "image-select")
        self.assertTrue(fields["media.support.0.src"]["required"])
        self.assertEqual(fields["content.fr.sections.0.heading"]["label"], "Section 1 - titre (FR)")
        self.assertEqual(fields["content.fr.sections.0.heading"]["group"], "Sections FR")
        self.assertEqual(fields["content.fr.sections.0.heading"]["control"], "text")
        self.assertEqual(fields["content.fr.sections.0.body"]["control"], "textarea")
        self.assertTrue(fields["content.fr.sections.0.body"]["required"])
        self.assertFalse(fields["content.en.sections.0.body"]["required"])

    def test_validate_changes_rejects_non_whitelisted_field(self):
        errors = validate_changes(sample_article(), [{"field": "slug", "value": "new-slug"}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_non_existing_section_index(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.sections.1.body", "value": "New section"}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_section_shape_change(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.sections", "value": []}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_new_support_image_slot(self):
        errors = validate_changes(sample_article(), [{"field": "media.support.0.src", "value": VALID_SUPPORT_SRC}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_reports_required_safe_field(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.title", "value": ""}])

        self.assertIn("required-field", [item["code"] for item in errors])

    def test_validate_changes_reports_required_french_section_body(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.sections.0.body", "value": ""}])

        self.assertIn("required-field", [item["code"] for item in errors])

    def test_validate_changes_rejects_invalid_hero_image_path(self):
        errors = validate_changes(sample_article(), [{"field": "media.hero.src", "value": "assets/images/missing.png"}])

        self.assertEqual(errors[0]["code"], "invalid-image")

    def test_validate_changes_rejects_invalid_support_image_path(self):
        article = sample_article(support=[{"src": VALID_SUPPORT_SRC}])

        errors = validate_changes(article, [{"field": "media.support.0.src", "value": "assets/images/missing.png"}])

        self.assertEqual(errors[0]["code"], "invalid-image")

    def test_save_article_changes_writes_allowed_field(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(path, [sample_article("assets/images/articles/current.png")])

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

    def test_save_article_changes_writes_existing_section_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(path, [sample_article("assets/images/articles/current.png")])

            result = save_article_changes(
                "demo",
                [
                    {"field": "content.fr.sections.0.heading", "value": "Updated heading FR"},
                    {"field": "content.en.sections.0.body", "value": "Updated body EN."},
                ],
                path=path,
                validator=lambda: (True, []),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        sections_fr = payload["articles"][0]["content"]["fr"]["sections"]
        sections_en = payload["articles"][0]["content"]["en"]["sections"]
        self.assertTrue(result["ok"])
        self.assertEqual(len(sections_fr), 1)
        self.assertEqual(len(sections_en), 1)
        self.assertEqual(sections_fr[0]["heading"], "Updated heading FR")
        self.assertEqual(sections_en[0]["body"], "Updated body EN.")

    def test_save_article_changes_writes_existing_hero_image_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(path, [sample_article("assets/images/articles/current.png")])

            result = save_article_changes(
                "demo",
                [{"field": "media.hero.src", "value": "assets/images/articles/replacement.png"}],
                path=path,
                validator=lambda: (True, []),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(result["ok"])
        self.assertEqual(payload["articles"][0]["media"]["hero"]["src"], "assets/images/articles/replacement.png")

    def test_save_article_changes_writes_existing_support_image_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(
                path,
                [
                    sample_article(
                        "assets/images/articles/current.png",
                        support=[
                            {"src": "assets/images/articles/current.png"},
                            {"src": "assets/images/articles/second.png"},
                        ],
                    )
                ],
            )

            result = save_article_changes(
                "demo",
                [{"field": "media.support.0.src", "value": "assets/images/articles/replacement.png"}],
                path=path,
                validator=lambda: (True, []),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        support = payload["articles"][0]["media"]["support"]
        self.assertTrue(result["ok"])
        self.assertEqual(len(support), 2)
        self.assertEqual(support[0]["src"], "assets/images/articles/replacement.png")
        self.assertEqual(support[1]["src"], "assets/images/articles/second.png")

    def test_save_article_changes_rejects_non_existing_hero_image_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(path, [sample_article("assets/images/articles/current.png")])

            result = save_article_changes(
                "demo",
                [{"field": "media.hero.src", "value": "assets/images/articles/missing.png"}],
                path=path,
                validator=lambda: (True, []),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["code"], "invalid-image")
        self.assertEqual(payload["articles"][0]["media"]["hero"]["src"], "assets/images/articles/current.png")

    def test_save_article_changes_rolls_back_when_validation_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(path, [sample_article("assets/images/articles/current.png")])

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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"articles": articles}, ensure_ascii=False, indent=2), encoding="utf-8")


def temp_articles_path(directory: str) -> Path:
    root = Path(directory)
    image_dir = root / "src" / "assets" / "images" / "articles"
    image_dir.mkdir(parents=True, exist_ok=True)
    (image_dir / "current.png").write_bytes(b"fake image")
    (image_dir / "replacement.png").write_bytes(b"fake image")
    (image_dir / "second.png").write_bytes(b"fake image")
    return root / "src" / "data" / "articles.json"


if __name__ == "__main__":
    unittest.main()
