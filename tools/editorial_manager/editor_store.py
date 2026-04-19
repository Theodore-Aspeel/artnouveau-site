"""Controlled read/write operations for the local article editor."""

from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any, Callable
from urllib.parse import quote

from .article_access import article_hero_image, article_publication_order, article_slug, article_title
from .checks import publication_check_article
from .editor_backups import create_articles_backup
from .editor_fields import (
    article_editable_locale_codes,
    editable_field_for_path,
    editable_field_value_payload,
    editable_fields_for_article,
    get_path,
    set_path,
)
from .editor_images import is_valid_editor_image_src, list_editor_image_options, project_root_from_articles_path
from .locale_report import analyze_article_locale
from .locales import DEFAULT_LOCALE, SUPPORTED_LOCALES, editable_locale_specs, preview_locale_codes
from .repository import ARTICLES_JSON, PROJECT_ROOT


Article = dict[str, Any]
Payload = dict[str, Any]
Validator = Callable[[], tuple[bool, list[str]]]


def load_article_payload(path: Path = ARTICLES_JSON) -> Payload:
    with path.open("r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("articles"), list):
        raise ValueError(f"{path} must contain an articles list.")
    return payload


def list_editor_articles(payload: Payload) -> list[dict[str, Any]]:
    articles = [article for article in payload.get("articles", []) if isinstance(article, dict)]
    rows = []
    for article in sorted(articles, key=lambda item: article_publication_order(item) or 999_999):
        rows.append(
            {
                "slug": article_slug(article),
                "title": article_title(article, "fr"),
                "title_en": article_title(article, "en"),
                "status": str(article.get("status") or ""),
                "order": article_publication_order(article),
                "has_hero": bool(article_hero_image(article)),
                "locale_statuses": editor_locale_statuses(article),
            }
        )
    return rows


def find_payload_article(payload: Payload, slug: str) -> Article | None:
    for article in payload.get("articles", []):
        if isinstance(article, dict) and article.get("slug") == slug:
            return article
    return None


def build_editor_article_payload(article: Article, project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    slug = article_slug(article)
    return {
        "slug": slug,
        "title": article_title(article, "fr"),
        "title_en": article_title(article, "en"),
        "status": str(article.get("status") or ""),
        "order": article_publication_order(article),
        "hero_src": article_hero_image(article),
        "support_images": current_support_images(article),
        "preview_urls": build_preview_urls(slug),
        "locale_contract": editor_locale_contract(article),
        "locale_statuses": editor_locale_statuses(article),
        "image_options": list_editor_image_options(project_root),
        "fields": [editable_field_value_payload(article, field) for field in editable_fields_for_article(article)],
        "checks": validate_article_for_editor(article, project_root=project_root),
    }


def build_preview_urls(slug: str) -> dict[str, str]:
    encoded_slug = quote(slug, safe="")
    article_url = f"article.html?slug={encoded_slug}"
    urls = {}
    for locale in preview_locale_codes():
        urls[locale] = article_url if locale == DEFAULT_LOCALE else f"{article_url}&previewLocale={locale}"
    return urls


def editor_locale_contract(article: Article | None = None) -> dict[str, Any]:
    editable_codes = (
        list(article_editable_locale_codes(article))
        if article is not None
        else [locale.code for locale in editable_locale_specs()]
    )
    preview_codes = [locale for locale in preview_locale_codes() if locale in editable_codes]
    return {
        "default": DEFAULT_LOCALE,
        "supported": [
            {
                "code": locale.code,
                "label": locale.label,
                "required": locale.required,
                "public": locale.public,
                "preview": locale.preview,
                "editable": locale.editable,
            }
            for locale in SUPPORTED_LOCALES
        ],
        "editable": editable_codes,
        "preview": preview_codes,
    }


def editor_locale_statuses(article: Article) -> dict[str, dict[str, Any]]:
    statuses: dict[str, dict[str, Any]] = {}
    for locale in preview_locale_codes():
        if locale == DEFAULT_LOCALE:
            continue
        item = analyze_article_locale(article, locale)
        statuses[locale] = {
            "status": item.status,
            "missing_fields": list(item.missing_fields),
        }
    return statuses


def validate_changes(
    article: Article,
    changes: list[dict[str, Any]],
    project_root: Path = PROJECT_ROOT,
) -> list[dict[str, str]]:
    draft = deepcopy(article)
    errors = apply_changes(draft, changes, project_root=project_root)
    if errors:
        return errors
    return validate_article_for_editor(draft, project_root=project_root)


def save_article_changes(
    slug: str,
    changes: list[dict[str, Any]],
    path: Path = ARTICLES_JSON,
    validator: Validator | None = None,
) -> dict[str, Any]:
    payload = load_article_payload(path)
    original_payload = deepcopy(payload)
    project_root = project_root_from_articles_path(path)
    article = find_payload_article(payload, slug)
    if article is None:
        return {"ok": False, "errors": [error("unknown-slug", f"Unknown article slug: {slug}.")]}

    errors = apply_changes(article, changes, project_root=project_root)
    if not errors:
        errors = validate_article_for_editor(article, project_root=project_root)
    if errors:
        return {"ok": False, "errors": errors}

    try:
        backup = create_articles_backup(path, project_root=project_root)
    except Exception as exc:
        return {
            "ok": False,
            "errors": [
                error(
                    "backup-failed",
                    f"La sauvegarde locale de securite n'a pas pu etre creee. Rien n'a ete enregistre: {exc}",
                )
            ],
        }

    write_payload_atomic(path, payload)
    validate = validator or run_project_validation
    try:
        ok, validation_errors = validate()
    except Exception as exc:
        ok = False
        validation_errors = [f"Project validation could not run: {exc}"]

    if not ok:
        write_payload_atomic(path, original_payload)
        return {
            "ok": False,
            "errors": [error("project-validation", message) for message in validation_errors],
            "rolled_back": True,
        }

    return {
        "ok": True,
        "article": build_editor_article_payload(article, project_root=project_root),
        "backup": backup,
        "message": "Article saved and validation passed.",
    }


def apply_changes(
    article: Article,
    changes: list[dict[str, Any]],
    project_root: Path = PROJECT_ROOT,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(changes, list):
        return [error("invalid-payload", "Changes must be a list.")]

    for index, change in enumerate(changes):
        if not isinstance(change, dict):
            errors.append(error("invalid-change", f"Change #{index + 1} must be an object."))
            continue

        field_path = str(change.get("field") or "")
        field = editable_field_for_path(article, field_path)
        if field is None:
            errors.append(error("field-not-editable", f"{field_path or '<empty>'} is not editable.", field_path))
            continue

        value = normalize_edit_value(change.get("value"))
        if field.choices and value not in field.choices:
            errors.append(
                error("invalid-choice", f"{field.label} must be one of {', '.join(field.choices)}.", field_path)
            )
            continue
        if field.control == "image-select" and not is_valid_editor_image_src(value, project_root):
            errors.append(error("invalid-image", f"{field.label} doit etre une image existante sous assets/images.", field_path))
            continue

        set_path(article, field_path, value)

    return errors


def validate_article_for_editor(article: Article, project_root: Path = PROJECT_ROOT) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    for field in editable_fields_for_article(article):
        value = normalize_edit_value(get_path(article, field.path))
        if field.required and not value:
            errors.append(error("required-field", f"{field.label} is required.", field.path))
        if field.choices and value and value not in field.choices:
            errors.append(error("invalid-choice", f"{field.label} must be one of {', '.join(field.choices)}.", field.path))
        if field.control == "image-select" and value and not is_valid_editor_image_src(value, project_root):
            errors.append(error("invalid-image", f"{field.label} doit etre une image existante sous assets/images.", field.path))

    publication_errors = [item for item in publication_check_article(article) if item.status == "ERROR"]
    for item in publication_errors:
        errors.append(error(item.code, item.message))

    return errors


def normalize_edit_value(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def current_support_images(article: Article) -> list[dict[str, Any]]:
    support = get_path(article, "media.support")
    if not isinstance(support, list):
        return []

    images: list[dict[str, Any]] = []
    for index, item in enumerate(support):
        if not isinstance(item, dict):
            continue
        images.append({"index": index, "src": normalize_edit_value(item.get("src"))})
    return images


def write_payload_atomic(path: Path, payload: Payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as file_handle:
        temp_path = Path(file_handle.name)
        file_handle.write(data)

    temp_path.replace(path)


def run_project_validation() -> tuple[bool, list[str]]:
    completed = subprocess.run(
        [npm_executable(), "run", "validate"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return True, []

    messages = [completed.stdout.strip(), completed.stderr.strip()]
    return False, [message for message in messages if message]


def npm_executable() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"


def error(code: str, message: str, field: str = "") -> dict[str, str]:
    payload = {"code": code, "message": message}
    if field:
        payload["field"] = field
    return payload
