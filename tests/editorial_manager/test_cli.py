import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tools.editorial_manager.cli import main


class CliTests(unittest.TestCase):
    def test_publication_check_slug_command_runs(self):
        article = {
            "slug": "demo",
            "status": "ready",
            "title": "Demo",
            "chapeau": "Demo dek.",
            "meta_description": "Demo meta.",
            "hero_image": "assets/images/demo.png",
            "alt_text": "Demo alt.",
            "publication_order_recommended": 1,
            "content": {"en": {"title": "Demo"}},
        }
        output = io.StringIO()

        with patch("tools.editorial_manager.cli.load_articles", return_value=[article]):
            with redirect_stdout(output):
                exit_code = main(["publication-check", "demo"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Publication checklist", output.getvalue())
        self.assertIn("Articles checked: 1", output.getvalue())


if __name__ == "__main__":
    unittest.main()
