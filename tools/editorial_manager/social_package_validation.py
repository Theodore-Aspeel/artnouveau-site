"""Validation helpers for exported social-package handoff payloads."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .social_package import SOCIAL_PACKAGE_CONTRACT_NAME, SOCIAL_PACKAGE_CONTRACT_VERSION


ALLOWED_QUEUE_STATUSES = {"candidate", "needs-review", "blocked"}
ALLOWED_READINESS_STATUSES = {"ready", "needs review", "blocked"}


@dataclass(frozen=True)
class SocialPackageValidationResult:
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def validate_social_package_file(path: str | Path) -> SocialPackageValidationResult:
    """Validate a JSON file exported from `social-package`."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as error:
        return SocialPackageValidationResult(False, (f"Could not read file: {error}",), ())
    except json.JSONDecodeError as error:
        return SocialPackageValidationResult(False, (f"Invalid JSON: {error}",), ())

    return validate_social_package_payload(payload)


def validate_social_package_payload(payload: Any) -> SocialPackageValidationResult:
    """Validate the minimal n8n-facing contract for a social package payload."""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return SocialPackageValidationResult(False, ("Payload must be a JSON object.",), ())

    contract = _mapping(payload, "contract", errors)
    if contract:
        _expect_equal(contract, "name", SOCIAL_PACKAGE_CONTRACT_NAME, errors)
        _expect_equal(contract, "version", SOCIAL_PACKAGE_CONTRACT_VERSION, errors)
        _expect_equal(contract, "kind", "read_only_social_handoff", errors)

    _expect_text(payload, "slug", errors)
    _expect_text(payload, "requested_locale", errors)
    _expect_text(payload, "source_locale", errors)

    queue_status = payload.get("queue_status")
    if queue_status not in ALLOWED_QUEUE_STATUSES:
        errors.append("queue_status must be one of: blocked, candidate, needs-review.")

    locale_status = _mapping(payload, "locale_status", errors)
    if locale_status:
        _expect_text(locale_status, "status", errors, path="locale_status.status")
        _expect_list(locale_status, "missing_fields", errors, path="locale_status.missing_fields")

    brief = _mapping(payload, "brief", errors)
    caption = _mapping(payload, "caption", errors)
    media = _mapping(payload, "media", errors)
    links = _mapping(payload, "links", errors)
    image_summary = _mapping(payload, "image_summary", errors)
    readiness = _mapping(payload, "readiness", errors)
    _expect_list(payload, "reasons", errors)

    if brief:
        _expect_text(brief, "slug", errors, path="brief.slug")

    if caption:
        _expect_text(caption, "slug", errors, path="caption.slug")
        _expect_text(caption, "source_locale", errors, path="caption.source_locale")
        _expect_list(caption, "hashtags", errors, path="caption.hashtags")

    if media:
        hero = _mapping(media, "hero", errors, path="media.hero")
        if hero:
            _expect_string(hero, "src", errors, path="media.hero.src")
            _expect_string(hero, "alt", errors, path="media.hero.alt")
            _expect_string(hero, "caption", errors, path="media.hero.caption")
        _expect_list(media, "support", errors, path="media.support")

    if links:
        _expect_text(links, "canonical_public_path", errors, path="links.canonical_public_path")
        public_paths = _mapping(links, "public_paths", errors, path="links.public_paths")
        if public_paths and not public_paths:
            errors.append("links.public_paths must not be empty.")

    if image_summary:
        if not isinstance(image_summary.get("has_hero"), bool):
            errors.append("image_summary.has_hero must be a boolean.")
        if not isinstance(image_summary.get("support_count"), int):
            errors.append("image_summary.support_count must be an integer.")

    if readiness:
        status = readiness.get("status")
        if status not in ALLOWED_READINESS_STATUSES:
            errors.append("readiness.status must be one of: blocked, needs review, ready.")
        _expect_list(readiness, "notes", errors, path="readiness.notes")

    if queue_status != "candidate":
        warnings.append("Payload is valid but queue_status is not candidate; n8n should stop before publishing.")

    return SocialPackageValidationResult(not errors, tuple(errors), tuple(warnings))


def _mapping(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    path: str | None = None,
) -> dict[str, Any]:
    value = payload.get(key)
    label = path or key
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object.")
        return {}
    return value


def _expect_equal(payload: dict[str, Any], key: str, expected: Any, errors: list[str]) -> None:
    if payload.get(key) != expected:
        errors.append(f"contract.{key} must be {expected!r}.")


def _expect_text(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    path: str | None = None,
) -> None:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path or key} must be a non-empty string.")


def _expect_string(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    path: str | None = None,
) -> None:
    if not isinstance(payload.get(key), str):
        errors.append(f"{path or key} must be a string.")


def _expect_list(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    path: str | None = None,
) -> None:
    if not isinstance(payload.get(key), list):
        errors.append(f"{path or key} must be an array.")
