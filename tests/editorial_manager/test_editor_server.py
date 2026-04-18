from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.editor_server import EDITOR_HTML, resolve_static_path, route_slug


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

    def test_editor_html_contains_non_technical_ux_markers(self):
        self.assertIn('class="editor-pane"', EDITOR_HTML)
        self.assertIn("Texte principal FR", EDITOR_HTML)
        self.assertIn("Texte principal EN", EDITOR_HTML)
        self.assertIn("Obligatoire", EDITOR_HTML)
        self.assertIn("Optionnel", EDITOR_HTML)
        self.assertIn("field-error", EDITOR_HTML)
        self.assertIn("à corriger avant d'enregistrer", EDITOR_HTML)
        self.assertIn('class="tabs"', EDITOR_HTML)
        self.assertIn("data-editor-tab", EDITOR_HTML)
        self.assertIn('class="primary"', EDITOR_HTML)
        self.assertIn('class="secondary"', EDITOR_HTML)
        self.assertIn("button-link tertiary", EDITOR_HTML)
        self.assertIn("article-button__chip", EDITOR_HTML)
        self.assertIn("tabForField", EDITOR_HTML)


if __name__ == "__main__":
    unittest.main()
