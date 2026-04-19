from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.editor_server import EDITOR_HTML, import_filename, resolve_static_path, route_slug


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

    def test_import_filename_reads_encoded_query_value(self):
        filename = import_filename("filename=Fa%C3%A7ade%20Demo.PNG")

        self.assertEqual(filename, "Façade Demo.PNG")

    def test_editor_html_contains_non_technical_ux_markers(self):
        self.assertIn('class="editor-pane"', EDITOR_HTML)
        self.assertIn("Texte principal ${locale.label}", EDITOR_HTML)
        self.assertIn("editableLocales", EDITOR_HTML)
        self.assertIn('{ code: "nl", label: "NL", required: false, public: false, preview: true, editable: true }', EDITOR_HTML)
        self.assertIn("Obligatoire", EDITOR_HTML)
        self.assertIn("Optionnel", EDITOR_HTML)
        self.assertIn("field-error", EDITOR_HTML)
        self.assertIn("à corriger avant d'enregistrer", EDITOR_HTML)
        self.assertIn('class="tabs"', EDITOR_HTML)
        self.assertIn("data-editor-tab", EDITOR_HTML)
        self.assertIn('class="primary"', EDITOR_HTML)
        self.assertIn('class="secondary"', EDITOR_HTML)
        self.assertIn("button-link tertiary", EDITOR_HTML)
        self.assertIn("Voir l'aperçu ${escapeHtml(locale.label)}", EDITOR_HTML)
        self.assertIn("article-button__chip", EDITOR_HTML)
        self.assertIn('renderLocaleChip(article.locale_statuses, "nl"', EDITOR_HTML)
        self.assertIn('"nl-missing": "NL absent"', EDITOR_HTML)
        self.assertIn('"nl-partial": "NL partiel"', EDITOR_HTML)
        self.assertIn('"nl-ready": "NL pr', EDITOR_HTML)
        self.assertIn("tabForField", EDITOR_HTML)
        self.assertIn("Article enregistr", EDITOR_HTML)
        self.assertIn("Modifications non enregistr", EDITOR_HTML)
        self.assertIn("hasUnsavedChanges", EDITOR_HTML)
        self.assertIn("updateSaveState", EDITOR_HTML)
        self.assertIn("confirmDiscardUnsavedChanges", EDITOR_HTML)
        self.assertIn("beforeunload", EDITOR_HTML)
        self.assertIn("Changer d'article les fera perdre", EDITOR_HTML)
        self.assertIn("Importer une image", EDITOR_HTML)
        self.assertIn('type="file"', EDITOR_HTML)
        self.assertIn("/api/images/import", EDITOR_HTML)
        self.assertIn("refreshImageSelectOptions", EDITOR_HTML)
        self.assertIn("Sauvegarde locale", EDITOR_HTML)
        self.assertIn("restoreBackupButton", EDITOR_HTML)
        self.assertIn("/api/backups/restore", EDITOR_HTML)
        self.assertIn("Une sauvegarde locale", EDITOR_HTML)

    def test_editor_html_prepares_local_draft_preview(self):
        self.assertIn('data-preview-locale="${escapeAttr(locale.code)}"', EDITOR_HTML)
        self.assertIn('editorDraft", "1"', EDITOR_HTML)
        self.assertIn("artnouveau:editor-draft-preview", EDITOR_HTML)
        self.assertIn("writeDraftPreview", EDITOR_HTML)
        self.assertIn("clearDraftPreview", EDITOR_HTML)
        self.assertIn("localStorage.setItem", EDITOR_HTML)
        self.assertIn("localStorage.removeItem", EDITOR_HTML)

    def test_article_template_reads_local_draft_preview_only_when_requested(self):
        script = Path("src/assets/scripts/article-template.js").read_text(encoding="utf-8")

        self.assertIn("articleWithEditorDraft", script)
        self.assertIn("editorDraftStorageKey", script)
        self.assertIn("searchParams.get('editorDraft') !== '1'", script)
        self.assertIn("localStorage.getItem", script)
        self.assertIn("applyDraftPath", script)
        self.assertIn("draft.changes.forEach", script)


if __name__ == "__main__":
    unittest.main()
