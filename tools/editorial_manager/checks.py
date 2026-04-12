"""Small read-only editorial checks for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .article_access import (
    article_hero_image,
    article_meta_description,
    article_model,
    article_publication_order,
    article_slug,
    article_title,
    has_english_content,
)


Article = dict[str, Any]


@dataclass(frozen=True)
class CheckIssue:
    severity: str
    code: str
    slug: str
    message: str


def check_article(article: Article) -> list[CheckIssue]:
    slug = article_slug(article)
    label = slug or "<missing slug>"
    issues: list[CheckIssue] = []

    if not slug:
        issues.append(error("missing-slug", label, "slug is missing."))

    if not article_title(article, "fr"):
        issues.append(error("missing-title-fr", label, "French title is missing."))

    if not article_hero_image(article):
        issues.append(error("missing-hero-image", label, "hero image is missing."))

    if not article_meta_description(article, "fr"):
        issues.append(error("missing-meta-description-fr", label, "French meta description is missing."))

    if article_model(article) == "v2" and not has_english_content(article):
        issues.append(warning("missing-content-en", label, "content.en is missing or empty."))

    if article_publication_order(article) is None:
        issues.append(warning("missing-publication-order", label, "publication order is missing."))

    return issues


def check_articles(articles: list[Article]) -> list[CheckIssue]:
    issues: list[CheckIssue] = []
    for article in articles:
        issues.extend(check_article(article))
    return issues


def error(code: str, slug: str, message: str) -> CheckIssue:
    return CheckIssue("ERROR", code, slug, message)


def warning(code: str, slug: str, message: str) -> CheckIssue:
    return CheckIssue("WARNING", code, slug, message)
