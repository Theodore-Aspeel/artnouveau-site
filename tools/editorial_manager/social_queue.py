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


@dataclass(frozen=True)
class SocialQueueFilters:
    status: str | None = None
    locale_status: str | None = None
    has_hero: bool | None = None
    limit: int | None = None


def build_social_queue(
    articles: list[Article],
    filters: SocialQueueFilters | None = None,
) -> list[SocialQueueItem]:
    """Build a compact batch view of social publication candidates."""
    sorted_articles = sorted(articles, key=lambda item: article_publication_order(item) or 999_999)
    items = [_queue_item_from_brief(build_social_brief(article)) for article in sorted_articles]
    return filter_social_queue(items, filters)


def build_social_next(
    articles: list[Article],
    filters: SocialQueueFilters | None = None,
) -> SocialQueueItem | None:
    """Return the first matching social queue item in publication order."""
    active_filters = filters or SocialQueueFilters(status="candidate")
    queue_filters = SocialQueueFilters(
        status=active_filters.status,
        locale_status=active_filters.locale_status,
        has_hero=active_filters.has_hero,
        limit=1,
    )
    items = build_social_queue(articles, queue_filters)
    return items[0] if items else None


def filter_social_queue(
    items: list[SocialQueueItem],
    filters: SocialQueueFilters | None,
) -> list[SocialQueueItem]:
    """Apply simple AND filters while preserving the existing queue order."""
    if filters is None:
        return items

    filtered = [
        item
        for item in items
        if _matches_social_queue_filters(item, filters)
    ]

    if filters.limit is not None:
        return filtered[:filters.limit]

    return filtered


def social_queue_to_dict(items: list[SocialQueueItem]) -> dict[str, Any]:
    counts = Counter(item.queue_status for item in items)
    return {
        "summary": {
            "total": len(items),
            "candidate": counts.get("candidate", 0),
            "needs_review": counts.get("needs-review", 0),
            "blocked": counts.get("blocked", 0),
        },
        "items": [_social_queue_item_to_dict(item) for item in items],
    }


def social_next_to_dict(item: SocialQueueItem | None) -> dict[str, Any]:
    return {
        "next": None if item is None else _social_queue_item_to_dict(item),
    }


def _social_queue_item_to_dict(item: SocialQueueItem) -> dict[str, Any]:
    return {
        "slug": item.slug,
        "title_fr": item.title_fr,
        "title_en": item.title_en,
        "locale_status": item.locale_status,
        "readiness": item.readiness,
        "has_hero": item.has_hero,
        "queue_status": item.queue_status,
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


def _matches_social_queue_filters(item: SocialQueueItem, filters: SocialQueueFilters) -> bool:
    if filters.status is not None and item.queue_status != filters.status:
        return False

    if filters.locale_status is not None and item.locale_status != filters.locale_status:
        return False

    if filters.has_hero is not None and item.has_hero != filters.has_hero:
        return False

    return True
