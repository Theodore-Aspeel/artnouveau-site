"""Read-only locale status helpers for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .article_access import article_slug, is_mapping, locale_content, normalize_text
from .locales import DEFAULT_LOCALE, normalize_locale


Article = dict[str, Any]


@dataclass(frozen=True)
class LocaleReportItem:
    slug: str
    status: str
    missing_fields: tuple[str, ...]
    target_locale: str = "en"


def analyze_article_locale(article: Article, target_locale: str = "en") -> LocaleReportItem:
    """Return a simple source/target editorial status for one article."""
    slug = article_slug(article) or "<missing slug>"
    source = locale_content(article, DEFAULT_LOCALE)
    target_locale = normalize_locale(target_locale)
    target = _raw_locale_content(article, target_locale)

    if not _has_real_text(target):
        return LocaleReportItem(
            slug,
            missing_locale_status(target_locale),
            tuple(_required_field_names(source)),
            target_locale,
        )

    missing_fields = tuple(_missing_target_fields(source, target))
    status = f"{target_locale}-ready" if not missing_fields else f"{target_locale}-partial"
    return LocaleReportItem(slug, status, missing_fields, target_locale)


def analyze_articles_locale(articles: list[Article], target_locale: str = "en") -> list[LocaleReportItem]:
    return [analyze_article_locale(article, target_locale) for article in articles]


def missing_locale_status(target_locale: str) -> str:
    """Keep the historic EN status while making newer preview locales explicit."""
    normalized = normalize_locale(target_locale)
    return "fr-only" if normalized == "en" else f"{normalized}-missing"


def _raw_locale_content(article: Article, locale: str) -> dict[str, Any]:
    content = article.get("content")
    if not is_mapping(content):
        return {}

    selected = content.get(locale)
    return selected if is_mapping(selected) else {}


def _missing_target_fields(source: dict[str, Any], target: dict[str, Any]) -> list[str]:
    missing: list[str] = []

    if not normalize_text(target.get("title")):
        missing.append("title")

    if not normalize_text(target.get("dek")):
        missing.append("dek")

    seo = target.get("seo")
    if not is_mapping(seo) or not normalize_text(seo.get("meta_description")):
        missing.append("seo.meta_description")

    media = target.get("media")
    if not is_mapping(media) or not normalize_text(media.get("hero_alt")):
        missing.append("media.hero_alt")

    missing.extend(_missing_section_fields(source, target))
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
