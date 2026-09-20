"""Unified read-only status for one article's editorial-to-social pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .article_access import article_slug, article_status
from .checks import publication_check_article
from .locale_report import analyze_article_locale
from .publication_gate import build_publication_gate
from .reel_pilot import DEFAULT_PUBLIC_BASE_URL, build_reel_pilot
from .social_package import build_social_package, social_package_to_dict


Article = dict[str, Any]
PIPELINE_STATUS_CONTRACT_NAME = "artnouveau.pipeline_status"
PIPELINE_STATUS_CONTRACT_VERSION = 1
DONE_STATUSES = {"ready", "completed"}


@dataclass(frozen=True)
class PipelineStage:
    id: str
    label: str
    status: str
    human_approval: str
    evidence: tuple[str, ...]
    next_action: str


def build_pipeline_status(
    article: Article,
    rights_registry: dict[str, Any],
    *,
    project_root: Path,
    locale: str = "fr",
    public_base_url: str = DEFAULT_PUBLIC_BASE_URL,
    image_probe=None,
) -> dict[str, Any]:
    """Aggregate existing checks without changing any project state."""
    slug = article_slug(article)
    checklist = publication_check_article(article)
    content_checks = tuple(
        item for item in checklist
        if item.code not in {"publication-status", "content-en"}
    )
    locale_items = {
        code: analyze_article_locale(article, code)
        for code in ("en", "nl")
    }
    publication_gate = build_publication_gate(
        article,
        rights_registry,
        project_root=project_root,
        image_probe=image_probe,
    )
    social = social_package_to_dict(build_social_package(article, locale))
    reel = build_reel_pilot(article, locale, public_base_url)

    stages = (
        _content_stage(content_checks),
        _localization_stage(locale_items),
        _rights_stage(publication_gate.media_rights),
        _publication_stage(article_status(article), publication_gate),
        _social_stage(article_status(article), social),
        _reel_stage(article_status(article), reel),
        _distribution_stage(),
        _measurement_stage(),
    )
    current = next((stage for stage in stages if stage.status not in DONE_STATUSES), None)
    blocking = any(stage.status == "blocked" for stage in stages)

    return {
        "contract": {
            "name": PIPELINE_STATUS_CONTRACT_NAME,
            "version": PIPELINE_STATUS_CONTRACT_VERSION,
            "kind": "read_only_pipeline_dashboard",
        },
        "slug": slug,
        "article_status": article_status(article),
        "overall_status": "blocked" if blocking else ("complete" if current is None else "in_progress"),
        "current_stage": current.id if current else None,
        "next_action": current.next_action if current else "No pending pipeline action.",
        "human_action_required": bool(current and current.human_approval == "required"),
        "stages": [asdict(stage) | {"evidence": list(stage.evidence)} for stage in stages],
        "review_links": publication_gate.preview_urls,
        "contracts": {
            "publication_gate": "artnouveau.publication_gate@1",
            "social_package": "artnouveau.social_package@1",
            "reel_pilot": "artnouveau.reel_pilot@1",
        },
        "read_only": True,
    }


def render_pipeline_status(payload: dict[str, Any]) -> str:
    lines = [
        f"Pipeline status: {payload['slug']}",
        f"Article status: {payload['article_status']}",
        f"Overall: {payload['overall_status']}",
        f"Current stage: {payload['current_stage'] or '-'}",
        f"Human action required: {'yes' if payload['human_action_required'] else 'no'}",
        f"Next action: {payload['next_action']}",
        "",
        "Stages:",
    ]
    for stage in payload["stages"]:
        lines.append(f"  - {stage['status'].upper()} [{stage['id']}] {stage['label']}")
        for evidence in stage["evidence"]:
            lines.append(f"      {evidence}")
    lines.append("")
    lines.append("Review links:")
    lines.extend(f"  - {locale.upper()}: {url}" for locale, url in payload["review_links"].items())
    return "\n".join(lines)


def _content_stage(checks) -> PipelineStage:
    errors = tuple(f"{item.code}: {item.message}" for item in checks if item.status == "ERROR")
    warnings = tuple(f"{item.code}: {item.message}" for item in checks if item.status == "WARNING")
    if errors:
        return PipelineStage(
            "editorial_qa", "Editorial content and QA", "blocked", "required", errors,
            "Resolve the blocking editorial checks, then rerun pipeline-status.",
        )
    if warnings:
        return PipelineStage(
            "editorial_qa", "Editorial content and QA", "needs_review", "required", warnings,
            "Review the editorial warnings with Christophe Aspel.",
        )
    return PipelineStage(
        "editorial_qa", "Editorial content and QA", "ready", "not_required", ("No blocking content issue.",), "",
    )


def _localization_stage(locale_items: dict[str, Any]) -> PipelineStage:
    incomplete = tuple(
        f"{code.upper()}: {item.status}; missing {', '.join(item.missing_fields) or 'localized content'}"
        for code, item in locale_items.items()
        if item.status != f"{code}-ready"
    )
    if incomplete:
        return PipelineStage(
            "localization", "English and Dutch localization", "needs_review", "required", incomplete,
            "Complete or review the missing EN/NL fields before publication.",
        )
    return PipelineStage(
        "localization", "English and Dutch localization", "ready", "not_required",
        tuple(f"{code.upper()}: {item.status}" for code, item in locale_items.items()), "",
    )


def _rights_stage(rights: dict[str, Any]) -> PipelineStage:
    evidence = tuple(
        f"{issue['severity']} {issue['code']}: {issue['src'] or '-'} - {issue['message']}"
        for issue in rights["issues"]
    ) or (f"{rights['cleared_count']}/{rights['runtime_asset_count']} article images cleared.",)
    if rights["status"] == "blocked":
        return PipelineStage(
            "media_rights", "Media rights and file integrity", "blocked", "required", evidence,
            "Resolve the image-rights or file-integrity errors.",
        )
    if rights["status"] == "needs-review":
        return PipelineStage(
            "media_rights", "Media rights and file integrity", "needs_review", "required", evidence,
            "Review the media-rights warnings.",
        )
    return PipelineStage(
        "media_rights", "Media rights and file integrity", "ready", "not_required", evidence, "",
    )


def _publication_stage(status: str, gate) -> PipelineStage:
    if status == "published":
        return PipelineStage(
            "publication", "Article publication", "completed", "confirmed", ("Article status is published.",), "",
        )
    blockers = tuple(reason for reason in gate.reasons if not reason.startswith("WARNING publication-status:"))
    if gate.status == "blocked":
        return PipelineStage(
            "publication", "Article publication", "blocked", "required", blockers or tuple(gate.reasons),
            "Resolve the publication preflight blockers.",
        )
    if blockers:
        return PipelineStage(
            "publication", "Article publication", "waiting", "required", blockers,
            "Complete the upstream editorial and localization reviews before publication approval.",
        )
    return PipelineStage(
        "publication", "Article publication", "needs_human_approval", "required",
        (f"Article remains {status}.", "Automated content, locale and rights checks are ready."),
        "Christophe reviews the previews; then choose the real publication date and run the guarded publication dry run.",
    )


def _social_stage(status: str, social: dict[str, Any]) -> PipelineStage:
    if status != "published":
        return PipelineStage(
            "social_package", "Social package", "waiting", "required",
            (f"Social queue status: {social['queue_status']}.", "Article publication is still pending."),
            "Complete the article publication gate before final social approval.",
        )
    if social["queue_status"] == "blocked":
        return PipelineStage(
            "social_package", "Social package", "blocked", "required", tuple(social["reasons"]),
            "Resolve the social-package blockers.",
        )
    if social["queue_status"] == "needs-review":
        return PipelineStage(
            "social_package", "Social package", "needs_human_approval", "required", tuple(social["reasons"]),
            "Review and approve the social package before preparing distribution.",
        )
    return PipelineStage(
        "social_package", "Social package", "ready", "required",
        (f"Social queue status: {social['queue_status']}.",), "",
    )


def _reel_stage(status: str, reel: dict[str, Any]) -> PipelineStage:
    if status != "published":
        return PipelineStage(
            "reel_pilot", "Reel pilot", "waiting", "required",
            (f"Reel contract status: {reel['pilot_status']}.",),
            "Keep the storyboard as a draft until the article publication gate is approved.",
        )
    if reel["pilot_status"] == "needs_editorial_input":
        return PipelineStage(
            "reel_pilot", "Reel pilot", "blocked", "required", ("Reel needs editorial or media input.",),
            "Complete the Reel editorial or media inputs.",
        )
    default_hook_id = reel["creative"]["default_hook_id"]
    default_hook = next(
        (hook for hook in reel["creative"]["hook_options"] if hook["id"] == default_hook_id),
        None,
    )
    hook_evidence = default_hook["text"] if default_hook else default_hook_id or "none"
    return PipelineStage(
        "reel_pilot", "Reel pilot", "needs_human_approval", "required",
        (f"Recommended hook: {hook_evidence}", "Storyboard exists; rendered video does not."),
        "Christophe approves the hook and storyboard before the first video render.",
    )


def _distribution_stage() -> PipelineStage:
    return PipelineStage(
        "distribution", "Instagram distribution", "not_started", "required",
        ("No Instagram upload or publication state is stored in the repository.",),
        "After video review, publish manually with explicit human approval and the tracked URL.",
    )


def _measurement_stage() -> PipelineStage:
    return PipelineStage(
        "measurement", "Analytics and learning loop", "waiting", "required",
        ("Measurement starts only after the first approved distribution.",),
        "Record Instagram and UTM results after publication, then compare with the recent account median.",
    )
