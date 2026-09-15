import tempfile
import unittest
from pathlib import Path

from tools.editorial_manager.media_rights import check_media_rights, collect_runtime_assets


def accept_all_images(assets, _project_root):
    return {src: True for src in assets}


def registry_for(*assets: str, status: str = "cleared"):
    return {
        "contract": {"name": "artnouveau.media_rights", "version": 1},
        "collections": [
            {
                "id": "fixture",
                "creator": "Fixture Photographer",
                "rights_holder": "Fixture Photographer",
                "public_credit": "Photographie : Fixture Photographer",
                "source_type": "original_photography",
                "rights_status": status,
                "confirmed_on": "2026-09-15",
                "confirmation_basis": "project_owner_statement",
                "assets": list(assets),
            }
        ],
    }


class MediaRightsTests(unittest.TestCase):
    def test_cleared_runtime_asset_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "src/assets/images/demo.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"fixture")

            report = check_media_rights(
                ["assets/images/demo.png"],
                registry_for("assets/images/demo.png"),
                project_root=root,
                image_probe=accept_all_images,
            )

        self.assertTrue(report.ok)
        self.assertEqual(report.status, "ready")
        self.assertEqual(report.cleared_count, 1)

    def test_unknown_runtime_asset_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            report = check_media_rights(
                ["assets/images/unknown.png"],
                registry_for(),
                project_root=Path(directory),
            )

        self.assertFalse(report.ok)
        self.assertIn("missing-rights-record", [issue.code for issue in report.issues])

    def test_non_cleared_asset_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "src/assets/images/demo.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"fixture")

            report = check_media_rights(
                ["assets/images/demo.png"],
                registry_for("assets/images/demo.png", status="pending"),
                project_root=root,
                image_probe=accept_all_images,
            )

        self.assertFalse(report.ok)
        self.assertIn("rights-not-cleared", [issue.code for issue in report.issues])

    def test_duplicate_registry_record_blocks(self):
        registry = registry_for("assets/images/demo.png", "assets/images/demo.png")
        report = check_media_rights([], registry)

        self.assertFalse(report.ok)
        self.assertIn("duplicate-rights-record", [issue.code for issue in report.issues])

    def test_shared_article_image_is_collected_once(self):
        articles = [
            {"media": {"hero": {"src": "assets/images/shared.png"}}},
            {"media": {"hero": {"src": "assets/images/shared.png"}}},
        ]

        with tempfile.TemporaryDirectory() as directory:
            assets = collect_runtime_assets(articles, Path(directory))

        self.assertEqual(assets, ["assets/images/shared.png"])

    def test_v1_support_image_object_is_collected(self):
        article = {
            "hero_image": "assets/images/hero.png",
            "support_images": [{"src": "assets/images/support.png"}],
        }

        with tempfile.TemporaryDirectory() as directory:
            assets = collect_runtime_assets([article], Path(directory))

        self.assertEqual(assets, ["assets/images/hero.png", "assets/images/support.png"])

    def test_static_image_path_with_spaces_is_collected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "src/pages/index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<img src="../assets/images/site/photo avec espace.png">',
                encoding="utf-8",
            )

            assets = collect_runtime_assets([], root)

        self.assertEqual(assets, ["assets/images/site/photo avec espace.png"])

    def test_corrupted_image_content_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "src/assets/images/demo.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"not a real png")

            report = check_media_rights(
                ["assets/images/demo.png"],
                registry_for("assets/images/demo.png"),
                project_root=root,
            )

        self.assertFalse(report.ok)
        self.assertIn("invalid-image-content", [issue.code for issue in report.issues])

    def test_registry_is_not_under_public_runtime(self):
        self.assertTrue(Path("research/media-rights.json").is_file())
        self.assertFalse(Path("src/data/media-rights.json").exists())
        self.assertFalse(Path("dist/data/media-rights.json").exists())


if __name__ == "__main__":
    unittest.main()
