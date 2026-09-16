"""Corpus-level publication migration plan.

The current site deliberately exposes every runtime article, including drafts.
This module compares that legacy behaviour with the future published-only
policy without changing the corpus or the build.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from .article_access import article_slug, article_status, article_title
from .publication_gate import build_publication_gate


@dataclass(frozen=True)
class PublicationPlanItem:
    slug: str
    title: str
    publication_status: str
    published_on: str | None
    current_visibility: str
    strict_visibility: str
    transition: str
    automated_gate: str
    human_approval: str
    reasons: tuple[str, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "title": self.title,
            "publication_status": self.publication_status,
            "published_on": self.published_on,
            "current_visibility": self.current_visibility,
            "strict_visibility": self.strict_visibility,
            "transition": self.transition,
            "automated_gate": self.automated_gate,
            "human_approval": self.human_approval,
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class PublicationPlanReport:
    activation_status: str
    human_approval: str
    reasons: tuple[str, ...]
    items: tuple[PublicationPlanItem, ...]

    @property
    def summary(self) -> dict[str, int]:
        return {
            "total_articles": len(self.items),
            "current_visible": sum(item.current_visibility == "visible" for item in self.items),
            "strict_visible": sum(item.strict_visibility == "visible" for item in self.items),
            "would_hide": sum(item.transition == "would-hide" for item in self.items),
            "published": sum(item.publication_status == "published" for item in self.items),
            "draft": sum(item.publication_status == "draft" for item in self.items),
        }

    def to_payload(self) -> dict[str, Any]:
        return {
            "contract": {
                "name": "artnouveau.publication_plan",
                "version": 1,
            },
            "current_policy": "legacy-visible",
            "candidate_policy": "published-only",
            "activation_status": self.activation_status,
            "human_approval": self.human_approval,
            "read_only": True,
            "summary": self.summary,
            "reasons": list(self.reasons),
            "items": [item.to_payload() for item in self.items],
        }


def _published_on(article: dict[str, Any]) -> str | None:
    publication = article.get("publication")
    value = publication.get("published_on") if isinstance(publication, dict) else None
    return value.strip() if isinstance(value, str) and value.strip() else None


def _valid_iso_date(value: str | None) -> bool:
    if value is None:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def build_publication_plan(
    articles: list[dict[str, Any]],
    rights_registry: dict[str, Any],
    *,
    project_root,
    image_probe=None,
) -> PublicationPlanReport:
    items: list[PublicationPlanItem] = []

    for article in articles:
        status = article_status(article)
        published_on = _published_on(article)
        gate = build_publication_gate(
            article,
            rights_registry,
            project_root=project_root,
            image_probe=image_probe,
        )
        strict_visible = status == "published"
        reasons = list(gate.reasons)
        if strict_visible and not _valid_iso_date(published_on):
            reasons.append("ERROR published-on: published article needs a valid ISO publication date.")

        items.append(
            PublicationPlanItem(
                slug=article_slug(article),
                title=article_title(article, "fr"),
                publication_status=status,
                published_on=published_on,
                current_visibility="visible",
                strict_visibility="visible" if strict_visible else "hidden",
                transition="unchanged" if strict_visible else "would-hide",
                automated_gate=gate.status,
                human_approval="required",
                reasons=tuple(reasons),
            )
        )

    would_hide = [item for item in items if item.transition == "would-hide"]
    invalid_published = [
        item
        for item in items
        if item.publication_status == "published"
        and (item.automated_gate != "ready-for-human-review" or not _valid_iso_date(item.published_on))
    ]

    reasons: list[str] = []
    if would_hide:
        reasons.append(
            f"Published-only mode would hide {len(would_hide)} currently visible article(s)."
        )
    if invalid_published:
        reasons.append(
            f"{len(invalid_published)} published article(s) do not pass the automated gate and date check."
        )

    if would_hide or invalid_published:
        activation_status = "blocked"
    else:
        activation_status = "ready-for-human-activation"

    return PublicationPlanReport(
        activation_status=activation_status,
        human_approval="required",
        reasons=tuple(reasons),
        items=tuple(items),
    )


def render_publication_plan(report: PublicationPlanReport) -> str:
    summary = report.summary
    lines = [
        "Publication plan",
        "Current policy: legacy-visible",
        "Candidate policy: published-only",
        f"Activation status: {report.activation_status}",
        "Human approval: required",
        (
            "Visibility: "
            f"{summary['current_visible']} current -> {summary['strict_visible']} strict "
            f"({summary['would_hide']} would hide)"
        ),
    ]
    if report.reasons:
        lines.append("Activation blockers:")
        lines.extend(f"  - {reason}" for reason in report.reasons)
    lines.append("Articles:")
    for item in report.items:
        lines.append(
            f"  - {item.slug}: {item.publication_status}, "
            f"{item.current_visibility} -> {item.strict_visibility}, gate={item.automated_gate}"
        )
    return "\n".join(lines)
