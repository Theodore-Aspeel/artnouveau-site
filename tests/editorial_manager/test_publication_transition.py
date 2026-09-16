import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from tools.editorial_manager.publication_transition import publish_article


def accept_all_images(assets, _project_root):
    return {src: True for src in assets}


def ready_article(status="draft", nl_ready=True):
    locale = {
        "title": "Demo",
        "dek": "Demo dek.",
        "sections": [{"heading": "Section", "body": "Body."}],
        "seo": {"meta_description": "Demo description."},
        "media": {"hero_alt": "Demo photograph."},
        "practical_items": [],
    }
    return {
        "schema_version": 2,
        "slug": "demo",
        "status": status,
        "format": "long",
        "publication": {"order": 1, "published_on": None, "updated_on": None},
        "media": {"hero": {"src": "assets/images/demo.png"}},
        "content": {"fr": dict(locale), "en": dict(locale), "nl": dict(locale) if nl_ready else {}},
    }


def rights_registry():
    return {
        "contract": {"name": "artnouveau.media_rights", "version": 1},
        "collections": [
            {
                "id": "fixture",
                "creator": "Christophe Aspel",
                "rights_holder": "Christophe Aspel",
                "public_credit": "Photographie : Christophe Aspel",
                "source_type": "original_photography",
                "rights_status": "cleared",
                "confirmed_on": "2026-09-15",
                "confirmation_basis": "project_owner_statement",
                "assets": ["assets/images/demo.png"],
            }
        ],
    }


def fixture_path(root: Path, article=None) -> Path:
    path = root / "src/data/articles.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"articles": [article or ready_article()]}), encoding="utf-8")
    image = root / "src/assets/images/demo.png"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"fixture")
    return path


class PublicationTransitionTests(unittest.TestCase):
    def test_dry_run_is_ready_without_changing_source(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture_path(Path(directory))
            original = path.read_text(encoding="utf-8")
            result = publish_article(
                "demo",
                "2026-09-16",
                rights_registry(),
                path=path,
                image_probe=accept_all_images,
                today=date(2026, 9, 16),
            )

            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertFalse((Path(directory) / ".editor-backups").exists())

        self.assertTrue(result.ok)
        self.assertEqual(result.status, "ready-for-human-approval")
        self.assertEqual(result.status_after, "published")
        self.assertFalse(result.written)
        self.assertEqual(result.locale_statuses, {"en": "en-ready", "nl": "nl-ready"})

    def test_write_requires_explicit_human_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture_path(Path(directory))
            result = publish_article(
                "demo",
                "2026-09-16",
                rights_registry(),
                path=path,
                write=True,
                image_probe=accept_all_images,
                today=date(2026, 9, 16),
            )

        self.assertFalse(result.ok)
        self.assertTrue(any("approval-required" in reason for reason in result.reasons))

    def test_approved_write_sets_status_and_date_and_creates_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = fixture_path(root)
            result = publish_article(
                "demo",
                "2026-09-16",
                rights_registry(),
                path=path,
                write=True,
                approved=True,
                validator=lambda: (True, []),
                image_probe=accept_all_images,
                today=date(2026, 9, 16),
            )
            saved = json.loads(path.read_text(encoding="utf-8"))["articles"][0]

            self.assertTrue((root / result.backup["path"]).is_file())

        self.assertTrue(result.ok)
        self.assertTrue(result.written)
        self.assertEqual(saved["status"], "published")
        self.assertEqual(saved["publication"]["published_on"], "2026-09-16")

    def test_failed_project_validation_rolls_back(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture_path(Path(directory))
            result = publish_article(
                "demo",
                "2026-09-16",
                rights_registry(),
                path=path,
                write=True,
                approved=True,
                validator=lambda: (False, ["Validation failed."]),
                image_probe=accept_all_images,
                today=date(2026, 9, 16),
            )
            saved = json.loads(path.read_text(encoding="utf-8"))["articles"][0]

        self.assertFalse(result.ok)
        self.assertTrue(result.rolled_back)
        self.assertEqual(saved["status"], "draft")
        self.assertIsNone(saved["publication"]["published_on"])

    def test_incomplete_dutch_locale_blocks_transition(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture_path(Path(directory), ready_article(nl_ready=False))
            result = publish_article(
                "demo",
                "2026-09-16",
                rights_registry(),
                path=path,
                image_probe=accept_all_images,
                today=date(2026, 9, 16),
            )

        self.assertFalse(result.ok)
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any("locale-nl" in reason for reason in result.reasons))

    def test_invalid_or_future_date_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture_path(Path(directory))
            invalid = publish_article(
                "demo", "2026-02-31", rights_registry(), path=path, today=date(2026, 9, 16)
            )
            future = publish_article(
                "demo", "2026-09-17", rights_registry(), path=path, today=date(2026, 9, 16)
            )

        self.assertFalse(invalid.ok)
        self.assertFalse(future.ok)
        self.assertTrue(any("future" in reason for reason in future.reasons))

    def test_published_article_cannot_be_republished(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture_path(Path(directory), ready_article(status="published"))
            result = publish_article(
                "demo", "2026-09-16", rights_registry(), path=path, today=date(2026, 9, 16)
            )

        self.assertFalse(result.ok)
        self.assertTrue(any("must be draft or ready" in reason for reason in result.reasons))

    def test_payload_contract_is_versioned(self):
        with tempfile.TemporaryDirectory() as directory:
            path = fixture_path(Path(directory))
            result = publish_article(
                "demo",
                "2026-09-16",
                rights_registry(),
                path=path,
                image_probe=accept_all_images,
                today=date(2026, 9, 16),
            )

        self.assertEqual(
            result.to_payload()["contract"],
            {"name": "artnouveau.publication_transition", "version": 1},
        )


if __name__ == "__main__":
    unittest.main()
