"""Small local workflow helper built from existing social primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .article_access import article_slug
from .social_package import SocialPackage, build_social_package
from .social_queue import SocialQueueFilters, SocialQueueItem, build_social_next


Article = dict[str, Any]


@dataclass(frozen=True)
class SocialWorkflow:
    selected: SocialQueueItem
    package: SocialPackage


def build_social_workflow(
    articles: list[Article],
    locale: str = "fr",
    filters: SocialQueueFilters | None = None,
) -> SocialWorkflow | None:
    """Select the next article and build its social package for local review."""
    selected = build_social_next(articles, filters)
    if selected is None:
        return None

    article = _find_article(articles, selected.slug)
    if article is None:
        return None

    return SocialWorkflow(
        selected=selected,
        package=build_social_package(article, locale),
    )


def _find_article(articles: list[Article], slug: str) -> Article | None:
    for article in articles:
        if article_slug(article) == slug:
            return article
    return None
