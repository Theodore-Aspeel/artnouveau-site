"""Guarded transition from an editorial draft to a published article."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable

from .article_access import article_slug, article_status
from .editor_backups import create_articles_backup
from .editor_images import project_root_from_articles_path
from .editor_store import load_article_payload, run_project_validation, write_payload_atomic
from .locale_report import analyze_article_locale
from .publication_gate import build_publication_gate
from .repository import ARTICLES_JSON


Validator = Callable[[], tuple[bool, list[str]]]


@dataclass(frozen=True)
class PublicationTransitionResult:
    slug: str
    status: str
    status_before: str
    status_after: str
    published_on: str | None
    human_approval: str
    preview_urls: dict[str, str]
    locale_statuses: dict[str, str]
    reasons: tuple[str, ...]
    written: bool = False
    rolled_back: bool = False
    backup: dict[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return self.status in {"ready-for-human-approval", "published"}

    def to_payload(self) -> dict[str, Any]:
        return {
            "contract": {
                "name": "artnouveau.publication_transition",
                "version": 1,
            },
            "slug": self.slug,
            "status": self.status,
            "status_before": self.status_before,
            "status_after": self.status_after,
            "published_on": self.published_on,
            "human_approval": self.human_approval,
            "preview_urls": self.preview_urls,
            "locale_statuses": self.locale_statuses,
            "reasons": list(self.reasons),
            "written": self.written,
            "rolled_back": self.rolled_back,
            "backup": self.backup,
        }


def publish_article(
    slug: str,
    publication_date: str,
    rights_registry: dict[str, Any],
    *,
    path: Path = ARTICLES_JSON,
    write: bool = False,
    approved: bool = False,
    validator: Validator | None = None,
    image_probe=None,
    today: date | None = None,
) -> PublicationTransitionResult:
    payload = load_article_payload(path)
    original_payload = deepcopy(payload)
    articles = payload["articles"]
    article_index = next(
        (index for index, article in enumerate(articles) if isinstance(article, dict) and article_slug(article) == slug),
        None,
    )
    if article_index is None:
        return blocked(slug, "unknown", None, f"Unknown article slug: {slug}.")

    article = articles[article_index]
    status_before = article_status(article)
    if status_before not in {"draft", "ready"}:
        return blocked(
            slug,
            status_before,
            None,
            f"Article status must be draft or ready, not {status_before}.",
        )

    parsed_date, date_error = parse_publication_date(publication_date, today=today)
    if date_error:
        return blocked(slug, status_before, None, date_error)

    proposal = deepcopy(article)
    proposal["status"] = "published"
    publication = proposal.get("publication")
    if not isinstance(publication, dict):
        publication = {}
        proposal["publication"] = publication
    publication["published_on"] = parsed_date.isoformat()

    project_root = project_root_from_articles_path(path)
    gate = build_publication_gate(
        proposal,
        rights_registry,
        project_root=project_root,
        image_probe=image_probe,
    )
    locale_items = {
        locale: analyze_article_locale(proposal, locale)
        for locale in ("en", "nl")
    }
    locale_statuses = {locale: item.status for locale, item in locale_items.items()}
    reasons = list(gate.reasons)
    for locale, item in locale_items.items():
        if item.status != f"{locale}-ready":
            missing = ", ".join(item.missing_fields) or "locale content"
            reasons.append(f"ERROR locale-{locale}: {item.status}; missing {missing}.")

    if gate.status != "ready-for-human-review" or reasons:
        return PublicationTransitionResult(
            slug=slug,
            status="blocked",
            status_before=status_before,
            status_after=status_before,
            published_on=parsed_date.isoformat(),
            human_approval="required",
            preview_urls=gate.preview_urls,
            locale_statuses=locale_statuses,
            reasons=tuple(reasons),
        )

    if not write:
        return PublicationTransitionResult(
            slug=slug,
            status="ready-for-human-approval",
            status_before=status_before,
            status_after="published",
            published_on=parsed_date.isoformat(),
            human_approval="pending",
            preview_urls=gate.preview_urls,
            locale_statuses=locale_statuses,
            reasons=(),
        )

    if not approved:
        return PublicationTransitionResult(
            slug=slug,
            status="blocked",
            status_before=status_before,
            status_after=status_before,
            published_on=parsed_date.isoformat(),
            human_approval="required",
            preview_urls=gate.preview_urls,
            locale_statuses=locale_statuses,
            reasons=("ERROR approval-required: --write also requires explicit --approve.",),
        )

    try:
        backup = create_articles_backup(path, project_root=project_root)
    except Exception as exc:
        return PublicationTransitionResult(
            slug=slug,
            status="blocked",
            status_before=status_before,
            status_after=status_before,
            published_on=parsed_date.isoformat(),
            human_approval="confirmed",
            preview_urls=gate.preview_urls,
            locale_statuses=locale_statuses,
            reasons=(f"ERROR backup-failed: {exc}",),
        )

    articles[article_index] = proposal
    write_payload_atomic(path, payload)
    validate = validator or run_project_validation
    try:
        valid, validation_errors = validate()
    except Exception as exc:
        valid = False
        validation_errors = [f"Project validation could not run: {exc}"]

    if not valid:
        write_payload_atomic(path, original_payload)
        return PublicationTransitionResult(
            slug=slug,
            status="blocked",
            status_before=status_before,
            status_after=status_before,
            published_on=parsed_date.isoformat(),
            human_approval="confirmed",
            preview_urls=gate.preview_urls,
            locale_statuses=locale_statuses,
            reasons=tuple(f"ERROR project-validation: {message}" for message in validation_errors),
            rolled_back=True,
            backup=backup,
        )

    return PublicationTransitionResult(
        slug=slug,
        status="published",
        status_before=status_before,
        status_after="published",
        published_on=parsed_date.isoformat(),
        human_approval="confirmed",
        preview_urls=gate.preview_urls,
        locale_statuses=locale_statuses,
        reasons=(),
        written=True,
        backup=backup,
    )


def parse_publication_date(value: str, *, today: date | None = None) -> tuple[date | None, str | None]:
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError):
        return None, "Publication date must use the valid ISO format YYYY-MM-DD."
    if parsed.isoformat() != value:
        return None, "Publication date must use the valid ISO format YYYY-MM-DD."
    if parsed > (today or date.today()):
        return None, "Publication date cannot be in the future because publication is immediate."
    return parsed, None


def blocked(slug: str, status_before: str, published_on: str | None, reason: str) -> PublicationTransitionResult:
    return PublicationTransitionResult(
        slug=slug,
        status="blocked",
        status_before=status_before,
        status_after=status_before,
        published_on=published_on,
        human_approval="required",
        preview_urls={},
        locale_statuses={},
        reasons=(f"ERROR transition: {reason}",),
    )


def render_publication_transition(result: PublicationTransitionResult) -> str:
    lines = [
        f"Publication transition: {result.slug}",
        f"Status: {result.status}",
        f"Transition: {result.status_before} -> {result.status_after}",
        f"Publication date: {result.published_on or '-'}",
        f"Human approval: {result.human_approval}",
    ]
    if result.preview_urls:
        lines.append("Previews:")
        lines.extend(f"  {locale.upper()}: {url}" for locale, url in result.preview_urls.items())
    if result.locale_statuses:
        lines.append(
            "Locales: " + ", ".join(f"{locale}={status}" for locale, status in result.locale_statuses.items())
        )
    if result.reasons:
        lines.append("Reasons:")
        lines.extend(f"  - {reason}" for reason in result.reasons)
    elif not result.written:
        lines.append("Dry run only: review the previews before rerunning with --write --approve.")
    else:
        lines.append("Article status and publication date were written; project validation passed.")
    return "\n".join(lines)
