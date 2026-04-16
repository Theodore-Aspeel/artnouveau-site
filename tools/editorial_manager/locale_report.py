"""Read-only locale status helpers for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .article_access import article_slug, is_mapping, locale_content, normalize_text


Article = dict[str, Any]


@dataclass(frozen=True)
class LocaleReportItem:
    slug: str
    status: str
    missing_fields: tuple[str, ...]


def analyze_article_locale(article: Article) -> LocaleReportItem:
    """Return a simple FR/EN editorial status for one article."""
    slug = article_slug(article) or "<missing slug>"
    french = locale_content(article, "fr")
    english = _raw_locale_content(article, "en")

    if not _has_real_text(english):
        return LocaleReportItem(slug, "fr-only", tuple(_required_field_names(french)))

    missing_fields = tuple(_missing_english_fields(french, english))
    status = "en-ready" if not missing_fields else "en-partial"
    return LocaleReportItem(slug, status, missing_fields)


def analyze_articles_locale(articles: list[Article]) -> list[LocaleReportItem]:
    return [analyze_article_locale(article) for article in articles]


def _raw_locale_content(article: Article, locale: str) -> dict[str, Any]:
    content = article.get("content")
    if not is_mapping(content):
        return {}

    selected = content.get(locale)
    return selected if is_mapping(selected) else {}


def _missing_english_fields(french: dict[str, Any], english: dict[str, Any]) -> list[str]:
    missing: list[str] = []

    if not normalize_text(english.get("title")):
        missing.append("title")

    if not normalize_text(english.get("dek")):
        missing.append("dek")

    seo = english.get("seo")
    if not is_mapping(seo) or not normalize_text(seo.get("meta_description")):
        missing.append("seo.meta_description")

    media = english.get("media")
    if not is_mapping(media) or not normalize_text(media.get("hero_alt")):
        missing.append("media.hero_alt")

    missing.extend(_missing_section_fields(french, english))
    return missing


def _missing_section_fields(french: dict[str, Any], english: dict[str, Any]) -> list[str]:
    french_sections = french.get("sections")
    if not isinstance(french_sections, list) or not french_sections:
        return []

    english_sections = english.get("sections")
    if not isinstance(english_sections, list) or not english_sections:
        return ["sections"]

    missing: list[str] = []
    if len(english_sections) < len(french_sections):
        missing.append("sections.count")

    for index, french_section in enumerate(french_sections):
        if not is_mapping(french_section):
            continue

        english_section = english_sections[index] if index < len(english_sections) else None
        if not is_mapping(english_section):
            continue

        if normalize_text(french_section.get("heading")) and not normalize_text(english_section.get("heading")):
            missing.append(f"sections[{index + 1}].heading")

        if normalize_text(french_section.get("body")) and not normalize_text(english_section.get("body")):
            missing.append(f"sections[{index + 1}].body")

    return missing


def _required_field_names(french: dict[str, Any]) -> list[str]:
    names = ["title", "dek", "seo.meta_description", "media.hero_alt"]
    if isinstance(french.get("sections"), list) and french["sections"]:
        names.append("sections")
    return names


def _has_real_text(value: Any) -> bool:
    if isinstance(value, str):
        return bool(normalize_text(value))

    if is_mapping(value):
        return any(_has_real_text(item) for item in value.values())

    if isinstance(value, list):
        return any(_has_real_text(item) for item in value)

    return False
