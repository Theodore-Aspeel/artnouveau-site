"""Deterministic read-only handoff for the first ANAD Reel pilot."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode, urlsplit, urlunsplit

from .article_access import is_mapping, locale_content, normalize_text
from .social_package import build_social_package, social_package_to_dict


Article = dict[str, Any]
REEL_PILOT_CONTRACT_NAME = "artnouveau.reel_pilot"
REEL_PILOT_CONTRACT_VERSION = 1
DEFAULT_PUBLIC_BASE_URL = "https://artnouveauetdeco.com"


def build_reel_pilot(
    article: Article,
    locale: str = "fr",
    public_base_url: str = DEFAULT_PUBLIC_BASE_URL,
) -> dict[str, Any]:
    """Build a review-only Reel plan from the existing social package."""
    package = social_package_to_dict(build_social_package(article, locale))
    source_locale = package["source_locale"]
    content = locale_content(article, source_locale)
    hooks = _hook_options(package, content)
    public_paths = package["links"]["public_paths"]
    destination_locale = source_locale if source_locale in public_paths else "fr"
    destination_path = public_paths.get(destination_locale, package["links"]["canonical_public_path"])
    link_plan = _link_plan(
        public_base_url,
        destination_path,
        article_slug=package["slug"],
        locale=source_locale,
        destination_locale=destination_locale,
    )
    status = _pilot_status(package, hooks)

    return {
        "contract": {
            "name": REEL_PILOT_CONTRACT_NAME,
            "version": REEL_PILOT_CONTRACT_VERSION,
            "kind": "read_only_reel_pilot_handoff",
        },
        "slug": package["slug"],
        "requested_locale": package["requested_locale"],
        "source_locale": source_locale,
        "pilot_status": status,
        "upstream": {
            "contract": "artnouveau.social_package@1",
            "queue_status": package["queue_status"],
            "readiness": package["readiness"]["status"],
            "reasons": package["reasons"],
        },
        "format": {
            "platform": "instagram_reel",
            "aspect_ratio": "9:16",
            "width_px": 1080,
            "height_px": 1920,
            "target_duration_seconds": 24,
            "safe_area_review_required": True,
        },
        "creative": {
            "default_hook_id": hooks[0]["id"] if hooks else None,
            "hook_options": hooks,
            "storyboard": _storyboard(package, content, hooks),
            "voiceover_draft": package["caption"]["caption"],
            "caption": package["caption"],
        },
        "media_plan": _media_plan(package),
        "link_plan": link_plan,
        "measurement_plan": {
            "comparison_basis": "recent_account_median",
            "instagram_metrics": [
                "three_second_retention",
                "average_watch_time_seconds",
                "completion_rate",
                "shares",
                "saves",
                "profile_visits",
            ],
            "site_metrics": ["utm_sessions", "engaged_sessions", "article_reads"],
        },
        "human_gates": [
            {"gate": "storyboard", "status": "pending"},
            {"gate": "media_crop_and_order", "status": "pending"},
            {"gate": "rendered_video", "status": "not_started"},
            {"gate": "instagram_publication", "status": "blocked_until_explicit_approval"},
        ],
        "automation_limits": {
            "renders_video": False,
            "uploads_media": False,
            "publishes_to_instagram": False,
            "stores_credentials": False,
            "writes_article_data": False,
        },
    }


def _hook_options(package: dict[str, Any], content: dict[str, Any]) -> list[dict[str, str]]:
    candidates = [
        ("social_hook", package["caption"]["hook"]),
        ("article_epigraph", content.get("epigraph")),
        ("first_section_heading", _section_heading(content, 0)),
    ]
    hooks: list[dict[str, str]] = []
    seen: set[str] = set()
    for source, value in candidates:
        text = normalize_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        hooks.append({"id": f"hook_{len(hooks) + 1}", "source": source, "text": text})
    return hooks


def _storyboard(
    package: dict[str, Any],
    content: dict[str, Any],
    hooks: list[dict[str, str]],
) -> list[dict[str, Any]]:
    hero_src = package["media"]["hero"]["src"]
    hook_text = hooks[0]["text"] if hooks else package["caption"]["title"]
    cards = [
        ("hook", 0, 3, hook_text, "slow_push_in"),
        ("observation", 3, 9, normalize_text(content.get("epigraph")), "vertical_pan"),
        ("reading_key", 9, 15, _section_heading(content, 0), "detail_crop"),
        ("reading_key", 15, 20, _section_heading(content, 1), "slow_pull_out"),
        ("cta", 20, 24, package["caption"]["cta"], "hold"),
    ]
    return [
        {
            "scene": index,
            "role": role,
            "start_second": start,
            "end_second": end,
            "source_image": hero_src,
            "on_screen_text": normalize_text(text),
            "motion_suggestion": motion,
        }
        for index, (role, start, end, text, motion) in enumerate(cards, start=1)
        if normalize_text(text)
    ]


def _media_plan(package: dict[str, Any]) -> dict[str, Any]:
    hero = package["media"]["hero"]
    contextual = [
        {**image, "role": "related_place_context", "use_in_default_storyboard": False}
        for image in package["media"]["support"]
    ]
    return {
        "primary_subject": {**hero, "role": "primary_subject"},
        "default_storyboard_uses_primary_only": True,
        "contextual_images": contextual,
        "editor_note": (
            "Supporting article images show related places. Do not present them as details "
            "of the primary building; include them only after explicit storyboard approval."
        ),
    }


def _link_plan(
    public_base_url: str,
    destination_path: str,
    article_slug: str,
    locale: str,
    destination_locale: str,
) -> dict[str, Any]:
    base = _normalize_public_base_url(public_base_url)
    utm = {
        "utm_source": "instagram",
        "utm_medium": "organic_social",
        "utm_campaign": f"anad_reel_{article_slug}",
        "utm_content": f"{locale}_pilot",
    }
    tracked_url = f"{base}{destination_path}?{urlencode(utm)}"
    return {
        "placement": "profile_link_or_story_sticker",
        "destination_locale": destination_locale,
        "destination_path": destination_path,
        "tracked_url": tracked_url,
        "utm": utm,
    }


def _normalize_public_base_url(value: str) -> str:
    parsed = urlsplit(normalize_text(value))
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("public_base_url must be an absolute http(s) URL without query or fragment")
    path = parsed.path.rstrip("/")
    return urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def _section_heading(content: dict[str, Any], index: int) -> str:
    sections = content.get("sections")
    if not isinstance(sections, list) or index >= len(sections):
        return ""
    section = sections[index]
    return normalize_text(section.get("heading")) if is_mapping(section) else ""


def _pilot_status(package: dict[str, Any], hooks: list[dict[str, str]]) -> str:
    if not package["media"]["hero"]["src"] or len(hooks) < 3:
        return "needs_editorial_input"
    if package["queue_status"] != "candidate":
        return "needs_upstream_review"
    return "ready_for_human_storyboard_review"
