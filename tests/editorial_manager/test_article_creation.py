import json
from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.article_creation import (
    ArticleCreationInput,
    build_article,
    create_article,
    next_order,
    validate_creation_input,
)


VALID_HERO_SRC = "assets/images/articles/current.png"


def creation_input(**overrides):
    values = {
        "slug": "nouvel-article-demo",
        "title_fr": "Nouvel article demo",
        "dek_fr": "Un court chapeau de travail pour demarrer l'article.",
        "epigraph_fr": "Une phrase d'ouverture claire.",
        "meta_description_fr": "Description SEO francaise du nouvel article.",
        "hero_alt_fr": "Facade du nouvel article.",
        "section_heading_fr": "Un premier regard",
        "section_body_fr": "Un premier paragraphe assez clair pour valider la base editoriale.",
        "hero_src": VALID_HERO_SRC,
        "city": "Lille",
        "country": "France",
        "style_key": "art_nouveau",
        "architect": "Architecte Demo",
        "address": "1 rue Demo",
        "date": "1904",
    }
    values.update(overrides)
    return ArticleCreationInput(**values)


class ArticleCreationTests(unittest.TestCase):
    def test_build_article_creates_minimal_v2_draft_with_empty_target_locales(self):
        article = build_article(creation_input(tag_keys=("facade",)), order=15)

        self.assertEqual(article["schema_version"], 2)
        self.assertEqual(article["id"], "nouvel-article-demo")
        self.assertEqual(article["slug"], "nouvel-article-demo")
        self.assertEqual(article["status"], "draft")
        self.assertEqual(article["publication"]["order"], 15)
        self.assertEqual(article["media"]["hero"]["src"], VALID_HERO_SRC)
        self.assertEqual(article["taxonomy"]["tag_keys"], ["art_nouveau", "facade"])
        self.assertEqual(article["content"]["fr"]["title"], "Nouvel article demo")
        self.assertEqual(article["content"]["fr"]["sections"][0]["heading"], "Un premier regard")
        self.assertEqual(article["content"]["en"]["title"], "")
        self.assertEqual(article["content"]["nl"]["sections"][0]["body"], "")
        self.assertEqual(
            article["content"]["fr"]["practical_items"],
            [
                {"key": "city", "value": "Lille"},
                {"key": "country", "value": "France"},
                {"key": "style", "value": "Art Nouveau"},
                {"key": "architect", "value": "Architecte Demo"},
                {"key": "address", "value": "1 rue Demo"},
                {"key": "date", "value": "1904"},
            ],
        )

    def test_validate_creation_input_rejects_duplicate_slug_and_bad_order(self):
        existing = [{"slug": "nouvel-article-demo", "publication": {"order": 4}}]

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_articles_path(root)
            make_image(root)
            errors = validate_creation_input(creation_input(order=4), existing, root)

        self.assertIn("slug already exists: nouvel-article-demo.", errors)
        self.assertIn("publication order already exists: 4.", errors)

    def test_validate_creation_input_rejects_missing_required_visible_field(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_articles_path(root)
            make_image(root)
            errors = validate_creation_input(creation_input(title_fr=""), [], root)

        self.assertIn("title_fr is required.", errors)

    def test_validate_creation_input_rejects_missing_image_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_articles_path(root)

            errors = validate_creation_input(creation_input(), [], root)

        self.assertIn("hero_src must be an existing image under src/assets/images.", errors)

    def test_create_article_dry_run_does_not_write_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = make_articles_path(root)
            make_image(root)

            result = create_article(creation_input(), path=path, write=False)
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(result.ok)
        self.assertFalse(result.written)
        self.assertEqual(payload["articles"], [])
        self.assertEqual(result.article["publication"]["order"], 1)

    def test_create_article_writes_and_runs_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = make_articles_path(root, [{"slug": "existing", "publication": {"order": 2}}])
            make_image(root)

            result = create_article(creation_input(), path=path, write=True, validator=lambda: (True, []))
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(result.ok)
        self.assertTrue(result.written)
        self.assertEqual(len(payload["articles"]), 2)
        self.assertEqual(payload["articles"][1]["slug"], "nouvel-article-demo")
        self.assertEqual(payload["articles"][1]["publication"]["order"], 3)

    def test_create_article_rolls_back_when_validation_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = make_articles_path(root)
            make_image(root)

            result = create_article(
                creation_input(),
                path=path,
                write=True,
                validator=lambda: (False, ["Validation failed."]),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(result.ok)
        self.assertTrue(result.rolled_back)
        self.assertEqual(result.errors, ("Validation failed.",))
        self.assertEqual(payload["articles"], [])

    def test_next_order_uses_current_maximum_order(self):
        self.assertEqual(next_order([{"publication": {"order": 2}}, {"publication": {"order": 7}}]), 8)


def make_articles_path(root: Path, articles=None) -> Path:
    path = root / "src" / "data" / "articles.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"articles": articles or []}, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def make_image(root: Path) -> None:
    image_path = root / "src" / VALID_HERO_SRC
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(b"fake image")


if __name__ == "__main__":
    unittest.main()
