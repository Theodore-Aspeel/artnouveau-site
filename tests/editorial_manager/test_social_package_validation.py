import json
import tempfile
import unittest
from pathlib import Path

from tools.editorial_manager.social_package import build_social_package, social_package_to_dict
from tools.editorial_manager.social_package_validation import (
    validate_social_package_file,
    validate_social_package_payload,
)


def ready_article() -> dict:
    return {
        "slug": "demo",
        "status": "ready",
        "format": "long",
        "publication": {"order": 1},
        "media": {"hero": {"src": "assets/images/demo.png"}},
        "facts": {"location": {"city": "Lille"}},
        "taxonomy": {"style_key": "art-nouveau"},
        "content": {
            "fr": {
                "title": "Maison Demo",
                "dek": "Dek FR.",
                "sections": [{"heading": "A", "body": "B"}],
                "seo": {"meta_description": "Meta FR."},
                "media": {"hero_alt": "Alt FR."},
            },
            "en": {
                "title": "Demo House",
                "dek": "Dek EN.",
                "sections": [{"heading": "A", "body": "B"}],
                "seo": {"meta_description": "Meta EN."},
                "media": {"hero_alt": "Alt EN."},
            },
        },
    }


class SocialPackageValidationTests(unittest.TestCase):
    def test_validate_social_package_accepts_current_payload(self):
        payload = social_package_to_dict(build_social_package(ready_article(), "en"))

        result = validate_social_package_payload(payload)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, ())
        self.assertEqual(result.warnings, ())

    def test_validate_social_package_rejects_wrong_contract(self):
        payload = social_package_to_dict(build_social_package(ready_article(), "en"))
        payload["contract"]["version"] = 99

        result = validate_social_package_payload(payload)

        self.assertFalse(result.ok)
        self.assertIn("contract.version must be 1.", result.errors)

    def test_validate_social_package_warns_when_not_candidate(self):
        article = ready_article()
        article["content"]["en"] = {}
        payload = social_package_to_dict(build_social_package(article, "en"))

        result = validate_social_package_payload(payload)

        self.assertTrue(result.ok)
        self.assertIn(
            "Payload is valid but queue_status is not candidate; n8n should stop before publishing.",
            result.warnings,
        )

    def test_validate_social_package_file_reads_json(self):
        payload = social_package_to_dict(build_social_package(ready_article(), "en"))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "social-package.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            result = validate_social_package_file(path)

        self.assertTrue(result.ok)


if __name__ == "__main__":
    unittest.main()
