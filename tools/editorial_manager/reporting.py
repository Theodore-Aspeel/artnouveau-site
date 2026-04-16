"""Terminal reporting for the read-only Editorial Manager CLI."""

from __future__ import annotations

from collections import Counter
import json
from typing import Any

from .article_access import (
    article_dek,
    article_format,
    article_model,
    article_publication_order,
    article_sections_count,
    article_slug,
    article_status,
    article_taxonomy,
    article_title,
    has_english_content,
)
from .checks import CheckIssue, PublicationCheckItem
from .locale_report import LocaleReportItem
from .social_brief import SocialBrief, social_brief_to_dict


Article = dict[str, Any]


def render_summary(articles: list[Article]) -> str:
    models = Counter(article_model(article) for article in articles)
    statuses = Counter(article_status(article) for article in articles)
    v2_articles = [article for article in articles if article_model(article) == "v2"]
    v2_without_en = sum(1 for article in v2_articles if not has_english_content(article))

    lines = [
        "Editorial Manager summary",
        f"Total articles: {len(articles)}",
        f"v1 articles: {models.get('v1', 0)}",
        f"v2 articles: {models.get('v2', 0)}",
        f"v2 without English content: {v2_without_en}",
    ]

    if statuses:
        lines.append("Statuses:")
        for status, count in sorted(statuses.items()):
            lines.append(f"  - {status}: {count}")

    return "\n".join(lines)


def render_article_list(articles: list[Article]) -> str:
    rows = []
    for article in sorted(articles, key=lambda item: article_publication_order(item) or 999_999):
        taxonomy = article_taxonomy(article)
        rows.append(
            [
                str(article_publication_order(article) or "-"),
                article_model(article),
                article_status(article),
                article_slug(article),
                article_title(article),
                taxonomy["city"],
                taxonomy["style"],
            ]
        )

    return render_table(
        ["Order", "Model", "Status", "Slug", "Title", "City", "Style"],
        rows,
    )


def render_article_detail(article: Article) -> str:
    taxonomy = article_taxonomy(article)
    lines = [
        f"Article: {article_slug(article)}",
        f"Model: {article_model(article)}",
        f"Status: {article_status(article)}",
        f"Format: {article_format(article)}",
        f"Publication order: {article_publication_order(article) or '-'}",
        f"Title: {article_title(article)}",
        f"Dek: {article_dek(article)}",
        f"City: {taxonomy['city']}",
        f"Country: {taxonomy['country']}",
        f"Style: {taxonomy['style']}",
        f"Sections: {article_sections_count(article)}",
        f"English content: {'yes' if has_english_content(article) else 'no'}",
    ]
    return "\n".join(lines)


def render_check_report(issues: list[CheckIssue], checked_count: int) -> str:
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    warnings = [issue for issue in issues if issue.severity == "WARNING"]

    lines = [
        "Editorial check",
        f"Articles checked: {checked_count}",
        f"Errors: {len(errors)}",
        f"Warnings: {len(warnings)}",
    ]

    if not issues:
        lines.append("No issues found.")
        return "\n".join(lines)

    if errors:
        lines.append("")
        lines.append("Errors:")
        lines.extend(render_issue_lines(errors))

    if warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(render_issue_lines(warnings))

    return "\n".join(lines)


def render_publication_check_report(items: list[PublicationCheckItem], checked_count: int) -> str:
    errors = [item for item in items if item.status == "ERROR"]
    warnings = [item for item in items if item.status == "WARNING"]
    ok_items = [item for item in items if item.status == "OK"]

    lines = [
        "Publication checklist",
        f"Articles checked: {checked_count}",
        f"OK: {len(ok_items)}",
        f"Errors: {len(errors)}",
        f"Warnings: {len(warnings)}",
    ]

    if not items:
        lines.append("No publication checks were run.")
        return "\n".join(lines)

    current_slug = None
    for item in items:
        if item.slug != current_slug:
            current_slug = item.slug
            lines.append("")
            lines.append(f"Article: {item.slug}")
        lines.append(f"  - {item.status} [{item.code}] {item.message}")

    return "\n".join(lines)


def render_locale_report(items: list[LocaleReportItem]) -> str:
    counts = Counter(item.status for item in items)
    rows = [
        [
            item.status,
            item.slug,
            ", ".join(item.missing_fields) if item.missing_fields else "-",
        ]
        for item in items
    ]

    lines = [
        "Locale report",
        f"Articles checked: {len(items)}",
        f"fr-only: {counts.get('fr-only', 0)}",
        f"en-partial: {counts.get('en-partial', 0)}",
        f"en-ready: {counts.get('en-ready', 0)}",
    ]

    if rows:
        lines.append("")
        lines.append(render_table(["Status", "Slug", "Missing EN fields"], rows))
    else:
        lines.append("No articles found.")

    return "\n".join(lines)


def render_social_brief(brief: SocialBrief) -> str:
    lines = [
        "Social publication brief",
        f"Slug: {brief.slug}",
        f"Locale status: {brief.locale_status.status}",
        f"Title FR: {brief.title_fr or '-'}",
        f"Title EN: {brief.title_en or '-'}",
        "",
        "Dek:",
        f"  FR: {brief.dek_fr or '-'}",
        f"  EN: {brief.dek_en or '-'}",
    ]

    if brief.quote is not None:
        lines.extend([
            "",
            "Quote:",
            f"  FR: {brief.quote.text_fr or '-'}",
            f"  EN: {brief.quote.text_en or '-'}",
            f"  Author: {brief.quote.author or '-'}",
            f"  Attribution FR: {brief.quote.attribution_fr or '-'}",
            f"  Attribution EN: {brief.quote.attribution_en or '-'}",
        ])

    lines.append("")
    lines.append("Practical items:")
    if brief.practical_items:
        for item in brief.practical_items:
            lines.append(f"  - {item.key}: {item.value}")
    else:
        lines.append("  - none")

    lines.extend([
        "",
        "Images:",
        f"  - hero: {'yes' if brief.images.has_hero else 'no'}",
        f"  - hero src: {brief.images.hero_src or '-'}",
        f"  - support images: {brief.images.support_count}",
        "",
        "Readiness:",
        f"  - status: {brief.readiness.status}",
        f"  - publication checklist: {brief.readiness.ok_count} OK, "
        f"{brief.readiness.error_count} errors, {brief.readiness.warning_count} warnings",
    ])

    if brief.readiness.notes:
        lines.append("  - notes:")
        for note in brief.readiness.notes:
            lines.append(f"    - {note}")

    return "\n".join(lines)


def render_social_brief_json(brief: SocialBrief) -> str:
    return json.dumps(social_brief_to_dict(brief), ensure_ascii=False, indent=2)


def render_issue_lines(issues: list[CheckIssue]) -> list[str]:
    return [f"  - [{issue.code}] {issue.slug}: {issue.message}" for issue in issues]


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def render_row(values: list[str]) -> str:
        return "  ".join(value.ljust(widths[index]) for index, value in enumerate(values)).rstrip()

    output = [
        render_row(headers),
        render_row(["-" * width for width in widths]),
    ]
    output.extend(render_row(row) for row in rows)
    return "\n".join(output)
