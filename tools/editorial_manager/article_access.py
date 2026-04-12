"""Small read helpers for the mixed v1/v2 article model.

The functions in this module are intentionally simple and read-only. They do
not try to replace the JavaScript compatibility layer used by the runtime.
"""

from __future__ import annotations

from typing import Any


Article = dict[str, Any]


def normalize_text(value: Any) -> str:
    """Return a stripped string, or an empty string for non-string values."""
    return value.strip() if isinstance(value, str) else ""


def is_mapping(value: Any) -> bool:
    return isinstance(value, dict)


def article_model(article: Article) -> str:
    """Return the detected article model version: v1 or v2."""
    if article.get("schema_version") == 2 or is_mapping(article.get("content")):
        return "v2"
    return "v1"


def locale_content(article: Article, locale: str = "fr") -> dict[str, Any]:
    content = article.get("content")
    if not is_mapping(content):
        return {}

    selected = content.get(locale)
    if is_mapping(selected):
        return selected

    french = content.get("fr")
    if is_mapping(french):
        return french

    return {}


def article_title(article: Article, locale: str = "fr") -> str:
    content = locale_content(article, locale)
    return normalize_text(content.get("title")) or normalize_text(article.get("title"))


def article_dek(article: Article, locale: str = "fr") -> str:
    content = locale_content(article, locale)
    return normalize_text(content.get("dek")) or normalize_text(article.get("chapeau"))


def article_hero_image(article: Article) -> str:
    media = article.get("media")
    hero = media.get("hero") if is_mapping(media) else None
    hero_src = normalize_text(hero.get("src")) if is_mapping(hero) else ""
    return hero_src or normalize_text(article.get("hero_image"))


def article_meta_description(article: Article, locale: str = "fr") -> str:
    content = locale_content(article, locale)
    seo = content.get("seo") if content else None
    meta_description = normalize_text(seo.get("meta_description")) if is_mapping(seo) else ""
    return meta_description or normalize_text(article.get("meta_description"))


def article_status(article: Article) -> str:
    return normalize_text(article.get("status")) or "unknown"


def article_format(article: Article) -> str:
    return normalize_text(article.get("format")) or "unknown"


def article_publication_order(article: Article) -> int | None:
    publication = article.get("publication")
    if is_mapping(publication) and isinstance(publication.get("order"), int):
        return publication["order"]

    legacy_order = article.get("publication_order_recommended")
    return legacy_order if isinstance(legacy_order, int) else None


def article_taxonomy(article: Article) -> dict[str, str]:
    facts = article.get("facts")
    location = facts.get("location") if is_mapping(facts) else None
    taxonomy = article.get("taxonomy")

    style = normalize_text(taxonomy.get("style_key")) if is_mapping(taxonomy) else ""
    city = normalize_text(location.get("city")) if is_mapping(location) else ""
    country = normalize_text(location.get("country")) if is_mapping(location) else ""

    return {
        "style": style or normalize_text(article.get("style")),
        "city": city or normalize_text(article.get("city")),
        "country": country or normalize_text(article.get("country")),
    }


def article_sections_count(article: Article, locale: str = "fr") -> int:
    content = locale_content(article, locale)
    sections = content.get("sections") if content else article.get("sections")
    return len(sections) if isinstance(sections, list) else 0


def has_english_content(article: Article) -> bool:
    content = article.get("content")
    english = content.get("en") if is_mapping(content) else None
    return is_mapping(english) and any(bool(normalize_text(value)) for value in english.values())


def article_slug(article: Article) -> str:
    return normalize_text(article.get("slug"))
