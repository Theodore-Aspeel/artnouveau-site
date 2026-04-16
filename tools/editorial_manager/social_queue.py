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
    reasons: tuple[str, ...] = ()


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
        "reasons": list(item.reasons),
    }


def _queue_item_from_brief(brief: SocialBrief) -> SocialQueueItem:
    queue_status = _queue_status(brief)
    return SocialQueueItem(
        slug=brief.slug,
        title_fr=brief.title_fr,
        title_en=brief.title_en,
        locale_status=brief.locale_status.status,
        readiness=brief.readiness.status,
        has_hero=brief.images.has_hero,
        queue_status=queue_status,
        reasons=_queue_reasons(brief, queue_status),
    )


def _queue_status(brief: SocialBrief) -> str:
    if brief.readiness.error_count > 0 or not brief.images.has_hero:
        return "blocked"

    if brief.readiness.warning_count > 0 or brief.locale_status.status != "en-ready":
        return "needs-review"

    return "candidate"


def _queue_reasons(brief: SocialBrief, queue_status: str) -> tuple[str, ...]:
    if queue_status == "candidate":
        return (
            "Publication checklist is ready.",
            "English content is ready.",
            "Hero image is present.",
        )

    if queue_status == "blocked":
        reasons = []
        if brief.readiness.error_count > 0:
            reasons.append(f"Publication checklist has {brief.readiness.error_count} error(s).")
            reasons.extend(_readiness_notes(brief, "ERROR"))
        if not brief.images.has_hero:
            reasons.append("Hero image is missing.")
        return tuple(_dedupe(reasons))

    reasons = []
    if brief.readiness.warning_count > 0:
        reasons.append(f"Publication checklist has {brief.readiness.warning_count} warning(s).")
        reasons.extend(_readiness_notes(brief, "WARNING"))
    if brief.locale_status.status == "fr-only":
        reasons.append("English content is missing.")
    elif brief.locale_status.status == "en-partial":
        missing = ", ".join(brief.locale_status.missing_fields)
        reasons.append(f"English content is incomplete: {missing}.")
    return tuple(_dedupe(reasons))


def _readiness_notes(brief: SocialBrief, status: str) -> list[str]:
    prefix = f"{status} "
    return [note for note in brief.readiness.notes if note.startswith(prefix)]


def _dedupe(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _matches_social_queue_filters(item: SocialQueueItem, filters: SocialQueueFilters) -> bool:
    if filters.status is not None and item.queue_status != filters.status:
        return False

    if filters.locale_status is not None and item.locale_status != filters.locale_status:
        return False

    if filters.has_hero is not None and item.has_hero != filters.has_hero:
        return False

    return True
