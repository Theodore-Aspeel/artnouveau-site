"""Read-only helpers for future FR-source translation synchronization.

The helpers in this module do not translate, write article data, or decide
whether a manual localized edit should be replaced. They provide a stable way
to name French source units and fingerprint their current text so a later
workflow can compare a stored source hash with the current source hash.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

from .article_access import is_mapping, normalize_text
from .locales import DEFAULT_LOCALE, normalize_locale


Article = dict[str, Any]
SyncState = dict[str, str]

LOCALIZED_TEXT_PATHS = (
    ("title",),
    ("dek",),
    ("epigraph",),
    ("seo", "meta_description"),
    ("media", "hero_alt"),
    ("around", "note"),
)


@dataclass(frozen=True)
class TranslationSyncUnit:
    path: str
    source_locale: str
    target_locale: str
    source_text: str
    source_hash: str
    target_text: str
    status: str


@dataclass(frozen=True)
class TranslationSyncReport:
    slug: str
    source_locale: str
    target_locale: str
    units: tuple[TranslationSyncUnit, ...]

    @property
    def missing_count(self) -> int:
        return _count_units(self.units, "missing")

    @property
    def source_changed_count(self) -> int:
        return _count_units(self.units, "source-changed")


def analyze_translation_sync(
    article: Article,
    target_locale: str,
    previous_source_hashes: SyncState | None = None,
) -> TranslationSyncReport:
    """Compare French source units with one target locale.

    ``previous_source_hashes`` is intentionally optional and external. A future
    workflow can store it in an internal state file after translation. When no
    previous hash is known, an existing target text is reported as
    ``localized-untracked`` instead of assuming it is safe to overwrite.
    """

    target_locale = normalize_locale(target_locale)
    source_locale = DEFAULT_LOCALE
    source = _locale_content(article, source_locale)
    target = _locale_content(article, target_locale)
    previous_source_hashes = previous_source_hashes or {}

    units = tuple(
        _build_unit(path, source_text, target, source_locale, target_locale, previous_source_hashes)
        for path, source_text in iter_source_units(source)
    )
    return TranslationSyncReport(
        slug=normalize_text(article.get("slug")) or "<missing slug>",
        source_locale=source_locale,
        target_locale=target_locale,
        units=units,
    )


def iter_source_units(source_content: dict[str, Any]) -> tuple[tuple[str, str], ...]:
    """Return stable paths and texts for translatable French source units."""

    units: list[tuple[str, str]] = []

    for path_parts in LOCALIZED_TEXT_PATHS:
        text = normalize_text(_get_nested(source_content, path_parts))
        if text:
            units.append((".".join(path_parts), text))

    sections = source_content.get("sections")
    if isinstance(sections, list):
        for index, section in enumerate(sections):
            if not is_mapping(section):
                continue
            for field in ("heading", "body"):
                text = normalize_text(section.get(field))
                if text:
                    units.append((f"sections[{index + 1}].{field}", text))

    practical_items = source_content.get("practical_items")
    if isinstance(practical_items, list):
        for item in practical_items:
            if not is_mapping(item):
                continue
            key = normalize_text(item.get("key"))
            value = normalize_text(item.get("value"))
            if key and value:
                units.append((f"practical_items.{key}.value", value))

    return tuple(units)


def source_text_hash(value: str) -> str:
    normalized = normalize_text(value).replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _build_unit(
    path: str,
    source_text: str,
    target_content: dict[str, Any],
    source_locale: str,
    target_locale: str,
    previous_source_hashes: SyncState,
) -> TranslationSyncUnit:
    current_hash = source_text_hash(source_text)
    target_text = _target_text_for_path(target_content, path)
    previous_hash = previous_source_hashes.get(path)

    if not target_text:
        status = "missing"
    elif previous_hash is None:
        status = "localized-untracked"
    elif previous_hash == current_hash:
        status = "current"
    else:
        status = "source-changed"

    return TranslationSyncUnit(
        path=path,
        source_locale=source_locale,
        target_locale=target_locale,
        source_text=source_text,
        source_hash=current_hash,
        target_text=target_text,
        status=status,
    )


def _locale_content(article: Article, locale: str) -> dict[str, Any]:
    content = article.get("content")
    if not is_mapping(content):
        return {}

    selected = content.get(locale)
    return selected if is_mapping(selected) else {}


def _target_text_for_path(target_content: dict[str, Any], path: str) -> str:
    if path.startswith("sections["):
        return _section_target_text(target_content, path)
    if path.startswith("practical_items."):
        return _practical_target_text(target_content, path)
    return normalize_text(_get_nested(target_content, tuple(path.split("."))))


def _section_target_text(target_content: dict[str, Any], path: str) -> str:
    prefix, field = path.split(".", 1)
    index_text = prefix.removeprefix("sections[").removesuffix("]")
    if not index_text.isdigit():
        return ""

    sections = target_content.get("sections")
    index = int(index_text) - 1
    if not isinstance(sections, list) or index < 0 or index >= len(sections):
        return ""

    section = sections[index]
    return normalize_text(section.get(field)) if is_mapping(section) else ""


def _practical_target_text(target_content: dict[str, Any], path: str) -> str:
    parts = path.split(".")
    if len(parts) != 3 or parts[0] != "practical_items" or parts[2] != "value":
        return ""

    expected_key = parts[1]
    practical_items = target_content.get("practical_items")
    if not isinstance(practical_items, list):
        return ""

    for item in practical_items:
        if is_mapping(item) and normalize_text(item.get("key")) == expected_key:
            return normalize_text(item.get("value"))
    return ""


def _get_nested(value: dict[str, Any], path_parts: tuple[str, ...]) -> Any:
    current: Any = value
    for part in path_parts:
        if not is_mapping(current):
            return ""
        current = current.get(part)
    return current


def _count_units(units: tuple[TranslationSyncUnit, ...], status: str) -> int:
    return sum(1 for unit in units if unit.status == status)
