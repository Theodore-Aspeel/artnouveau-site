"""Read-only social publication brief helpers for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .article_access import (
    article_dek,
    article_hero_image,
    article_slug,
    article_title,
    article_taxonomy,
    is_mapping,
    locale_content,
    normalize_text,
)
from .checks import PublicationCheckItem, publication_check_article
from .locale_report import LocaleReportItem, analyze_article_locale


Article = dict[str, Any]


@dataclass(frozen=True)
class PracticalItem:
    key: str
    value: str


@dataclass(frozen=True)
class QuoteBrief:
    text_fr: str
    text_en: str
    author: str
    attribution_fr: str
    attribution_en: str


@dataclass(frozen=True)
class ImagePresence:
    has_hero: bool
    hero_src: str
    support_count: int


@dataclass(frozen=True)
class ReadinessBrief:
    status: str
    ok_count: int
    error_count: int
    warning_count: int
    notes: tuple[str, ...]


@dataclass(frozen=True)
class SocialBrief:
    slug: str
    title_fr: str
    title_en: str
    locale_status: LocaleReportItem
    dek_fr: str
    dek_en: str
    quote: QuoteBrief | None
    practical_items: tuple[PracticalItem, ...]
    images: ImagePresence
    readiness: ReadinessBrief


def build_social_brief(article: Article) -> SocialBrief:
    """Build a compact human-readable publication brief for one article."""
    locale_status = analyze_article_locale(article)
    return SocialBrief(
        slug=article_slug(article) or "<missing slug>",
        title_fr=article_title(article, "fr"),
        title_en=_localized_text(article, "en", "title"),
        locale_status=locale_status,
        dek_fr=article_dek(article, "fr"),
        dek_en=_localized_text(article, "en", "dek"),
        quote=_quote_brief(article),
        practical_items=tuple(_practical_items(article)),
        images=_image_presence(article),
        readiness=_readiness_brief(publication_check_article(article)),
    )


def _localized_text(article: Article, locale: str, field: str) -> str:
    content = article.get("content")
    selected = content.get(locale) if is_mapping(content) else None
    if not is_mapping(selected):
        return ""
    return normalize_text(selected.get(field))


def _quote_brief(article: Article) -> QuoteBrief | None:
    sources = article.get("sources")
    quote = sources.get("quote") if is_mapping(sources) else None
    if not is_mapping(quote):
        return None

    text = quote.get("text")
    attribution = quote.get("attribution")
    text_fr = normalize_text(text.get("fr")) if is_mapping(text) else normalize_text(quote.get("text"))
    text_en = normalize_text(text.get("en")) if is_mapping(text) else ""

    if not text_fr and not text_en:
        return None

    return QuoteBrief(
        text_fr=text_fr,
        text_en=text_en,
        author=normalize_text(quote.get("author")),
        attribution_fr=normalize_text(attribution.get("fr")) if is_mapping(attribution) else "",
        attribution_en=normalize_text(attribution.get("en")) if is_mapping(attribution) else "",
    )


def _practical_items(article: Article) -> list[PracticalItem]:
    content = locale_content(article, "fr")
    raw_items = content.get("practical_items")
    items: list[PracticalItem] = []

    if isinstance(raw_items, list):
        for item in raw_items:
            if not is_mapping(item):
                continue
            key = normalize_text(item.get("key"))
            value = normalize_text(item.get("value"))
            if key and value:
                items.append(PracticalItem(key, value))

    if items:
        return items

    taxonomy = article_taxonomy(article)
    return [
        PracticalItem(key, value)
        for key, value in (
            ("city", taxonomy["city"]),
            ("country", taxonomy["country"]),
            ("style", taxonomy["style"]),
        )
        if value
    ]


def _image_presence(article: Article) -> ImagePresence:
    hero_src = article_hero_image(article)
    media = article.get("media")
    support = media.get("support") if is_mapping(media) else None
    support_count = 0

    if isinstance(support, list):
        support_count = sum(
            1
            for item in support
            if is_mapping(item) and normalize_text(item.get("src"))
        )

    return ImagePresence(bool(hero_src), hero_src, support_count)


def _readiness_brief(items: list[PublicationCheckItem]) -> ReadinessBrief:
    errors = [item for item in items if item.status == "ERROR"]
    warnings = [item for item in items if item.status == "WARNING"]
    ok_items = [item for item in items if item.status == "OK"]

    if errors:
        status = "blocked"
    elif warnings:
        status = "needs review"
    else:
        status = "ready"

    notes = tuple(f"{item.status} [{item.code}] {item.message}" for item in errors + warnings)
    return ReadinessBrief(status, len(ok_items), len(errors), len(warnings), notes)
