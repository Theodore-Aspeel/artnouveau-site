"""One deterministic preflight before the final human publication review."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .article_access import article_slug
from .checks import publication_check_article
from .editor_store import build_preview_urls
from .locale_report import analyze_article_locale
from .media_rights import (
    check_media_rights,
    collect_article_assets,
)


@dataclass(frozen=True)
class PublicationGateReport:
    slug: str
    status: str
    human_approval: str
    preview_urls: dict[str, str]
    reasons: tuple[str, ...]
    publication_checks: tuple[dict[str, str], ...]
    locale_status: dict[str, Any]
    media_rights: dict[str, Any]

    @property
    def ok(self) -> bool:
        return self.status == "ready-for-human-review"

    def to_payload(self) -> dict[str, Any]:
        return {
            "contract": {
                "name": "artnouveau.publication_gate",
                "version": 1,
            },
            "slug": self.slug,
            "status": self.status,
            "human_approval": self.human_approval,
            "project_quality_gate": "required-separately",
            "preview_urls": self.preview_urls,
            "reasons": list(self.reasons),
            "publication_checks": list(self.publication_checks),
            "locale_status": self.locale_status,
            "media_rights": self.media_rights,
        }


def build_publication_gate(
    article: dict[str, Any],
    rights_registry: dict[str, Any],
    *,
    project_root,
    image_probe=None,
) -> PublicationGateReport:
    slug = article_slug(article)
    checklist = publication_check_article(article)
    checklist_payload = tuple(asdict(item) for item in checklist)
    locale_item = analyze_article_locale(article, "en")
    locale_payload = {
        "locale": "en",
        "status": locale_item.status,
        "missing_fields": list(locale_item.missing_fields),
    }
    rights = check_media_rights(
        collect_article_assets(article),
        rights_registry,
        project_root=project_root,
        warn_unused=False,
        image_probe=image_probe,
    )

    reasons: list[str] = []
    for item in checklist:
        if item.status != "OK":
            reasons.append(f"{item.status} {item.code}: {item.message}")
    if locale_item.status != "en-ready":
        reasons.append(f"WARNING locale-en: English locale status is {locale_item.status}.")
    for issue in rights.issues:
        reasons.append(f"{issue.severity} {issue.code}: {issue.message}")

    has_error = any(item.status == "ERROR" for item in checklist) or not rights.ok
    has_warning = any(item.status == "WARNING" for item in checklist) or locale_item.status != "en-ready"
    status = "blocked" if has_error else ("needs-review" if has_warning else "ready-for-human-review")
    return PublicationGateReport(
        slug=slug,
        status=status,
        human_approval="required",
        preview_urls=build_preview_urls(slug),
        reasons=tuple(reasons),
        publication_checks=checklist_payload,
        locale_status=locale_payload,
        media_rights=rights.to_payload(),
    )


def render_publication_gate(report: PublicationGateReport) -> str:
    lines = [
        f"Publication gate: {report.slug}",
        f"Automated status: {report.status}",
        "Human approval: required",
        "Previews:",
    ]
    lines.extend(f"  {locale.upper()}: {url}" for locale, url in report.preview_urls.items())
    if report.reasons:
        lines.append("Reasons:")
        lines.extend(f"  - {reason}" for reason in report.reasons)
    else:
        lines.append("Automated checks: all passed")
    return "\n".join(lines)
