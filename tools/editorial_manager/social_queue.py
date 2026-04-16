"""Read-only batch queue helpers for social publication candidates."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .article_access import article_publication_order
from .social_brief import SocialBrief, build_social_brief


Article = dict[str, Any]


@dataclass(frozen=True)
class SocialQueueItem:
    slug: str
    title_fr: str
    title_en: str
    locale_status: str
    readiness: str
    has_hero: bool
    queue_status: str


def build_social_queue(articles: list[Article]) -> list[SocialQueueItem]:
    """Build a compact batch view of social publication candidates."""
    sorted_articles = sorted(articles, key=lambda item: article_publication_order(item) or 999_999)
    return [_queue_item_from_brief(build_social_brief(article)) for article in sorted_articles]


def social_queue_to_dict(items: list[SocialQueueItem]) -> dict[str, Any]:
    counts = Counter(item.queue_status for item in items)
    return {
        "summary": {
            "total": len(items),
            "candidate": counts.get("candidate", 0),
            "needs_review": counts.get("needs-review", 0),
            "blocked": counts.get("blocked", 0),
        },
        "items": [
            {
                "slug": item.slug,
                "title_fr": item.title_fr,
                "title_en": item.title_en,
                "locale_status": item.locale_status,
                "readiness": item.readiness,
                "has_hero": item.has_hero,
                "queue_status": item.queue_status,
            }
            for item in items
        ],
    }


def _queue_item_from_brief(brief: SocialBrief) -> SocialQueueItem:
    return SocialQueueItem(
        slug=brief.slug,
        title_fr=brief.title_fr,
        title_en=brief.title_en,
        locale_status=brief.locale_status.status,
        readiness=brief.readiness.status,
        has_hero=brief.images.has_hero,
        queue_status=_queue_status(brief),
    )


def _queue_status(brief: SocialBrief) -> str:
    if brief.readiness.error_count > 0 or not brief.images.has_hero:
        return "blocked"

    if brief.readiness.warning_count > 0 or brief.locale_status.status != "en-ready":
        return "needs-review"

    return "candidate"
