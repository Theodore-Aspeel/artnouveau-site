from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.editor_server import resolve_static_path, route_slug


class EditorServerTests(unittest.TestCase):
    def test_resolve_static_path_serves_files_below_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article_path = root / "article.html"
            article_path.write_text("<html></html>", encoding="utf-8")

            resolved = resolve_static_path(root, "/article.html")

        self.assertEqual(resolved, article_path.resolve())

    def test_resolve_static_path_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            resolved = resolve_static_path(root, "/../secret.txt")

        self.assertIsNone(resolved)

    def test_route_slug_decodes_current_article_slug(self):
        slug = route_slug("/api/articles/demo%20lille", "/api/articles/")

        self.assertEqual(slug, "demo lille")


if __name__ == "__main__":
    unittest.main()
