import json
import tempfile
import unittest
from pathlib import Path

from tests.editorial_manager.test_reel_pilot import ready_article
from tools.editorial_manager.reel_pilot import build_reel_pilot
from tools.editorial_manager.reel_pilot_validation import (
    validate_reel_pilot_file,
    validate_reel_pilot_payload,
)


class ReelPilotValidationTests(unittest.TestCase):
    def test_accepts_generated_payload(self):
        result = validate_reel_pilot_payload(build_reel_pilot(ready_article()))

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, ())

    def test_rejects_publish_capability(self):
        payload = build_reel_pilot(ready_article())
        payload["automation_limits"]["publishes_to_instagram"] = True

        result = validate_reel_pilot_payload(payload)

        self.assertFalse(result.ok)
        self.assertIn("automation_limits.publishes_to_instagram must be false.", result.errors)

    def test_reads_exported_json_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reel.json"
            path.write_text(json.dumps(build_reel_pilot(ready_article())), encoding="utf-8")

            result = validate_reel_pilot_file(path)

        self.assertTrue(result.ok)


if __name__ == "__main__":
    unittest.main()
