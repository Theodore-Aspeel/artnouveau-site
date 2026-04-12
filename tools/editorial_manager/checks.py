"""Small read-only editorial checks for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .article_access import (
    article_dek,
    article_format,
    article_hero_alt,
    article_hero_image,
    article_meta_description,
    article_model,
    article_publication_order,
    article_sections_count,
    article_slug,
    article_status,
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


@dataclass(frozen=True)
class PublicationCheckItem:
    status: str
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


def publication_check_article(article: Article) -> list[PublicationCheckItem]:
    slug = article_slug(article)
    label = slug or "<missing slug>"
    items: list[PublicationCheckItem] = []

    status = article_status(article)
    if status in {"ready", "published"}:
        items.append(ok("publication-status", label, f"publication status is {status}."))
    elif status == "draft":
        items.append(warn_item("publication-status", label, "article is still marked as draft."))
    elif status == "unknown":
        items.append(warn_item("publication-status", label, "publication status is missing."))
    else:
        items.append(error_item("publication-status", label, f"publication status is not recognized: {status}."))

    if article_title(article, "fr"):
        items.append(ok("title-fr", label, "French title is present."))
    else:
        items.append(error_item("title-fr", label, "French title is missing."))

    if article_dek(article, "fr"):
        items.append(ok("dek-fr", label, "French dek/chapeau is present."))
    else:
        items.append(error_item("dek-fr", label, "French dek/chapeau is missing."))

    if article_meta_description(article, "fr"):
        items.append(ok("meta-description-fr", label, "French meta description is present."))
    else:
        items.append(error_item("meta-description-fr", label, "French meta description is missing."))

    if article_hero_image(article):
        items.append(ok("hero-image", label, "hero image is present."))
    else:
        items.append(error_item("hero-image", label, "hero image is missing."))

    if article_hero_alt(article, "fr"):
        items.append(ok("hero-alt-fr", label, "French hero alt text is present."))
    else:
        items.append(error_item("hero-alt-fr", label, "French hero alt text is missing."))

    if article_format(article) in {"long", "article-complet"}:
        if article_sections_count(article, "fr") > 0:
            items.append(ok("sections-fr", label, "French sections are present for a long article."))
        else:
            items.append(error_item("sections-fr", label, "long article has no French sections."))

    if article_publication_order(article) is not None:
        items.append(ok("publication-order", label, "publication order is present."))
    else:
        items.append(error_item("publication-order", label, "publication order is missing."))

    if has_english_content(article):
        items.append(ok("content-en", label, "English content is present."))
    else:
        items.append(warn_item("content-en", label, "English content is missing or empty."))

    return items


def publication_check_articles(articles: list[Article]) -> list[PublicationCheckItem]:
    items: list[PublicationCheckItem] = []
    for article in articles:
        items.extend(publication_check_article(article))
    return items


def error(code: str, slug: str, message: str) -> CheckIssue:
    return CheckIssue("ERROR", code, slug, message)


def warning(code: str, slug: str, message: str) -> CheckIssue:
    return CheckIssue("WARNING", code, slug, message)


def ok(code: str, slug: str, message: str) -> PublicationCheckItem:
    return PublicationCheckItem("OK", code, slug, message)


def warn_item(code: str, slug: str, message: str) -> PublicationCheckItem:
    return PublicationCheckItem("WARNING", code, slug, message)


def error_item(code: str, slug: str, message: str) -> PublicationCheckItem:
    return PublicationCheckItem("ERROR", code, slug, message)
