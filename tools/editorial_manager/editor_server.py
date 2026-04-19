"""Tiny local browser editor served by the Editorial Manager."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse
import webbrowser

from .editor_fields import editable_field_payload
from .editor_backups import create_articles_backup, list_article_backups, restore_articles_backup
from .editor_images import editor_image_path, import_editor_image, list_editor_image_options
from .editor_store import (
    build_editor_article_payload,
    find_payload_article,
    list_editor_articles,
    load_article_payload,
    run_project_validation,
    save_article_changes,
    validate_changes,
)
from .repository import ARTICLES_JSON, PROJECT_ROOT


DIST_ROOT = PROJECT_ROOT / "dist"
SRC_ROOT = PROJECT_ROOT / "src"


def run_editor_server(host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True) -> None:
    server = ThreadingHTTPServer((host, port), EditorRequestHandler)
    url = f"http://{host}:{server.server_port}/"
    print(f"Editorial editor running at {url}")
    print("Press Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(url)
    server.serve_forever()


class EditorRequestHandler(BaseHTTPRequestHandler):
    server_version = "EditorialEditor/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path

        if route == "/":
            self.send_text(EDITOR_HTML, "text/html; charset=utf-8")
            return

        if route == "/data/articles.json":
            self.send_file(ARTICLES_JSON)
            return

        if route.startswith("/assets/images/"):
            image_path = editor_image_path(unquote(route.lstrip("/")))
            if image_path is not None:
                self.send_file(image_path)
                return

        if route.startswith("/assets/"):
            asset_path = resolve_static_path(SRC_ROOT, route)
            if asset_path is None:
                asset_path = resolve_static_path(DIST_ROOT, route)
            if asset_path is None:
                self.send_json({"error": "Asset not found."}, HTTPStatus.NOT_FOUND)
                return
            self.send_file(asset_path)
            return

        site_path = resolve_static_path(DIST_ROOT, route)
        if site_path is not None:
            self.send_file(site_path)
            return

        if route == "/api/fields":
            self.send_json({"fields": editable_field_payload()})
            return

        if route == "/api/articles":
            payload = load_article_payload(ARTICLES_JSON)
            self.send_json({"articles": list_editor_articles(payload)})
            return

        if route == "/api/backups":
            self.send_json({"backups": list_article_backups()})
            return

        slug = route_slug(route, "/api/articles/")
        if slug:
            payload = load_article_payload(ARTICLES_JSON)
            article = find_payload_article(payload, slug)
            if article is None:
                self.send_json({"error": "Unknown article slug."}, HTTPStatus.NOT_FOUND)
                return
            self.send_json(build_editor_article_payload(article))
            return

        self.send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path

        if route == "/api/images/import":
            filename = import_filename(parsed.query)
            payload = self.read_bytes()
            try:
                image = import_editor_image(filename, payload)
            except ValueError as exc:
                self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)
                return
            self.send_json({"ok": True, "image": image, "image_options": list_editor_image_options()})
            return

        if route == "/api/backups/restore":
            request = self.read_json()
            try:
                current_backup = create_articles_backup(ARTICLES_JSON, keep=6)
                restored = restore_articles_backup(request.get("backup_id"), ARTICLES_JSON)
                ok, validation_errors = run_project_validation()
            except (FileNotFoundError, ValueError, OSError) as exc:
                self.send_json({"ok": False, "errors": [{"code": "restore-failed", "message": str(exc)}]}, HTTPStatus.BAD_REQUEST)
                return
            if not ok:
                restore_articles_backup(current_backup["id"], ARTICLES_JSON)
                self.send_json(
                    {
                        "ok": False,
                        "errors": [
                            {
                                "code": "restore-validation",
                                "message": "La restauration a echoue pendant la verification. L'etat precedent a ete remis en place.",
                            }
                        ]
                        + [{"code": "restore-validation", "message": message} for message in validation_errors],
                    },
                    HTTPStatus.BAD_REQUEST,
                )
                return
            self.send_json(
                {
                    "ok": True,
                    "restored": restored,
                    "backups": list_article_backups(),
                    "message": "Sauvegarde restauree. La verification du projet est passee.",
                }
            )
            return

        if route.endswith("/validate"):
            slug = route_slug(route[: -len("/validate")], "/api/articles/")
            if not slug:
                self.send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)
                return
            payload = load_article_payload(ARTICLES_JSON)
            article = find_payload_article(payload, slug)
            if article is None:
                self.send_json({"error": "Unknown article slug."}, HTTPStatus.NOT_FOUND)
                return
            request = self.read_json()
            errors = validate_changes(article, request.get("changes", []))
            self.send_json({"ok": not errors, "errors": errors})
            return

        if route.endswith("/save"):
            slug = route_slug(route[: -len("/save")], "/api/articles/")
            if not slug:
                self.send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)
                return
            request = self.read_json()
            result = save_article_changes(slug, request.get("changes", []), ARTICLES_JSON)
            status = HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST
            self.send_json(result, status)
            return

        self.send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}

    def read_bytes(self) -> bytes:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return b""
        return self.rfile.read(length)

    def send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_text(self, payload: str, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_file(self, path) -> None:
        payload = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def resolve_static_path(root: Path, route: str) -> Path | None:
    if not root.exists():
        return None
    relative_route = unquote(route).lstrip("/") or "index.html"
    candidate = (root / relative_route).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate if candidate.is_file() else None


def route_slug(route: str, prefix: str) -> str:
    if not route.startswith(prefix):
        return ""
    slug = route[len(prefix):].strip("/")
    if not slug or "/" in slug:
        return ""
    return unquote(slug)


def import_filename(query: str) -> str:
    values = parse_qs(query, keep_blank_values=True).get("filename", [])
    return values[0] if values else ""


EDITOR_HTML = r"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Éditeur éditorial</title>
  <style>
    :root { --border: #d8ded7; --muted: #667381; --text: #21313b; --panel: #ffffff; --soft: #f5f8f3; --soft-strong: #edf3eb; --accent: #1f6b5d; --accent-dark: #174f45; --accent-soft: #e7f2ee; --gold: #b88122; --rose: #b85852; --error: #b42318; --error-bg: #fff0ee; --success: #1f6f43; --success-bg: #edf7ef; --shadow: 0 16px 36px rgba(38, 51, 44, 0.08); }
    body { margin: 0; font-family: Arial, sans-serif; color: var(--text); background: linear-gradient(180deg, #f4f7f2 0%, #f8f5f1 52%, #f6f7f8 100%); }
    header { padding: 14px 22px; background: var(--panel); border-bottom: 1px solid var(--border); }
    main { display: grid; grid-template-columns: 330px 1fr; height: calc(100vh - 59px); min-height: 620px; }
    aside { border-right: 1px solid var(--border); background: #fbfcf9; overflow: auto; }
    .editor-pane { padding: 18px 20px; overflow: auto; }
    h1 { margin: 0; font-size: 21px; letter-spacing: 0; }
    h2 { margin: 0; font-size: 22px; }
    h3 { margin: 0; font-size: 17px; }
    p { margin: 0; }
    button, select, input, textarea { font: inherit; }
    button, .button-link { border: 1px solid #a8b2a9; border-radius: 8px; background: #ffffff; padding: 8px 11px; cursor: pointer; line-height: 1.2; }
    .button-link { color: inherit; display: inline-block; text-decoration: none; }
    button.primary { background: var(--accent); color: #ffffff; border-color: var(--accent); box-shadow: 0 8px 18px rgba(31, 107, 93, 0.18); font-weight: 700; }
    button.primary:hover { background: var(--accent-dark); }
    button.primary:disabled:hover { background: var(--accent); }
    button.secondary { background: #ffffff; border-color: #7b9b8d; color: var(--accent-dark); font-weight: 700; }
    .button-link.tertiary { border-color: transparent; background: transparent; color: var(--accent-dark); padding-inline: 6px; text-decoration: underline; text-underline-offset: 3px; }
    button:disabled { cursor: not-allowed; opacity: 0.55; }
    .article-list-header { position: sticky; top: 0; z-index: 2; display: grid; gap: 4px; padding: 13px 14px; background: #fbfcf9; border-bottom: 1px solid var(--border); }
    .article-list-title { font-weight: 800; }
    .article-count { color: var(--muted); font-size: 13px; }
    .article-button { display: grid; gap: 6px; width: calc(100% - 14px); text-align: left; border: 1px solid transparent; border-radius: 8px; margin: 7px; padding: 10px 12px; background: transparent; }
    .article-button:hover { background: #ffffff; border-color: #e1e7df; }
    .article-button.active { background: #ffffff; border-color: #99b8aa; box-shadow: 0 8px 22px rgba(33, 49, 59, 0.08); }
    .article-button__title { font-weight: 800; line-height: 1.25; }
    .article-button__meta { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; color: var(--muted); font-size: 12px; }
    .article-button__chip { display: inline-flex; align-items: center; min-height: 20px; padding: 1px 7px; border-radius: 999px; background: var(--accent-soft); color: var(--accent-dark); font-weight: 700; }
    .article-button__chip.warning { background: #fff4df; color: #7b4e12; }
    .meta { color: var(--muted); font-size: 13px; margin-top: 4px; }
    .editor-shell { display: grid; gap: 12px; max-width: 1160px; }
    .editor-header { position: sticky; top: 0; z-index: 5; display: grid; gap: 10px; padding: 14px; border: 1px solid var(--border); border-radius: 8px; background: rgba(255, 255, 255, 0.97); box-shadow: 0 10px 26px rgba(38, 51, 44, 0.08); }
    .editor-title-row { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 14px; align-items: start; }
    .status-pills, .preview-actions, .primary-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .status-pills { justify-content: flex-start; margin-top: 8px; }
    .editor-toolbar { display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap; padding-top: 10px; border-top: 1px solid #edf0eb; }
    .backup-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; padding-top: 10px; border-top: 1px solid #edf0eb; }
    .backup-actions label { font-weight: 700; }
    .primary-actions { order: 1; }
    .preview-actions { order: 2; margin-left: auto; }
    .pill { display: inline-flex; align-items: center; min-height: 24px; padding: 2px 8px; border: 1px solid #dbe3da; border-radius: 999px; background: var(--soft); color: #3f4d44; font-size: 12px; font-weight: 700; }
    .pill.required { border-color: #efcfca; background: #fff5f3; color: #8a2f25; }
    .pill.optional { color: var(--muted); }
    .pill.warning { border-color: #eed39b; background: #fff7e8; color: #7b4e12; }
    .save-state { border-color: #cfe1d4; background: var(--success-bg); color: var(--success); }
    .save-state.dirty { border-color: #eed39b; background: #fff7e8; color: #7b4e12; }
    .tabs { display: flex; gap: 7px; overflow-x: auto; padding: 3px 2px 2px; }
    .tab-button { border-color: #d6dfd5; background: #ffffff; color: #43504a; font-weight: 700; white-space: nowrap; }
    .tab-button.active { background: var(--accent); border-color: var(--accent); color: #ffffff; }
    .form-grid { display: grid; gap: 12px; }
    .tab-panel { display: none; gap: 12px; }
    .tab-panel.active { display: grid; }
    .field-panel { border: 1px solid var(--border); border-radius: 8px; background: var(--panel); overflow: hidden; box-shadow: 0 8px 24px rgba(38, 51, 44, 0.05); }
    .field-panel__header { display: grid; gap: 4px; padding: 11px 14px; border-bottom: 1px solid var(--border); background: linear-gradient(90deg, var(--soft-strong), #ffffff); }
    .field-panel__description { color: var(--muted); font-size: 14px; }
    .field-group { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 14px; padding: 14px; }
    .field-row { display: grid; gap: 6px; }
    .field-row--wide { grid-column: 1 / -1; }
    .field-label-line { display: flex; gap: 8px; align-items: center; justify-content: flex-start; flex-wrap: wrap; font-weight: 700; }
    .field-help { color: var(--muted); font-size: 13px; line-height: 1.4; }
    .field-error { display: none; color: var(--error); font-size: 13px; font-weight: 700; }
    .field-row.has-error .field-error { display: block; }
    .field-row.has-error input, .field-row.has-error textarea, .field-row.has-error select { border-color: var(--error); box-shadow: 0 0 0 2px rgba(180, 35, 24, 0.08); }
    input, textarea, select { border: 1px solid #aeb9c3; border-radius: 6px; padding: 9px 10px; background: #ffffff; max-width: 100%; }
    textarea { min-height: 84px; resize: vertical; line-height: 1.45; }
    .field-row--wide textarea { min-height: 116px; }
    .hero-preview { display: grid; gap: 8px; max-width: 460px; }
    .hero-preview img { width: 100%; max-height: 300px; object-fit: cover; border-radius: 6px; border: 1px solid var(--border); background: #ffffff; }
    .image-import { display: grid; gap: 10px; padding: 14px; }
    .image-import__actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .image-import input[type="file"] { max-width: 420px; }
    .image-empty, .support-preview .empty { padding: 12px; border: 1px dashed #b8c2cc; border-radius: 6px; background: #ffffff; color: var(--muted); }
    .support-summary { display: grid; gap: 10px; }
    .support-summary__grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
    .support-preview { display: grid; gap: 6px; padding: 10px; border: 1px solid var(--border); border-radius: 6px; background: #ffffff; }
    .support-preview img { width: 100%; max-height: 180px; object-fit: cover; border-radius: 6px; border: 1px solid var(--border); background: #ffffff; }
    .message { padding: 11px 13px; border-radius: 6px; border: 1px solid #b9ddc2; background: var(--success-bg); color: var(--success); font-weight: 700; }
    .message.error { border-color: #e6b7b0; background: var(--error-bg); color: var(--error); }
    .message ul { margin: 8px 0 0; padding-left: 20px; font-weight: 400; }
    .empty { color: var(--muted); }
    @media (max-width: 920px) { main { grid-template-columns: 1fr; height: auto; min-height: 100vh; } aside { max-height: 34vh; border-right: 0; border-bottom: 1px solid var(--border); } .editor-pane { padding: 16px; } .editor-title-row { grid-template-columns: 1fr; } .preview-actions { margin-left: 0; } .field-group { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <header>
    <h1>Éditeur éditorial</h1>
  </header>
  <main>
    <aside id="articleList"></aside>
    <section class="editor-pane">
      <div id="editor"><p class="empty">Choisissez un article à modifier.</p></div>
    </section>
  </main>
  <script>
    let fields = [];
    let articles = [];
    let currentSlug = "";
    let currentValues = {};
    let savedValues = {};
    let currentImageOptions = [];
    let currentArticleFields = [];
    let currentTab = "essentiel";
    let recentBackups = [];
    let currentLocaleContract = defaultLocaleContract();

    async function api(path, options) {
      const response = await fetch(path, options);
      const data = await response.json();
      if (!response.ok) throw data;
      return data;
    }

    async function init() {
      fields = (await api("/api/fields")).fields;
      articles = (await api("/api/articles")).articles;
      recentBackups = (await api("/api/backups")).backups || [];
      renderArticleList();
    }

    function renderArticleList() {
      const list = document.getElementById("articleList");
      list.innerHTML = `
        <div class="article-list-header">
          <div class="article-list-title">Articles</div>
          <div class="article-count">${articles.length} article${articles.length > 1 ? "s" : ""} disponibles</div>
        </div>
      `;
      articles.forEach((article) => {
        const button = document.createElement("button");
        button.className = "article-button" + (article.slug === currentSlug ? " active" : "");
        button.innerHTML = `
          <span class="article-button__title">${escapeHtml(article.title || article.slug)}</span>
          <span class="article-button__meta">
            <span>${escapeHtml(statusLabel(article.status))}</span>
            <span class="article-button__chip${article.has_hero ? "" : " warning"}">${article.has_hero ? "image choisie" : "image à choisir"}</span>
            ${renderLocaleChip(article.locale_statuses, "nl", "article-button__chip")}
          </span>
        `;
        button.addEventListener("click", () => openArticle(article.slug));
        list.appendChild(button);
      });
    }

    async function openArticle(slug) {
      if (slug !== currentSlug && !confirmDiscardUnsavedChanges()) return;
      const article = await api(`/api/articles/${encodeURIComponent(slug)}`);
      currentSlug = slug;
      currentValues = {};
      article.fields.forEach((item) => currentValues[item.path] = item.value || "");
      savedValues = { ...currentValues };
      currentImageOptions = article.image_options || [];
      currentArticleFields = article.fields || [];
      currentLocaleContract = article.locale_contract || defaultLocaleContract();
      currentTab = "essentiel";
      renderArticleList();
      renderEditor(article);
    }

    function renderEditor(article) {
      const editor = document.getElementById("editor");
      const controls = renderFieldGroups(article.fields || []);
      editor.innerHTML = `
        <div class="editor-shell">
          <div class="editor-header">
            <div class="editor-title-row">
              <div>
                <h2>${escapeHtml(article.title || article.slug)}</h2>
                <div class="meta">Article: ${escapeHtml(article.slug)}</div>
                <div class="status-pills">
                  <span class="pill save-state" id="saveState">Article enregistré</span>
                  <span class="pill">Statut: ${escapeHtml(statusLabel(article.status))}</span>
                  <span class="pill">${article.hero_src ? "Image principale choisie" : "Image principale à choisir"}</span>
                  ${renderLocaleChip(article.locale_statuses, "nl", "pill")}
                </div>
              </div>
              <div class="primary-actions" aria-label="Actions principales">
                <button id="saveButton" class="primary" type="button">Enregistrer</button>
                <button id="validateButton" class="secondary" type="button">Vérifier les champs</button>
              </div>
            </div>
            ${renderBackupActions()}
            <div class="editor-toolbar">
              ${renderEditorTabs()}
              ${renderPreviewActions(article.preview_urls || {})}
            </div>
          </div>
          <div id="message" aria-live="polite"></div>
          <form class="form-grid" id="articleForm">${controls}</form>
        </div>
      `;
      document.getElementById("validateButton").addEventListener("click", validateArticle);
      document.getElementById("saveButton").addEventListener("click", saveArticle);
      const restoreButton = document.getElementById("restoreBackupButton");
      if (restoreButton) restoreButton.addEventListener("click", restoreBackup);
      document.querySelectorAll("[data-preview-locale]").forEach((link) => {
        link.addEventListener("click", writeDraftPreview);
      });
      document.querySelectorAll("[data-editor-tab]").forEach((button) => {
        button.addEventListener("click", () => activateTab(button.dataset.editorTab));
      });
      document.querySelectorAll("[data-field]").forEach((control) => {
        control.addEventListener("input", () => handleFieldEdit(control));
        control.addEventListener("change", () => handleFieldEdit(control));
      });
      const imageImportButton = document.getElementById("imageImportButton");
      if (imageImportButton) imageImportButton.addEventListener("click", importImage);
      const heroSelect = document.querySelector('[data-field="media.hero.src"]');
      if (heroSelect) {
        heroSelect.addEventListener("change", () => {
          currentValues["media.hero.src"] = heroSelect.value;
          const preview = document.getElementById("heroPreview");
          if (preview) preview.outerHTML = renderHeroPreview(heroSelect.value);
        });
      }
      document.querySelectorAll('select[data-control="image-select"]').forEach((select) => {
        if (select.dataset.field === "media.hero.src") return;
        select.addEventListener("change", () => {
          currentValues[select.dataset.field] = select.value;
          const preview = document.getElementById(fieldPreviewId(select.dataset.field));
          if (preview) preview.outerHTML = renderSupportFieldPreview(select.dataset.field, select.value);
        });
      });
      updateSaveState();
    }

    function renderPreviewActions(urls) {
      const links = previewLocales().map((locale) => {
        const url = draftPreviewUrl(urls[locale.code] || previewUrl(locale.code));
        return `<a class="button-link tertiary" href="${escapeAttr(url)}" target="_blank" rel="noopener noreferrer" data-preview-locale="${escapeAttr(locale.code)}">Voir l'aperçu ${escapeHtml(locale.label)}</a>`;
      }).join("");
      return `
        <div class="preview-actions" aria-label="Preview de l'article">
          ${links}
        </div>
      `;
    }

    function defaultLocaleContract() {
      return {
        default: "fr",
        supported: [
          { code: "fr", label: "FR", required: true, public: true, preview: true, editable: true },
          { code: "en", label: "EN", required: false, public: true, preview: true, editable: true },
          { code: "nl", label: "NL", required: false, public: false, preview: true, editable: true },
        ],
        editable: ["fr", "en", "nl"],
        preview: ["fr", "en", "nl"],
      };
    }

    function defaultLocale() {
      return currentLocaleContract.default || "fr";
    }

    function localeSpecs() {
      return Array.isArray(currentLocaleContract.supported) ? currentLocaleContract.supported : [];
    }

    function editableLocales() {
      const editableCodes = localeCodeSet(currentLocaleContract.editable);
      return localeSpecs().filter((locale) => locale && locale.editable && editableCodes.has(locale.code));
    }

    function previewLocales() {
      const previewCodes = localeCodeSet(currentLocaleContract.preview);
      return localeSpecs().filter((locale) => locale && locale.preview && previewCodes.has(locale.code));
    }

    function localeSpec(code) {
      return localeSpecs().find((locale) => locale.code === code) || { code, label: String(code || "").toUpperCase() };
    }

    function localeCodeSet(codes) {
      if (!Array.isArray(codes)) return new Set(localeSpecs().map((locale) => locale.code));
      return new Set(codes);
    }

    function renderBackupActions() {
      const options = recentBackups.map((backup) => `<option value="${escapeAttr(backup.id)}">${escapeHtml(backup.label)}</option>`).join("");
      const disabled = recentBackups.length ? "" : " disabled";
      const help = recentBackups.length ? "Revient a une version locale recente de articles.json." : "Aucune sauvegarde locale disponible pour le moment.";
      return `
        <div class="backup-actions" aria-label="Sauvegardes locales">
          <label for="backupSelect">Sauvegarde locale</label>
          <select id="backupSelect"${disabled}>${options}</select>
          <button id="restoreBackupButton" class="secondary" type="button"${disabled}>Restaurer</button>
          <span class="meta">${help}</span>
        </div>
      `;
    }

    function renderEditorTabs() {
      const localeButtons = editableLocales().map((locale) => renderTabButton(locale.code, `Texte ${locale.label}`)).join("");
      return `
        <nav class="tabs" aria-label="Parties de l'article">
          ${renderTabButton("essentiel", "Essentiel")}
          ${localeButtons}
          ${renderTabButton("images", "Images")}
        </nav>
      `;
    }

    function renderTabButton(tab, label) {
      return `<button class="tab-button${currentTab === tab ? " active" : ""}" type="button" data-editor-tab="${escapeAttr(tab)}">${escapeHtml(label)}</button>`;
    }

    function activateTab(tab) {
      currentTab = tab || "essentiel";
      document.querySelectorAll("[data-editor-tab]").forEach((button) => {
        button.classList.toggle("active", button.dataset.editorTab === currentTab);
      });
      document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
        panel.classList.toggle("active", panel.dataset.tabPanel === currentTab);
      });
    }

    function previewUrl(locale) {
      const base = `article.html?slug=${encodeURIComponent(currentSlug)}`;
      return locale === defaultLocale() ? base : `${base}&previewLocale=${encodeURIComponent(locale)}`;
    }

    function renderLocaleChip(statuses, locale, className) {
      const item = statuses && statuses[locale];
      if (!item || !item.status) return "";
      const warning = item.status.endsWith("-missing") || item.status.endsWith("-partial");
      const title = item.missing_fields && item.missing_fields.length
        ? ` title="${escapeAttr("Champs manquants: " + item.missing_fields.join(", "))}"`
        : "";
      return `<span class="${className}${warning ? " warning" : ""}"${title}>${escapeHtml(localeStatusLabel(item.status))}</span>`;
    }

    function draftPreviewUrl(href) {
      const url = new URL(href, window.location.href);
      url.searchParams.set("editorDraft", "1");
      return url.pathname.replace(/^\//, "") + url.search + url.hash;
    }

    function renderHeroPreview(src) {
      if (!src) {
        return `<div class="hero-preview" id="heroPreview"><strong>Aperçu de l'image principale</strong><p class="image-empty">Aucune image principale sélectionnée.</p></div>`;
      }
      return `
        <div class="hero-preview" id="heroPreview">
          <strong>Aperçu de l'image principale</strong>
          <img src="/${escapeAttr(encodeImagePath(src))}" alt="">
          <div class="meta">${escapeHtml(src)}</div>
        </div>
      `;
    }

    function renderSupportSummary(images) {
      if (!images.length) {
        return `<div class="support-summary"><strong>Images support</strong><p class="empty">Aucune image support existante. Cet éditeur ne permet pas d'en ajouter.</p></div>`;
      }
      const cards = images.map((image) => renderSupportCard(image.index, image.src || "")).join("");
      return `
        <div class="support-summary">
          <strong>Images support</strong>
          <div class="support-summary__grid">${cards}</div>
        </div>
      `;
    }

    function renderSupportCard(index, src) {
      if (!src) {
        return `<div class="support-preview"><strong>Image ${Number(index) + 1}</strong><p class="empty">Aucune image.</p></div>`;
      }
      return `
        <div class="support-preview">
          <strong>Image ${Number(index) + 1}</strong>
          <img src="/${escapeAttr(encodeImagePath(src))}" alt="">
          <div class="meta">${escapeHtml(src)}</div>
        </div>
      `;
    }

    function renderFieldGroups(articleFields) {
      const groups = editorGroups();
      articleFields.forEach((field) => {
        groupForField(groups, field).fields.push(field);
      });

      return editorTabs().map((tab) => {
        const groupMarkup = groups.filter((group) => group.tab === tab.key && group.fields.length).map((group) => {
          const controls = group.fields.map((field) => renderField(field, currentValues[field.path] || "")).join("");
          return `
            <section class="field-panel" aria-labelledby="${escapeAttr(group.id)}">
              <div class="field-panel__header">
                <h3 id="${escapeAttr(group.id)}">${escapeHtml(group.name)}</h3>
                <p class="field-panel__description">${escapeHtml(group.description)}</p>
              </div>
              <div class="field-group">${controls}</div>
            </section>
          `;
        }).join("");
        const importMarkup = tab.key === "images" ? renderImageImportPanel() : "";
        if (tab.key === "images") {
          return `<div class="tab-panel${currentTab === tab.key ? " active" : ""}" data-tab-panel="${escapeAttr(tab.key)}">${importMarkup}${groupMarkup}</div>`;
        }
        if (!groupMarkup) return "";
        return `<div class="tab-panel${currentTab === tab.key ? " active" : ""}" data-tab-panel="${escapeAttr(tab.key)}">${groupMarkup}</div>`;
      }).join("");
    }

    function renderImageImportPanel() {
      return `
        <section class="field-panel" aria-labelledby="group-image-import">
          <div class="field-panel__header">
            <h3 id="group-image-import">Importer une image</h3>
            <p class="field-panel__description">Ajouter une image locale au projet, puis la choisir dans les listes image principale ou support.</p>
          </div>
          <div class="image-import">
            <input id="imageImportFile" type="file" accept=".avif,.gif,.jpg,.jpeg,.png,.webp,image/avif,image/gif,image/jpeg,image/png,image/webp">
            <div class="image-import__actions">
              <button id="imageImportButton" class="secondary" type="button">Importer l'image</button>
              <span class="meta">Une seule image a la fois. Extensions acceptees: avif, gif, jpg, jpeg, png, webp.</span>
            </div>
          </div>
        </section>
      `;
    }

    function editorTabs() {
      return [
        { key: "essentiel" },
        ...editableLocales().map((locale) => ({ key: locale.code })),
        { key: "images" },
      ];
    }

    function editorGroups() {
      const groups = [
        { id: "group-status", key: "status", tab: "essentiel", name: "Publication", description: "Etat de travail de l'article.", fields: [] },
      ];
      editableLocales().forEach((locale) => {
        const tab = locale.required ? "essentiel" : locale.code;
        const description = locale.required
          ? `Titre, chapeau, épigraphe, SEO et note liée en ${locale.label}.`
          : `Champs ${locale.label}, à compléter progressivement quand le contenu existe.`;
        groups.push(
          { id: `group-${locale.code}-main`, key: `${locale.code}-main`, tab, name: `Texte principal ${locale.label}`, description, fields: [] },
          { id: `group-${locale.code}-practical`, key: `${locale.code}-practical`, tab: locale.code, name: `Informations pratiques ${locale.label}`, description: `Valeurs visibles dans le bloc pratique ${locale.label}.`, fields: [] },
          { id: `group-${locale.code}-sections`, key: `${locale.code}-sections`, tab: locale.code, name: `Sections ${locale.label}`, description: `Titres et paragraphes du corps ${locale.label} si disponibles.`, fields: [] }
        );
      });
      groups.push(
        { id: "group-hero", key: "hero", tab: "images", name: "Image principale", description: "Image affichée en tête d'article.", fields: [] },
        { id: "group-support", key: "support", tab: "images", name: "Images support", description: "Images secondaires déjà présentes dans l'article.", fields: [] },
        { id: "group-other", key: "other", tab: "essentiel", name: "Autres champs", description: "Champs éditables complémentaires.", fields: [] },
      );
      return groups;
    }

    function groupForField(groups, field) {
      const path = field.path || "";
      let key = "other";
      if (path === "status") key = "status";
      else if (path === "media.hero.src") key = "hero";
      else if (path.startsWith("media.support.")) key = "support";
      else {
        const locale = contentLocale(path);
        if (locale && path.includes(".practical_items.")) key = `${locale}-practical`;
        else if (locale && path.includes(".sections.")) key = `${locale}-sections`;
        else if (locale) key = `${locale}-main`;
      }
      return groups.find((group) => group.key === key) || groups[groups.length - 1];
    }

    function renderField(field, value) {
      const required = field.required ? " required" : "";
      const fieldId = fieldDomId(field.path);
      const help = fieldHelp(field);
      const helpMarkup = help ? `<p class="field-help" id="${escapeAttr(fieldId)}-help">${escapeHtml(help)}</p>` : "";
      const describedBy = help ? ` aria-describedby="${escapeAttr(fieldId)}-help ${escapeAttr(fieldId)}-error"` : ` aria-describedby="${escapeAttr(fieldId)}-error"`;
      const badge = `<span class="pill ${field.required ? "required" : "optional"}">${field.required ? "Obligatoire" : "Optionnel"}</span>`;
      const label = `<div class="field-label-line"><label for="${escapeAttr(fieldId)}">${fieldLabel(field)}</label>${badge}</div>`;
      const error = `<p class="field-error" id="${escapeAttr(fieldId)}-error"></p>`;
      const rowClass = isWideField(field) ? "field-row field-row--wide" : "field-row";
      if (field.control === "select") {
        const options = field.choices.map((choice) => `<option value="${escapeAttr(choice)}"${choice === value ? " selected" : ""}>${escapeHtml(choice)}</option>`).join("");
        return `<div class="${rowClass}" data-field-row="${escapeAttr(field.path)}">${label}${helpMarkup}<select id="${escapeAttr(fieldId)}" data-field="${escapeAttr(field.path)}"${required}${describedBy}>${options}</select>${error}</div>`;
      }
      if (field.control === "image-select") {
        const options = `<option value="">Choisir une image...</option>` + currentImageOptions.map((image) => `<option value="${escapeAttr(image.src)}"${image.src === value ? " selected" : ""}>${escapeHtml(image.label || image.src)}</option>`).join("");
        const preview = field.path.startsWith("media.support.") ? renderSupportFieldPreview(field.path, value) : "";
        const heroPreview = field.path === "media.hero.src" ? renderHeroPreview(value) : "";
        return `<div class="${rowClass}" data-field-row="${escapeAttr(field.path)}">${label}${helpMarkup}<select id="${escapeAttr(fieldId)}" data-control="image-select" data-field="${escapeAttr(field.path)}"${required}${describedBy}>${options}</select>${error}${heroPreview}${preview}</div>`;
      }
      if (field.control === "textarea") {
        return `<div class="${rowClass}" data-field-row="${escapeAttr(field.path)}">${label}${helpMarkup}<textarea id="${escapeAttr(fieldId)}" data-field="${escapeAttr(field.path)}"${required}${describedBy}>${escapeHtml(value)}</textarea>${error}</div>`;
      }
      return `<div class="${rowClass}" data-field-row="${escapeAttr(field.path)}">${label}${helpMarkup}<input id="${escapeAttr(fieldId)}" data-field="${escapeAttr(field.path)}" value="${escapeAttr(value)}"${required}${describedBy}>${error}</div>`;
    }

    function isWideField(field) {
      const path = field.path || "";
      return field.control === "textarea" || path === "media.hero.src" || path.startsWith("media.support.");
    }

    function fieldLabel(field) {
      return escapeHtml(displayLabel(field));
    }

    function displayLabel(field) {
      const path = field.path || "";
      const labels = {
        "status": "Statut",
        "media.hero.src": "Image principale",
      };
      if (labels[path]) return labels[path];

      const main = path.match(/^content\.([a-z]{2})\.(title|dek|epigraph|seo\.meta_description|media\.hero_alt|around\.note)$/);
      if (main) {
        const locale = localeSpec(main[1]).label;
        const labelsByField = {
          title: "Titre",
          dek: "Chapeau",
          epigraph: "Épigraphe",
          "seo.meta_description": "Description courte",
          "media.hero_alt": "Description de l'image",
          "around.note": "Note d'article lié",
        };
        return `${labelsByField[main[2]] || field.label} ${locale}`;
      }

      const section = path.match(/^content\.([a-z]{2})\.sections\.(\d+)\.(heading|body)$/);
      if (section) {
        const locale = localeSpec(section[1]).label;
        const number = Number(section[2]) + 1;
        return section[3] === "heading" ? `Section ${number} - titre ${locale}` : `Section ${number} - texte ${locale}`;
      }

      const practical = path.match(/^content\.([a-z]{2})\.practical_items\.(\d+)\.value$/);
      if (practical) {
        const locale = localeSpec(practical[1]).label;
        const labelsByKey = { city: "Ville", country: "Pays", style: "Style", architect: "Architecte", address: "Adresse", date: "Date", access: "Accès" };
        return `${labelsByKey[field.readonly_key] || field.label} ${locale}`;
      }

      const support = path.match(/^media\.support\.(\d+)\.src$/);
      if (support) return `Image support ${Number(support[1]) + 1}`;
      return field.label || path;
    }

    function fieldHelp(field) {
      const path = field.path || "";
      if (path === "status") return "Choisir l'état de travail avant publication.";
      if (path === "media.hero.src") return "Choisir une image déjà présente dans le projet.";
      if (path.includes(".title")) return "Titre visible en haut de l'article.";
      if (path.includes(".dek")) return "Court résumé affiché sous le titre.";
      if (path.includes(".epigraph")) return "Phrase d'accroche affichée avant le texte.";
      if (path.includes("seo.meta_description")) return "Résumé court utilisé par les moteurs de recherche et les partages.";
      if (path.includes("media.hero_alt")) return "Décrire brièvement l'image pour l'accessibilité.";
      if (path.includes(".around.note")) return "Courte note visible vers l'article lié.";
      if (path.includes(".sections.") && path.endsWith(".heading")) return "Intertitre de section.";
      if (path.includes(".sections.") && path.endsWith(".body")) return "Texte principal de cette section.";
      if (path.includes(".practical_items.")) return "Modifier seulement la valeur visible, pas le type d'information.";
      if (path.startsWith("media.support.")) return "Remplacer uniquement l'image de cet emplacement existant.";
      return "";
    }

    function contentLocale(path) {
      const match = String(path || "").match(/^content\.([a-z]{2})\./);
      return match ? match[1] : "";
    }

    function fieldDomId(path) {
      return `field-${String(path).replace(/[^a-z0-9]+/gi, "-")}`;
    }

    function statusLabel(status) {
      const labels = { draft: "brouillon", ready: "prêt", published: "publié" };
      return labels[status] || status || "-";
    }

    function localeStatusLabel(status) {
      const labels = {
        "fr-only": "EN absent",
        "en-missing": "EN absent",
        "en-partial": "EN partiel",
        "en-ready": "EN prêt",
        "nl-missing": "NL absent",
        "nl-partial": "NL partiel",
        "nl-ready": "NL prêt"
      };
      return labels[status] || status || "-";
    }

    function renderSupportFieldPreview(fieldPath, src) {
      const id = fieldPreviewId(fieldPath);
      if (!src) {
        return `<div class="support-preview" id="${escapeAttr(id)}"><p class="empty">Aucune image sélectionnée pour cet emplacement.</p></div>`;
      }
      return `
        <div class="support-preview" id="${escapeAttr(id)}">
          <img src="/${escapeAttr(encodeImagePath(src))}" alt="">
          <div class="meta">${escapeHtml(src)}</div>
        </div>
      `;
    }

    function fieldPreviewId(fieldPath) {
      return `preview-${String(fieldPath).replace(/[^a-z0-9]+/gi, "-")}`;
    }

    function collectChanges() {
      return Array.from(document.querySelectorAll("[data-field]")).map((control) => ({
        field: control.dataset.field,
        value: control.value
      }));
    }

    function draftPreviewStorageKey(slug) {
      return `artnouveau:editor-draft-preview:${slug}`;
    }

    function writeDraftPreview() {
      if (!currentSlug) return;
      try {
        window.localStorage.setItem(draftPreviewStorageKey(currentSlug), JSON.stringify({
          slug: currentSlug,
          changes: collectChanges(),
          expires_at: Date.now() + 24 * 60 * 60 * 1000
        }));
      } catch (error) {
        setMessage("Le brouillon de preview n'a pas pu être préparé dans ce navigateur.", true);
      }
    }

    function clearDraftPreview(slug) {
      try {
        window.localStorage.removeItem(draftPreviewStorageKey(slug));
      } catch (error) {
        return;
      }
    }

    function handleFieldEdit(control) {
      currentValues[control.dataset.field] = control.value;
      clearFieldError(control.dataset.field);
      updateSaveState();
    }

    async function importImage() {
      const input = document.getElementById("imageImportFile");
      const file = input && input.files ? input.files[0] : null;
      if (!file) {
        setMessage("Choisissez d'abord une image locale a importer.", true);
        return;
      }
      setMessage("Import de l'image en cours...");
      try {
        const result = await api(`/api/images/import?filename=${encodeURIComponent(file.name)}`, {
          method: "POST",
          headers: { "Content-Type": "application/octet-stream" },
          body: file
        });
        currentImageOptions = result.image_options || currentImageOptions;
        refreshImageSelectOptions();
        if (input) input.value = "";
        setMessage(`Image importee: ${escapeHtml(result.image.src)}. Elle est maintenant disponible dans les listes d'images.`);
      } catch (error) {
        setMessage(escapeHtml(error.error || "L'import de l'image a echoue."), true);
      }
    }

    function refreshImageSelectOptions() {
      document.querySelectorAll('select[data-control="image-select"]').forEach((select) => {
        const value = currentValues[select.dataset.field] || select.value || "";
        select.innerHTML = `<option value="">Choisir une image...</option>` + currentImageOptions.map((image) => `<option value="${escapeAttr(image.src)}"${image.src === value ? " selected" : ""}>${escapeHtml(image.label || image.src)}</option>`).join("");
      });
    }

    function hasUnsavedChanges() {
      return collectChanges().some((change) => change.value !== (savedValues[change.field] || ""));
    }

    function updateSaveState() {
      const dirty = hasUnsavedChanges();
      const state = document.getElementById("saveState");
      const button = document.getElementById("saveButton");
      if (state) {
        state.textContent = dirty ? "Modifications non enregistrées" : "Article enregistré";
        state.classList.toggle("dirty", dirty);
      }
      if (button) button.disabled = !dirty;
    }

    function confirmDiscardUnsavedChanges() {
      if (!currentSlug || !hasUnsavedChanges()) return true;
      return window.confirm("Des modifications ne sont pas enregistrées. Changer d'article les fera perdre. Continuer ?");
    }

    async function validateArticle() {
      clearAllFieldErrors();
      setMessage("Vérification en cours...");
      const result = await api(`/api/articles/${encodeURIComponent(currentSlug)}/validate`, postPayload({ changes: collectChanges() }));
      renderResult(result, "Vérification terminée. Aucun blocage détecté.");
    }

    async function saveArticle() {
      if (!hasUnsavedChanges()) {
        setMessage("Aucune modification à enregistrer.");
        updateSaveState();
        return;
      }
      clearAllFieldErrors();
      setMessage("Enregistrement en cours...");
      try {
        const result = await api(`/api/articles/${encodeURIComponent(currentSlug)}/save`, postPayload({ changes: collectChanges() }));
        clearDraftPreview(currentSlug);
        recentBackups = (await api("/api/backups")).backups || [];
        await openArticle(currentSlug);
        renderResult(result, "Article enregistre. Une sauvegarde locale a ete creee avant l'enregistrement.");
      } catch (error) {
        renderResult(error, "L'enregistrement a échoué.");
      }
    }

    async function restoreBackup() {
      if (!confirmDiscardUnsavedChanges()) return;
      const select = document.getElementById("backupSelect");
      const backupId = select ? select.value : "";
      if (!backupId) {
        setMessage("Aucune sauvegarde locale a restaurer.", true);
        return;
      }
      const backup = recentBackups.find((item) => item.id === backupId);
      const label = backup ? backup.label : "la sauvegarde choisie";
      if (!window.confirm(`Restaurer la sauvegarde locale du ${label} ? L'etat actuel sera aussi sauvegarde avant la restauration.`)) return;

      clearAllFieldErrors();
      setMessage("Restauration de la sauvegarde locale en cours...");
      try {
        const result = await api("/api/backups/restore", postPayload({ backup_id: backupId }));
        articles = (await api("/api/articles")).articles;
        recentBackups = result.backups || (await api("/api/backups")).backups || [];
        if (currentSlug) {
          const stillExists = articles.some((article) => article.slug === currentSlug);
          if (stillExists) await openArticle(currentSlug);
          else {
            currentSlug = "";
            renderArticleList();
            document.getElementById("editor").innerHTML = `<p class="message">Sauvegarde restauree. Choisissez un article a modifier.</p>`;
          }
        }
        setMessage("Sauvegarde locale restauree. La verification du projet est passee.");
      } catch (error) {
        renderResult(error, "La restauration a echoue.");
      }
    }

    function postPayload(payload) {
      return { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) };
    }

    function renderResult(result, successMessage) {
      if (result.ok) {
        clearAllFieldErrors();
        setMessage(successMessage);
        return;
      }
      const errors = result.errors || [{ message: result.error || "Erreur inconnue." }];
      applyErrors(errors);
    }

    function setMessage(message, isError) {
      const box = document.getElementById("message");
      box.className = message ? "message" + (isError ? " error" : "") : "";
      box.innerHTML = message || "";
    }

    function applyErrors(errors) {
      clearAllFieldErrors();
      const items = errors.map((item) => ({ ...item, message: friendlyError(item) }));
      const firstFieldError = items.find((item) => item.field);
      if (firstFieldError) activateTab(tabForField(firstFieldError.field));
      items.forEach((item) => {
        if (!item.field) return;
        const row = fieldRow(item.field);
        const errorBox = document.getElementById(`${fieldDomId(item.field)}-error`);
        if (row && errorBox) {
          row.classList.add("has-error");
          errorBox.textContent = item.message;
        }
      });
      const list = items.map((item) => `<li>${escapeHtml(item.message)}</li>`).join("");
      setMessage(`<strong>${items.length} point${items.length > 1 ? "s" : ""} à corriger avant d'enregistrer.</strong><ul>${list}</ul>`, true);
    }

    function tabForField(fieldPath) {
      const group = groupForField(editorGroups(), { path: fieldPath });
      return group.tab || "essentiel";
    }

    function clearAllFieldErrors() {
      document.querySelectorAll(".field-row.has-error").forEach((row) => row.classList.remove("has-error"));
      document.querySelectorAll(".field-error").forEach((box) => box.textContent = "");
    }

    function clearFieldError(fieldPath) {
      const row = fieldRow(fieldPath);
      const errorBox = document.getElementById(`${fieldDomId(fieldPath)}-error`);
      if (row) row.classList.remove("has-error");
      if (errorBox) errorBox.textContent = "";
    }

    function fieldRow(fieldPath) {
      return Array.from(document.querySelectorAll("[data-field-row]")).find((row) => row.dataset.fieldRow === fieldPath);
    }

    function friendlyError(error) {
      const field = currentArticleFields.find((item) => item.path === error.field);
      const label = field ? displayLabel(field) : "";
      if (error.code === "required-field") return `${label || "Ce champ"} est obligatoire.`;
      if (error.code === "invalid-image") return `${label || "Cette image"} doit utiliser une image existante du projet.`;
      if (error.code === "invalid-choice") return `${label || "Ce choix"} contient une valeur non autorisée.`;
      if (error.code === "project-validation") return "La validation complète du projet a échoué. Rien n'a été enregistré.";
      return error.message || "Erreur inconnue.";
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
    }

    function escapeAttr(value) {
      return escapeHtml(value);
    }

    function encodeImagePath(src) {
      return String(src).split("/").map((part) => encodeURIComponent(part)).join("/");
    }

    window.addEventListener("beforeunload", (event) => {
      if (!hasUnsavedChanges()) return;
      event.preventDefault();
      event.returnValue = "";
    });

    init().catch((error) => {
      document.getElementById("editor").innerHTML = `<p class="message error">${escapeHtml(error.error || error.message || "L'éditeur n'a pas pu démarrer.")}</p>`;
    });
  </script>
</body>
</html>
"""
