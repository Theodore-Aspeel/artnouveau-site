"""Tiny local browser editor served by the Editorial Manager."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from typing import Any
from urllib.parse import unquote, urlparse
import webbrowser

from .editor_fields import editable_field_payload
from .editor_images import editor_image_path
from .editor_store import (
    build_editor_article_payload,
    find_payload_article,
    list_editor_articles,
    load_article_payload,
    save_article_changes,
    validate_changes,
)
from .repository import ARTICLES_JSON


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

        if route.startswith("/assets/images/"):
            image_path = editor_image_path(unquote(route.lstrip("/")))
            if image_path is None:
                self.send_json({"error": "Image not found."}, HTTPStatus.NOT_FOUND)
                return
            self.send_file(image_path)
            return

        if route == "/api/fields":
            self.send_json({"fields": editable_field_payload()})
            return

        if route == "/api/articles":
            payload = load_article_payload(ARTICLES_JSON)
            self.send_json({"articles": list_editor_articles(payload)})
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


def route_slug(route: str, prefix: str) -> str:
    if not route.startswith(prefix):
        return ""
    slug = route[len(prefix):].strip("/")
    if not slug or "/" in slug:
        return ""
    return unquote(slug)


EDITOR_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Éditeur éditorial</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; color: #1f2933; background: #f6f7f8; }
    header { padding: 16px 24px; background: #ffffff; border-bottom: 1px solid #d9dee3; }
    main { display: grid; grid-template-columns: 320px 1fr; min-height: calc(100vh - 66px); }
    aside { border-right: 1px solid #d9dee3; background: #ffffff; overflow: auto; }
    section { padding: 20px; overflow: auto; }
    h1 { margin: 0; font-size: 22px; }
    h2 { margin: 0 0 12px; font-size: 20px; }
    button, select, input, textarea { font: inherit; }
    button { border: 1px solid #9aa6b2; border-radius: 6px; background: #ffffff; padding: 8px 10px; cursor: pointer; }
    button.primary { background: #155e75; color: #ffffff; border-color: #155e75; }
    button:disabled { cursor: not-allowed; opacity: 0.55; }
    .article-button { display: block; width: 100%; text-align: left; border: 0; border-bottom: 1px solid #e4e8eb; border-radius: 0; padding: 12px 14px; }
    .article-button.active { background: #e7f2f5; }
    .meta { color: #617080; font-size: 13px; margin-top: 4px; }
    .form-grid { display: grid; gap: 14px; max-width: 960px; }
    label { display: grid; gap: 6px; font-weight: 700; }
    input, textarea, select { border: 1px solid #b8c2cc; border-radius: 6px; padding: 9px; background: #ffffff; }
    textarea { min-height: 96px; resize: vertical; }
    .hero-preview { display: grid; gap: 8px; max-width: 420px; margin: 14px 0; }
    .hero-preview img { width: 100%; max-height: 280px; object-fit: cover; border-radius: 6px; border: 1px solid #d9dee3; background: #ffffff; }
    .hero-preview .empty { padding: 12px; border: 1px solid #d9dee3; border-radius: 6px; background: #ffffff; }
    fieldset { border: 1px solid #d9dee3; border-radius: 6px; padding: 14px; background: #ffffff; }
    legend { padding: 0 6px; font-weight: 700; }
    .field-group { display: grid; gap: 14px; }
    .actions { display: flex; gap: 10px; margin: 16px 0; }
    .message { margin: 12px 0; padding: 10px; border-radius: 6px; background: #eef6ee; }
    .message.error { background: #fbeaea; }
    .empty { color: #617080; }
    @media (max-width: 760px) { main { grid-template-columns: 1fr; } aside { max-height: 40vh; border-right: 0; border-bottom: 1px solid #d9dee3; } }
  </style>
</head>
<body>
  <header>
    <h1>Éditeur éditorial</h1>
  </header>
  <main>
    <aside id="articleList"></aside>
    <section>
      <div id="editor"><p class="empty">Choisissez un article à modifier.</p></div>
    </section>
  </main>
  <script>
    let fields = [];
    let articles = [];
    let currentSlug = "";
    let currentValues = {};
    let currentImageOptions = [];

    async function api(path, options) {
      const response = await fetch(path, options);
      const data = await response.json();
      if (!response.ok) throw data;
      return data;
    }

    async function init() {
      fields = (await api("/api/fields")).fields;
      articles = (await api("/api/articles")).articles;
      renderArticleList();
    }

    function renderArticleList() {
      const list = document.getElementById("articleList");
      list.innerHTML = "";
      articles.forEach((article) => {
        const button = document.createElement("button");
        button.className = "article-button" + (article.slug === currentSlug ? " active" : "");
        button.innerHTML = `<strong>${escapeHtml(article.title || article.slug)}</strong><div class="meta">${escapeHtml(article.status || "-")} · ${article.has_hero ? "image principale" : "pas d'image principale"}</div>`;
        button.addEventListener("click", () => openArticle(article.slug));
        list.appendChild(button);
      });
    }

    async function openArticle(slug) {
      const article = await api(`/api/articles/${encodeURIComponent(slug)}`);
      currentSlug = slug;
      currentValues = {};
      article.fields.forEach((item) => currentValues[item.path] = item.value || "");
      currentImageOptions = article.image_options || [];
      renderArticleList();
      renderEditor(article);
    }

    function renderEditor(article) {
      const editor = document.getElementById("editor");
      const controls = renderFieldGroups(article.fields || []);
      editor.innerHTML = `
        <h2>${escapeHtml(article.title || article.slug)}</h2>
        <div class="meta">Slug: ${escapeHtml(article.slug)} · Image principale: ${escapeHtml(article.hero_src || "-")}</div>
        ${renderHeroPreview(article.hero_src || "")}
        <div class="actions">
          <button id="validateButton">Valider</button>
          <button id="saveButton" class="primary">Enregistrer</button>
        </div>
        <div id="message"></div>
        <form class="form-grid" id="articleForm">${controls}</form>
      `;
      document.getElementById("validateButton").addEventListener("click", validateArticle);
      document.getElementById("saveButton").addEventListener("click", saveArticle);
      const heroSelect = document.querySelector('[data-field="media.hero.src"]');
      if (heroSelect) {
        heroSelect.addEventListener("change", () => {
          currentValues["media.hero.src"] = heroSelect.value;
          const preview = document.getElementById("heroPreview");
          if (preview) preview.outerHTML = renderHeroPreview(heroSelect.value);
        });
      }
    }

    function renderHeroPreview(src) {
      if (!src) {
        return `<div class="hero-preview" id="heroPreview"><strong>Image principale actuelle</strong><p class="empty">Aucune image principale.</p></div>`;
      }
      return `
        <div class="hero-preview" id="heroPreview">
          <strong>Image principale actuelle</strong>
          <img src="/${escapeAttr(encodeImagePath(src))}" alt="">
          <div class="meta">${escapeHtml(src)}</div>
        </div>
      `;
    }

    function renderFieldGroups(articleFields) {
      const groups = [];
      articleFields.forEach((field) => {
        let group = groups.find((item) => item.name === (field.group || "Champs principaux"));
        if (!group) {
          group = { name: field.group || "Champs principaux", fields: [] };
          groups.push(group);
        }
        group.fields.push(field);
      });

      return groups.map((group) => {
        const controls = group.fields.map((field) => renderField(field, currentValues[field.path] || "")).join("");
        return `<fieldset><legend>${escapeHtml(group.name)}</legend><div class="field-group">${controls}</div></fieldset>`;
      }).join("");
    }

    function renderField(field, value) {
      const required = field.required ? " required" : "";
      if (field.control === "select") {
        const options = field.choices.map((choice) => `<option value="${escapeAttr(choice)}"${choice === value ? " selected" : ""}>${escapeHtml(choice)}</option>`).join("");
        return `<label>${escapeHtml(field.label)}<select data-field="${escapeAttr(field.path)}"${required}>${options}</select></label>`;
      }
      if (field.control === "image-select") {
        const options = `<option value="">Choisir une image...</option>` + currentImageOptions.map((image) => `<option value="${escapeAttr(image.src)}"${image.src === value ? " selected" : ""}>${escapeHtml(image.label || image.src)}</option>`).join("");
        return `<label>${escapeHtml(field.label)}<select data-field="${escapeAttr(field.path)}"${required}>${options}</select></label>`;
      }
      if (field.control === "textarea") {
        return `<label>${escapeHtml(field.label)}<textarea data-field="${escapeAttr(field.path)}"${required}>${escapeHtml(value)}</textarea></label>`;
      }
      return `<label>${escapeHtml(field.label)}<input data-field="${escapeAttr(field.path)}" value="${escapeAttr(value)}"${required}></label>`;
    }

    function collectChanges() {
      return Array.from(document.querySelectorAll("[data-field]")).map((control) => ({
        field: control.dataset.field,
        value: control.value
      }));
    }

    async function validateArticle() {
      setMessage("Validation en cours...");
      const result = await api(`/api/articles/${encodeURIComponent(currentSlug)}/validate`, postPayload({ changes: collectChanges() }));
      renderResult(result, "Validation réussie.");
    }

    async function saveArticle() {
      setMessage("Enregistrement en cours...");
      try {
        const result = await api(`/api/articles/${encodeURIComponent(currentSlug)}/save`, postPayload({ changes: collectChanges() }));
        await openArticle(currentSlug);
        renderResult(result, result.message || "Enregistrement réussi.");
      } catch (error) {
        renderResult(error, "L'enregistrement a échoué.");
      }
    }

    function postPayload(payload) {
      return { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) };
    }

    function renderResult(result, successMessage) {
      if (result.ok) {
        setMessage(successMessage);
        return;
      }
      const errors = result.errors || [{ message: result.error || "Erreur inconnue." }];
      setMessage(errors.map((item) => `${item.code || "error"}: ${item.message}`).join("<br>"), true);
    }

    function setMessage(message, isError) {
      const box = document.getElementById("message");
      box.className = message ? "message" + (isError ? " error" : "") : "";
      box.innerHTML = message || "";
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

    init().catch((error) => {
      document.getElementById("editor").innerHTML = `<p class="message error">${escapeHtml(error.error || error.message || "L'éditeur n'a pas pu démarrer.")}</p>`;
    });
  </script>
</body>
</html>
"""
