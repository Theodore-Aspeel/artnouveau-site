"""Read-only social caption proposal helpers for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import re
import unicodedata

from .article_access import article_taxonomy
from .social_brief import SocialBrief, build_social_brief


Article = dict[str, Any]


@dataclass(frozen=True)
class SocialCaption:
    slug: str
    requested_locale: str
    source_locale: str
    locale_status: str
    title: str
    hook: str
    caption: str
    cta: str
    hashtags: tuple[str, ...]


def build_social_caption(article: Article, locale: str = "fr") -> SocialCaption:
    """Build a deterministic, human-editable caption proposal for one article."""
    brief = build_social_brief(article)
    source_locale = _caption_source_locale(brief, locale)
    title = _localized_value(brief, source_locale, "title")
    dek = _localized_value(brief, source_locale, "dek")

    return SocialCaption(
        slug=brief.slug,
        requested_locale=locale,
        source_locale=source_locale,
        locale_status=brief.locale_status.status,
        title=title,
        hook=_build_hook(title, source_locale),
        caption=_build_caption(title, dek),
        cta=_build_cta(source_locale),
        hashtags=tuple(_hashtags(article, brief)),
    )


def social_caption_to_dict(caption: SocialCaption) -> dict[str, Any]:
    """Convert a caption proposal to a small automation-friendly payload."""
    return {
        "slug": caption.slug,
        "requested_locale": caption.requested_locale,
        "source_locale": caption.source_locale,
        "locale_status": caption.locale_status,
        "title": caption.title,
        "hook": caption.hook,
        "caption": caption.caption,
        "cta": caption.cta,
        "hashtags": list(caption.hashtags),
    }


def _caption_source_locale(brief: SocialBrief, requested_locale: str) -> str:
    if requested_locale == "en" and (brief.title_en or brief.dek_en):
        return "en"
    return "fr"


def _localized_value(brief: SocialBrief, locale: str, field: str) -> str:
    if field == "title":
        return brief.title_en if locale == "en" else brief.title_fr
    if field == "dek":
        return brief.dek_en if locale == "en" else brief.dek_fr
    return ""


def _build_hook(title: str, locale: str) -> str:
    if not title:
        return ""
    prefix = "À découvrir" if locale == "fr" else "Look closer"
    return f"{prefix}: {title}"


def _build_caption(title: str, dek: str) -> str:
    if dek:
        return _short_text(dek, 220)
    return _short_text(title, 220)


def _build_cta(locale: str) -> str:
    if locale == "en":
        return "Read the article on the site."
    return "Lire l'article sur le site."


def _short_text(value: str, max_length: int) -> str:
    if len(value) <= max_length:
        return value

    shortened = value[: max_length - 3].rstrip()
    if " " in shortened:
        shortened = shortened.rsplit(" ", 1)[0]
    return f"{shortened}..."


def _hashtags(article: Article, brief: SocialBrief) -> list[str]:
    values = _practical_values(brief)
    taxonomy = article_taxonomy(article)
    candidates = [
        values.get("style") or taxonomy["style"],
        values.get("city") or taxonomy["city"],
        values.get("country") or taxonomy["country"],
        "architecture",
        "patrimoine",
    ]

    hashtags: list[str] = []
    for candidate in candidates:
        tag = _hashtag(candidate)
        if tag and tag not in hashtags:
            hashtags.append(tag)
    return hashtags


def _practical_values(brief: SocialBrief) -> dict[str, str]:
    return {item.key: item.value for item in brief.practical_items}


def _hashtag(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[A-Za-z0-9]+", ascii_value)
    if not words:
        return ""
    return "#" + "".join(word[:1].upper() + word[1:] for word in words)
