import tempfile
import unittest
from pathlib import Path

from tools.editorial_manager.publication_gate import build_publication_gate


def accept_all_images(assets, _project_root):
    return {src: True for src in assets}


def ready_article(status: str = "ready"):
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
        "publication": {"order": 1},
        "media": {"hero": {"src": "assets/images/demo.png"}},
        "content": {"fr": dict(locale), "en": dict(locale)},
    }


def rights_registry(*assets: str):
    return {
        "contract": {"name": "artnouveau.media_rights", "version": 1},
        "collections": [
            {
                "id": "fixture",
                "creator": "Fixture Photographer",
                "rights_holder": "Fixture Photographer",
                "public_credit": "Photographie : Fixture Photographer",
                "source_type": "original_photography",
                "rights_status": "cleared",
                "confirmed_on": "2026-09-15",
                "confirmation_basis": "project_owner_statement",
                "assets": list(assets),
            }
        ],
    }


class PublicationGateTests(unittest.TestCase):
    def test_ready_article_reaches_human_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "src/assets/images/demo.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"fixture")

            report = build_publication_gate(
                ready_article(),
                rights_registry("assets/images/demo.png"),
                project_root=root,
                image_probe=accept_all_images,
            )

        self.assertTrue(report.ok)
        self.assertEqual(report.status, "ready-for-human-review")
        self.assertEqual(report.human_approval, "required")
        self.assertEqual(report.reasons, ())
        self.assertEqual(set(report.preview_urls), {"fr", "en", "nl"})

    def test_draft_never_reaches_ready_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "src/assets/images/demo.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"fixture")

            report = build_publication_gate(
                ready_article(status="draft"),
                rights_registry("assets/images/demo.png"),
                project_root=root,
                image_probe=accept_all_images,
            )

        self.assertFalse(report.ok)
        self.assertEqual(report.status, "needs-review")
        self.assertTrue(any("publication-status" in reason for reason in report.reasons))

    def test_missing_rights_record_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            report = build_publication_gate(
                ready_article(),
                rights_registry(),
                project_root=Path(directory),
                image_probe=accept_all_images,
            )

        self.assertFalse(report.ok)
        self.assertEqual(report.status, "blocked")
        self.assertTrue(any("missing-rights-record" in reason for reason in report.reasons))

    def test_payload_has_stable_contract_and_human_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            report = build_publication_gate(
                ready_article(),
                rights_registry(),
                project_root=Path(directory),
                image_probe=accept_all_images,
            )

        payload = report.to_payload()
        self.assertEqual(payload["contract"], {"name": "artnouveau.publication_gate", "version": 1})
        self.assertEqual(payload["human_approval"], "required")
        self.assertEqual(payload["project_quality_gate"], "required-separately")
        self.assertIn("media_rights", payload)
        self.assertIn("publication_checks", payload)


if __name__ == "__main__":
    unittest.main()
