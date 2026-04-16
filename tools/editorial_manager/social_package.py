"""Read-only social automation package helpers for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .social_brief import SocialBrief, build_social_brief, social_brief_to_dict
from .social_caption import SocialCaption, build_social_caption, social_caption_to_dict
from .social_queue import SocialQueueItem, build_social_queue


Article = dict[str, Any]


@dataclass(frozen=True)
class SocialPackage:
    slug: str
    requested_locale: str
    source_locale: str
    brief: SocialBrief
    caption: SocialCaption
    queue_item: SocialQueueItem


def build_social_package(article: Article, locale: str = "fr") -> SocialPackage:
    """Build a compact JSON-ready package for later social automation."""
    brief = build_social_brief(article)
    caption = build_social_caption(article, locale)
    queue_item = build_social_queue([article])[0]

    return SocialPackage(
        slug=brief.slug,
        requested_locale=locale,
        source_locale=caption.source_locale,
        brief=brief,
        caption=caption,
        queue_item=queue_item,
    )


def social_package_to_dict(package: SocialPackage) -> dict[str, Any]:
    """Convert a social package to a stable automation-friendly payload."""
    brief_payload = social_brief_to_dict(package.brief)
    caption_payload = social_caption_to_dict(package.caption)

    return {
        "slug": package.slug,
        "requested_locale": package.requested_locale,
        "source_locale": package.source_locale,
        "locale_status": brief_payload["locale_status"],
        "queue_status": package.queue_item.queue_status,
        "brief": brief_payload,
        "caption": caption_payload,
        "image_summary": brief_payload["image_summary"],
        "readiness": brief_payload["readiness"],
        "reasons": list(package.queue_item.reasons),
    }
