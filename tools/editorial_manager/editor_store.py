"""Controlled read/write operations for the local article editor."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any, Callable

from .article_access import article_hero_image, article_publication_order, article_slug, article_title
from .checks import publication_check_article
from .editor_fields import editable_field_for_path, editable_field_value_payload, editable_fields_for_article, get_path, set_path
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
            }
        )
    return rows


def find_payload_article(payload: Payload, slug: str) -> Article | None:
    for article in payload.get("articles", []):
        if isinstance(article, dict) and article.get("slug") == slug:
            return article
    return None


def build_editor_article_payload(article: Article) -> dict[str, Any]:
    return {
        "slug": article_slug(article),
        "title": article_title(article, "fr"),
        "title_en": article_title(article, "en"),
        "status": str(article.get("status") or ""),
        "order": article_publication_order(article),
        "hero_src": article_hero_image(article),
        "fields": [editable_field_value_payload(article, field) for field in editable_fields_for_article(article)],
        "checks": validate_article_for_editor(article),
    }


def validate_changes(article: Article, changes: list[dict[str, Any]]) -> list[dict[str, str]]:
    draft = deepcopy(article)
    errors = apply_changes(draft, changes)
    if errors:
        return errors
    return validate_article_for_editor(draft)


def save_article_changes(
    slug: str,
    changes: list[dict[str, Any]],
    path: Path = ARTICLES_JSON,
    validator: Validator | None = None,
) -> dict[str, Any]:
    payload = load_article_payload(path)
    original_payload = deepcopy(payload)
    article = find_payload_article(payload, slug)
    if article is None:
        return {"ok": False, "errors": [error("unknown-slug", f"Unknown article slug: {slug}.")]}

    errors = apply_changes(article, changes)
    if not errors:
        errors = validate_article_for_editor(article)
    if errors:
        return {"ok": False, "errors": errors}

    write_payload_atomic(path, payload)
    validate = validator or run_project_validation
    ok, validation_errors = validate()
    if not ok:
        write_payload_atomic(path, original_payload)
        return {
            "ok": False,
            "errors": [error("project-validation", message) for message in validation_errors],
            "rolled_back": True,
        }

    return {
        "ok": True,
        "article": build_editor_article_payload(article),
        "message": "Article saved and validation passed.",
    }


def apply_changes(article: Article, changes: list[dict[str, Any]]) -> list[dict[str, str]]:
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
            errors.append(error("field-not-editable", f"{field_path or '<empty>'} is not editable."))
            continue

        value = normalize_edit_value(change.get("value"))
        if field.choices and value not in field.choices:
            errors.append(error("invalid-choice", f"{field.label} must be one of {', '.join(field.choices)}."))
            continue

        set_path(article, field_path, value)

    return errors


def validate_article_for_editor(article: Article) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    for field in editable_fields_for_article(article):
        value = normalize_edit_value(get_path(article, field.path))
        if field.required and not value:
            errors.append(error("required-field", f"{field.label} is required."))
        if field.choices and value and value not in field.choices:
            errors.append(error("invalid-choice", f"{field.label} must be one of {', '.join(field.choices)}."))

    publication_errors = [item for item in publication_check_article(article) if item.status == "ERROR"]
    for item in publication_errors:
        errors.append(error(item.code, item.message))

    return errors


def normalize_edit_value(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def write_payload_atomic(path: Path, payload: Payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as file_handle:
        temp_path = Path(file_handle.name)
        file_handle.write(data)

    temp_path.replace(path)


def run_project_validation() -> tuple[bool, list[str]]:
    completed = subprocess.run(
        ["npm", "run", "validate"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return True, []

    messages = [completed.stdout.strip(), completed.stderr.strip()]
    return False, [message for message in messages if message]


def error(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}
