"""Read-only social automation package helpers for article entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

from .article_access import (
    article_hero_alt,
    article_hero_image,
    is_mapping,
    locale_content,
    normalize_text,
)
from .locales import DEFAULT_LOCALE, normalize_locale, preview_locale_codes
from .social_brief import SocialBrief, build_social_brief, social_brief_to_dict
from .social_caption import SocialCaption, build_social_caption, social_caption_to_dict
from .social_queue import SocialQueueItem, build_social_queue


Article = dict[str, Any]


@dataclass(frozen=True)
class SocialPackageImage:
    src: str
    alt: str
    caption: str


@dataclass(frozen=True)
class SocialPackageMedia:
    hero: SocialPackageImage
    support: tuple[SocialPackageImage, ...]


@dataclass(frozen=True)
class SocialPackageLinks:
    article_fr_path: str
    article_en_preview_path: str
    preview_paths: dict[str, str]


@dataclass(frozen=True)
class SocialPackage:
    slug: str
    requested_locale: str
    source_locale: str
    brief: SocialBrief
    caption: SocialCaption
    media: SocialPackageMedia
    links: SocialPackageLinks
    queue_item: SocialQueueItem


def build_social_package(article: Article, locale: str = "fr") -> SocialPackage:
    """Build a compact JSON-ready package for later social automation."""
    requested_locale = normalize_locale(locale)
    brief = build_social_brief(article)
    caption = build_social_caption(article, requested_locale)
    queue_item = build_social_queue([article])[0]

    return SocialPackage(
        slug=brief.slug,
        requested_locale=requested_locale,
        source_locale=caption.source_locale,
        brief=brief,
        caption=caption,
        media=_media_package(article, caption.source_locale),
        links=_links_package(brief.slug),
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
        "media": _media_to_dict(package.media),
        "links": _links_to_dict(package.links),
        "image_summary": brief_payload["image_summary"],
        "readiness": brief_payload["readiness"],
        "reasons": list(package.queue_item.reasons),
    }


def _links_to_dict(links: SocialPackageLinks) -> dict[str, Any]:
    return {
        "article_fr_path": links.article_fr_path,
        "article_en_preview_path": links.article_en_preview_path,
        "preview_paths": links.preview_paths,
    }


def _media_to_dict(media: SocialPackageMedia) -> dict[str, Any]:
    return {
        "hero": _image_to_dict(media.hero),
        "support": [_image_to_dict(image) for image in media.support],
    }


def _image_to_dict(image: SocialPackageImage) -> dict[str, str]:
    return {
        "src": image.src,
        "alt": image.alt,
        "caption": image.caption,
    }


def _media_package(article: Article, locale: str) -> SocialPackageMedia:
    localized_media = _localized_media(article, locale)
    media = article.get("media")
    hero = media.get("hero") if is_mapping(media) else None
    support = media.get("support") if is_mapping(media) else None

    return SocialPackageMedia(
        hero=SocialPackageImage(
            src=article_hero_image(article),
            alt=article_hero_alt(article, locale),
            caption=_first_text(
                localized_media.get("hero_caption"),
                hero.get("caption") if is_mapping(hero) else None,
            ),
        ),
        support=tuple(_support_images(support, localized_media)),
    )


def _links_package(slug: str) -> SocialPackageLinks:
    encoded_slug = quote(slug, safe="")
    article_fr_path = f"article.html?slug={encoded_slug}"
    preview_paths = {
        locale: article_fr_path if locale == DEFAULT_LOCALE else f"{article_fr_path}&previewLocale={locale}"
        for locale in preview_locale_codes()
    }

    return SocialPackageLinks(
        article_fr_path=article_fr_path,
        article_en_preview_path=preview_paths.get("en", article_fr_path),
        preview_paths=preview_paths,
    )


def _localized_media(article: Article, locale: str) -> dict[str, Any]:
    content = locale_content(article, locale)
    media = content.get("media") if content else None
    return media if is_mapping(media) else {}


def _support_images(support: Any, localized_media: dict[str, Any]) -> list[SocialPackageImage]:
    if not isinstance(support, list):
        return []

    support_alt = localized_media.get("support_alt")
    support_captions = localized_media.get("support_captions")
    images: list[SocialPackageImage] = []

    for index, item in enumerate(support):
        if not is_mapping(item):
            continue

        src = normalize_text(item.get("src"))
        if not src:
            continue

        images.append(
            SocialPackageImage(
                src=src,
                alt=_first_text(_list_text(support_alt, index), item.get("alt")),
                caption=_first_text(
                    _list_text(support_captions, index),
                    item.get("caption"),
                ),
            )
        )

    return images


def _list_text(values: Any, index: int) -> str:
    if not isinstance(values, list) or index >= len(values):
        return ""
    return normalize_text(values[index])


def _first_text(*values: Any) -> str:
    for value in values:
        text = normalize_text(value)
        if text:
            return text
    return ""
