import tempfile
import unittest
from pathlib import Path

from tools.editorial_manager.pipeline_status import build_pipeline_status, render_pipeline_status


def complete_article(status: str = "draft") -> dict:
    localized = lambda title, dek, epigraph, heading, alt, meta: {
        "title": title,
        "dek": dek,
        "epigraph": epigraph,
        "sections": [
            {"heading": heading, "body": "Body one."},
            {"heading": "Second heading", "body": "Body two."},
        ],
        "seo": {"meta_description": meta},
        "media": {"hero_alt": alt},
    }
    return {
        "schema_version": 2,
        "slug": "demo",
        "status": status,
        "format": "long",
        "publication": {"order": 1, "published_on": "2026-09-20" if status == "published" else None},
        "media": {"hero": {"src": "assets/images/demo.png"}, "support": []},
        "facts": {"location": {"city": "Lille", "country": "France"}},
        "taxonomy": {"style_key": "art_nouveau"},
        "content": {
            "fr": localized("Maison Demo", "Dek FR.", "Une façade change la rue.", "Lire la façade", "Alt FR.", "Meta FR."),
            "en": localized("Demo House", "Dek EN.", "A facade changes the street.", "Read the facade", "Alt EN.", "Meta EN."),
            "nl": localized("Demohuis", "Dek NL.", "Een gevel verandert de straat.", "Lees de gevel", "Alt NL.", "Meta NL."),
        },
    }


def rights_registry(status: str = "cleared") -> dict:
    return {
        "contract": {"name": "artnouveau.media_rights", "version": 1},
        "collections": [{
            "id": "fixture",
            "creator": "Christophe Aspel",
            "rights_holder": "Christophe Aspel",
            "public_credit": "Photographie : Christophe Aspel",
            "source_type": "original_photography",
            "rights_status": status,
            "confirmed_on": "2026-09-15",
            "confirmation_basis": "project_owner_statement",
            "assets": ["assets/images/demo.png"],
        }],
    }


def accept_all_images(assets, _project_root):
    return {src: True for src in assets}


class PipelineStatusTests(unittest.TestCase):
    def build(self, article=None, registry=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "src/assets/images/demo.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"fixture")
            return build_pipeline_status(
                article or complete_article(),
                registry or rights_registry(),
                project_root=root,
                image_probe=accept_all_images,
            )

    def test_draft_ready_article_points_to_human_publication_gate(self):
        payload = self.build()

        self.assertEqual(payload["contract"]["name"], "artnouveau.pipeline_status")
        self.assertEqual(payload["current_stage"], "publication")
        self.assertTrue(payload["human_action_required"])
        self.assertIn("real publication date", payload["next_action"])
        statuses = {stage["id"]: stage["status"] for stage in payload["stages"]}
        self.assertEqual(statuses["editorial_qa"], "ready")
        self.assertEqual(statuses["localization"], "ready")
        self.assertEqual(statuses["media_rights"], "ready")
        self.assertEqual(statuses["publication"], "needs_human_approval")
        self.assertTrue(payload["read_only"])

    def test_missing_translation_becomes_first_action(self):
        article = complete_article()
        article["content"]["en"] = {}

        payload = self.build(article=article)

        self.assertEqual(payload["current_stage"], "localization")
        self.assertEqual(payload["overall_status"], "in_progress")
        self.assertIn("EN/NL", payload["next_action"])

    def test_rights_error_blocks_pipeline(self):
        payload = self.build(registry=rights_registry("pending"))

        self.assertEqual(payload["overall_status"], "blocked")
        self.assertEqual(payload["current_stage"], "media_rights")
        rights = next(stage for stage in payload["stages"] if stage["id"] == "media_rights")
        self.assertEqual(rights["status"], "blocked")

    def test_published_article_points_to_reel_human_review(self):
        payload = self.build(article=complete_article("published"))

        self.assertEqual(payload["current_stage"], "reel_pilot")
        self.assertIn("approves the hook and storyboard", payload["next_action"])
        social = next(stage for stage in payload["stages"] if stage["id"] == "social_package")
        self.assertEqual(social["status"], "ready")
        reel = next(stage for stage in payload["stages"] if stage["id"] == "reel_pilot")
        self.assertIn("Une façade change la rue.", reel["evidence"][0])

    def test_human_render_is_short_and_actionable(self):
        rendered = render_pipeline_status(self.build())

        self.assertIn("Pipeline status: demo", rendered)
        self.assertIn("Current stage: publication", rendered)
        self.assertIn("NEEDS_HUMAN_APPROVAL [publication]", rendered)


if __name__ == "__main__":
    unittest.main()
