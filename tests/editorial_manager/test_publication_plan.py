import tempfile
import unittest
from pathlib import Path

from tools.editorial_manager.publication_plan import build_publication_plan


def accept_all_images(assets, _project_root):
    return {src: True for src in assets}


def article(slug: str, status: str, published_on=None):
    locale = {
        "title": slug,
        "dek": "Demo dek.",
        "sections": [{"heading": "Section", "body": "Body."}],
        "seo": {"meta_description": "Demo description."},
        "media": {"hero_alt": "Demo photograph."},
        "practical_items": [],
    }
    return {
        "schema_version": 2,
        "slug": slug,
        "status": status,
        "format": "long",
        "publication": {"order": 1, "published_on": published_on},
        "media": {"hero": {"src": f"assets/images/{slug}.png"}},
        "content": {"fr": dict(locale), "en": dict(locale)},
    }


def registry(*assets: str):
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
                "assets": list(assets),
            }
        ],
    }


def write_asset(root: Path, slug: str) -> None:
    asset = root / f"src/assets/images/{slug}.png"
    asset.parent.mkdir(parents=True, exist_ok=True)
    asset.write_bytes(b"fixture")


class PublicationPlanTests(unittest.TestCase):
    def test_draft_is_visible_now_but_hidden_in_strict_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            write_asset(Path(directory), "draft-demo")
            report = build_publication_plan(
                [article("draft-demo", "draft")],
                registry("assets/images/draft-demo.png"),
                project_root=Path(directory),
                image_probe=accept_all_images,
            )

        item = report.items[0]
        self.assertEqual(item.current_visibility, "visible")
        self.assertEqual(item.strict_visibility, "hidden")
        self.assertEqual(item.transition, "would-hide")
        self.assertEqual(report.activation_status, "blocked")
        self.assertEqual(report.summary["would_hide"], 1)

    def test_ready_published_article_allows_human_activation(self):
        with tempfile.TemporaryDirectory() as directory:
            write_asset(Path(directory), "published-demo")
            report = build_publication_plan(
                [article("published-demo", "published", "2026-09-16")],
                registry("assets/images/published-demo.png"),
                project_root=Path(directory),
                image_probe=accept_all_images,
            )

        self.assertEqual(report.activation_status, "ready-for-human-activation")
        self.assertEqual(report.summary["strict_visible"], 1)
        self.assertEqual(report.items[0].transition, "unchanged")
        self.assertEqual(report.human_approval, "required")

    def test_published_article_requires_valid_publication_date(self):
        with tempfile.TemporaryDirectory() as directory:
            write_asset(Path(directory), "published-demo")
            report = build_publication_plan(
                [article("published-demo", "published", "2026-02-31")],
                registry("assets/images/published-demo.png"),
                project_root=Path(directory),
                image_probe=accept_all_images,
            )

        self.assertEqual(report.activation_status, "blocked")
        self.assertTrue(any("published-on" in reason for reason in report.items[0].reasons))

    def test_payload_has_versioned_read_only_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            write_asset(Path(directory), "demo")
            report = build_publication_plan(
                [article("demo", "draft")],
                registry("assets/images/demo.png"),
                project_root=Path(directory),
                image_probe=accept_all_images,
            )

        payload = report.to_payload()
        self.assertEqual(payload["contract"], {"name": "artnouveau.publication_plan", "version": 1})
        self.assertTrue(payload["read_only"])
        self.assertEqual(payload["candidate_policy"], "published-only")
        self.assertEqual(payload["human_approval"], "required")


if __name__ == "__main__":
    unittest.main()
