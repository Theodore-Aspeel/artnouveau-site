import json
import os
from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.editor_store import (
    build_editor_article_payload,
    build_preview_urls,
    npm_executable,
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
                "practical_items": [
                    {"key": "city", "value": "Lille"},
                    {"key": "address", "value": "Rue de Demo"},
                ],
            },
            "en": {
                "title": "Demo EN",
                "dek": "Dek EN.",
                "epigraph": "Epigraph EN.",
                "sections": [{"heading": "Heading EN", "body": "Body EN."}],
                "seo": {"meta_description": "Meta EN."},
                "media": {"hero_alt": "Alt EN."},
                "around": {"note": "Around EN."},
                "practical_items": [
                    {"key": "city", "value": "Lille"},
                    {"key": "address", "value": "Demo Street"},
                ],
            },
        },
    }


class EditorStoreTests(unittest.TestCase):
    def test_editor_payload_contains_only_editable_fields(self):
        payload = build_editor_article_payload(sample_article(support=[{"src": VALID_SUPPORT_SRC}]))
        field_paths = [field["path"] for field in payload["fields"]]

        self.assertTrue(payload["image_options"])
        self.assertEqual(payload["preview_urls"]["fr"], "article.html?slug=demo")
        self.assertEqual(payload["preview_urls"]["en"], "article.html?slug=demo&previewLocale=en")
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
        self.assertIn("content.fr.practical_items.0.value", field_paths)
        self.assertIn("content.en.practical_items.1.value", field_paths)
        self.assertNotIn("slug", field_paths)
        self.assertNotIn("taxonomy.style_key", field_paths)
        self.assertNotIn("content.fr.sections", field_paths)
        self.assertNotIn("content.fr.practical_items", field_paths)
        self.assertNotIn("content.fr.practical_items.0.key", field_paths)

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

    def test_practical_item_fields_are_grouped_with_readonly_keys(self):
        payload = build_editor_article_payload(sample_article())
        fields = {field["path"]: field for field in payload["fields"]}

        self.assertEqual(fields["content.fr.practical_items.0.value"]["label"], "Ville (FR)")
        self.assertEqual(fields["content.fr.practical_items.0.value"]["group"], "Informations pratiques FR")
        self.assertEqual(fields["content.fr.practical_items.0.value"]["control"], "text")
        self.assertEqual(fields["content.fr.practical_items.0.value"]["readonly_key"], "city")
        self.assertTrue(fields["content.fr.practical_items.0.value"]["required"])
        self.assertEqual(fields["content.en.practical_items.1.value"]["label"], "Adresse (EN)")
        self.assertEqual(fields["content.en.practical_items.1.value"]["readonly_key"], "address")
        self.assertFalse(fields["content.en.practical_items.1.value"]["required"])

    def test_preview_urls_keep_encoded_slug_and_locale_parameter(self):
        urls = build_preview_urls("demo/lille ete")

        self.assertEqual(urls["fr"], "article.html?slug=demo%2Flille%20ete")
        self.assertEqual(urls["en"], "article.html?slug=demo%2Flille%20ete&previewLocale=en")

    def test_validate_changes_rejects_non_whitelisted_field(self):
        errors = validate_changes(sample_article(), [{"field": "slug", "value": "new-slug"}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_non_existing_section_index(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.sections.1.body", "value": "New section"}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_section_shape_change(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.sections", "value": []}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_practical_item_shape_change(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.practical_items", "value": []}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_practical_item_key_edit(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.practical_items.0.key", "value": "country"}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_new_practical_item_index(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.practical_items.2.value", "value": "New"}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_rejects_new_support_image_slot(self):
        errors = validate_changes(sample_article(), [{"field": "media.support.0.src", "value": VALID_SUPPORT_SRC}])

        self.assertEqual(errors[0]["code"], "field-not-editable")

    def test_validate_changes_reports_required_safe_field(self):
        errors = validate_changes(sample_article(), [{"field": "content.fr.title", "value": ""}])

        self.assertIn("required-field", [item["code"] for item in errors])
        self.assertIn(
            {"code": "required-field", "message": "Titre français is required.", "field": "content.fr.title"},
            errors,
        )

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

    def test_validate_then_save_flow_updates_json(self):
        changes = [{"field": "content.fr.title", "value": "Updated FR"}]
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            article = sample_article("assets/images/articles/current.png")
            write_payload(path, [article])

            validation_errors = validate_changes(article, changes, project_root=Path(directory))
            result = save_article_changes("demo", changes, path=path, validator=lambda: (True, []))
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(validation_errors, [])
        self.assertTrue(result["ok"])
        self.assertEqual(payload["articles"][0]["content"]["fr"]["title"], "Updated FR")

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

    def test_save_article_changes_writes_existing_practical_item_values_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(path, [sample_article("assets/images/articles/current.png")])

            result = save_article_changes(
                "demo",
                [
                    {"field": "content.fr.practical_items.0.value", "value": "Roubaix"},
                    {"field": "content.en.practical_items.1.value", "value": "Updated street"},
                ],
                path=path,
                validator=lambda: (True, []),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        practical_fr = payload["articles"][0]["content"]["fr"]["practical_items"]
        practical_en = payload["articles"][0]["content"]["en"]["practical_items"]
        self.assertTrue(result["ok"])
        self.assertEqual(len(practical_fr), 2)
        self.assertEqual(len(practical_en), 2)
        self.assertEqual(practical_fr[0], {"key": "city", "value": "Roubaix"})
        self.assertEqual(practical_fr[1], {"key": "address", "value": "Rue de Demo"})
        self.assertEqual(practical_en[0], {"key": "city", "value": "Lille"})
        self.assertEqual(practical_en[1], {"key": "address", "value": "Updated street"})

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

    def test_save_article_changes_rolls_back_when_validation_cannot_run(self):
        with tempfile.TemporaryDirectory() as directory:
            path = temp_articles_path(directory)
            write_payload(path, [sample_article("assets/images/articles/current.png")])

            result = save_article_changes(
                "demo",
                [{"field": "content.fr.title", "value": "Updated FR"}],
                path=path,
                validator=lambda: (_ for _ in ()).throw(OSError("npm not found")),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(result["ok"])
        self.assertTrue(result["rolled_back"])
        self.assertEqual(result["errors"][0]["code"], "project-validation")
        self.assertIn("Project validation could not run", result["errors"][0]["message"])
        self.assertEqual(payload["articles"][0]["content"]["fr"]["title"], "Demo FR")

    def test_project_validation_uses_windows_npm_command(self):
        expected = "npm.cmd" if os.name == "nt" else "npm"

        self.assertEqual(npm_executable(), expected)


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
