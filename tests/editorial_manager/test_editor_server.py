from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from tools.editorial_manager.editor_server import (
    EDITOR_HTML,
    import_filename,
    resolve_static_path,
    route_slug,
    run_editor_pipeline_status,
    run_editor_publication,
)


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

    def test_editor_html_contains_read_only_pipeline_view(self):
        self.assertIn("Parcours de l’article", EDITOR_HTML)
        self.assertIn("Prochaine action", EDITOR_HTML)
        self.assertIn("Aucune étape n’est validée automatiquement", EDITOR_HTML)
        self.assertIn("/pipeline-status", EDITOR_HTML)
        self.assertIn("pipelineStageLabel", EDITOR_HTML)
        self.assertIn("Contenu et vérifications", EDITOR_HTML)
        self.assertIn("Mise en ligne Instagram", EDITOR_HTML)
        self.assertIn("Validation humaine requise", EDITOR_HTML)
        self.assertIn("dernière version enregistrée", EDITOR_HTML)

    def test_editor_html_prepares_local_draft_preview(self):
        self.assertIn('data-preview-locale="${escapeAttr(locale.code)}"', EDITOR_HTML)
        self.assertIn('editorDraft", "1"', EDITOR_HTML)
        self.assertIn("artnouveau:editor-draft-preview", EDITOR_HTML)
        self.assertIn("writeDraftPreview", EDITOR_HTML)
        self.assertIn("clearDraftPreview", EDITOR_HTML)
        self.assertIn("localStorage.setItem", EDITOR_HTML)
        self.assertIn("localStorage.removeItem", EDITOR_HTML)

    def test_editor_html_contains_guarded_publication_flow(self):
        self.assertIn("Validation avant publication", EDITOR_HTML)
        self.assertIn('id="publicationDate"', EDITOR_HTML)
        self.assertIn('id="publicationCheckButton"', EDITOR_HTML)
        self.assertIn('id="publicationApproval"', EDITOR_HTML)
        self.assertIn('id="publishArticleButton"', EDITOR_HTML)
        self.assertIn("hasUnsavedChanges()", EDITOR_HTML)
        self.assertIn("ready-for-human-approval", EDITOR_HTML)
        self.assertIn("approved: true", EDITOR_HTML)
        self.assertIn("Le déploiement reste séparé", EDITOR_HTML)

    def test_editor_publication_requires_date_before_running_transition(self):
        result = run_editor_publication("demo", {}, write=False)

        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["code"], "publication-date-required")

    def test_editor_publication_requires_explicit_approval_for_write(self):
        result = run_editor_publication("demo", {"publication_date": "2026-09-16"}, write=True)

        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["code"], "approval-required")

    @patch("tools.editorial_manager.editor_server.publish_article")
    @patch("tools.editorial_manager.editor_server.load_media_rights_registry")
    def test_editor_publication_returns_transition_payload(self, load_registry, publish):
        load_registry.return_value = {"collections": []}
        transition = Mock(ok=True, written=False)
        transition.to_payload.return_value = {"status": "ready-for-human-approval"}
        publish.return_value = transition

        result = run_editor_publication("demo", {"publication_date": "2026-09-16"}, write=False)

        self.assertTrue(result["ok"])
        self.assertEqual(result["publication"]["status"], "ready-for-human-approval")
        publish.assert_called_once_with(
            "demo",
            "2026-09-16",
            load_registry.return_value,
            write=False,
            approved=False,
        )

    @patch("tools.editorial_manager.editor_server.build_pipeline_status")
    @patch("tools.editorial_manager.editor_server.load_media_rights_registry")
    @patch("tools.editorial_manager.editor_server.find_payload_article")
    @patch("tools.editorial_manager.editor_server.load_article_payload")
    def test_editor_pipeline_status_returns_read_only_payload(self, load_payload, find_article, load_registry, build_status):
        load_payload.return_value = {"articles": []}
        article = {"slug": "demo"}
        find_article.return_value = article
        load_registry.return_value = {"collections": []}
        build_status.return_value = {"slug": "demo", "read_only": True, "current_stage": "publication"}

        result = run_editor_pipeline_status("demo")

        self.assertTrue(result["ok"])
        self.assertTrue(result["pipeline"]["read_only"])
        build_status.assert_called_once()
        self.assertIs(build_status.call_args.args[0], article)
        self.assertIs(build_status.call_args.args[1], load_registry.return_value)

    @patch("tools.editorial_manager.editor_server.find_payload_article", return_value=None)
    @patch("tools.editorial_manager.editor_server.load_article_payload", return_value={"articles": []})
    def test_editor_pipeline_status_rejects_unknown_article(self, _load_payload, _find_article):
        result = run_editor_pipeline_status("missing")

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "unknown-article")

    @patch("tools.editorial_manager.editor_server.load_article_payload", side_effect=ValueError("invalid data"))
    def test_editor_pipeline_status_reports_calculation_error(self, _load_payload):
        result = run_editor_pipeline_status("demo")

        self.assertFalse(result["ok"])
        self.assertEqual(result["code"], "pipeline-status-failed")
        self.assertIn("invalid data", result["error"])

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
