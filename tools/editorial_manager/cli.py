"""Command line interface for the read-only Editorial Manager."""

from __future__ import annotations

import argparse

from .checks import check_article, check_articles, publication_check_article, publication_check_articles
from .locale_report import analyze_article_locale, analyze_articles_locale
from .repository import find_article_by_slug, load_articles
from .reporting import (
    render_article_detail,
    render_article_list,
    render_check_report,
    render_locale_report,
    render_publication_check_report,
    render_social_brief,
    render_social_brief_json,
    render_social_queue,
    render_social_queue_json,
    render_summary,
)
from .social_brief import build_social_brief
from .social_queue import build_social_queue


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.editorial_manager",
        description="Read-only editorial explorer for the article dataset.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("summary", help="Show a global article summary.")
    subparsers.add_parser("list", help="List articles in publication order.")

    show_parser = subparsers.add_parser("show", help="Show a simple article card.")
    show_parser.add_argument("slug", help="Article slug to inspect.")

    check_parser = subparsers.add_parser("check", help="Run simple read-only editorial checks.")
    check_parser.add_argument("slug", nargs="?", help="Optional article slug to check.")

    publication_check_parser = subparsers.add_parser(
        "publication-check",
        help="Run a read-only publication preparation checklist.",
    )
    publication_check_parser.add_argument("slug", nargs="?", help="Optional article slug to check.")

    locale_report_parser = subparsers.add_parser(
        "locale-report",
        help="Show the read-only FR/EN content status.",
    )
    locale_report_parser.add_argument("slug", nargs="?", help="Optional article slug to inspect.")

    social_brief_parser = subparsers.add_parser(
        "social-brief",
        help="Prepare a read-only social publication brief for one article.",
    )
    social_brief_parser.add_argument("slug", help="Article slug to prepare.")
    social_brief_parser.add_argument(
        "--json",
        action="store_true",
        help="Output the social brief as a simple structured JSON payload.",
    )

    social_queue_parser = subparsers.add_parser(
        "social-queue",
        help="Show a read-only batch queue of social publication candidates.",
    )
    social_queue_parser.add_argument(
        "--json",
        action="store_true",
        help="Output the social queue as a simple structured JSON payload.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    articles = load_articles()

    if args.command == "summary":
        print(render_summary(articles))
        return 0

    if args.command == "list":
        print(render_article_list(articles))
        return 0

    if args.command == "show":
        article = find_article_by_slug(articles, args.slug)
        if article is None:
            parser.error(f"unknown article slug: {args.slug}")
        print(render_article_detail(article))
        return 0

    if args.command == "check":
        if args.slug:
            article = find_article_by_slug(articles, args.slug)
            if article is None:
                parser.error(f"unknown article slug: {args.slug}")
            issues = check_article(article)
            print(render_check_report(issues, 1))
        else:
            issues = check_articles(articles)
            print(render_check_report(issues, len(articles)))
        return 1 if any(issue.severity == "ERROR" for issue in issues) else 0

    if args.command == "publication-check":
        if args.slug:
            article = find_article_by_slug(articles, args.slug)
            if article is None:
                parser.error(f"unknown article slug: {args.slug}")
            items = publication_check_article(article)
            print(render_publication_check_report(items, 1))
        else:
            items = publication_check_articles(articles)
            print(render_publication_check_report(items, len(articles)))
        return 1 if any(item.status == "ERROR" for item in items) else 0

    if args.command == "locale-report":
        if args.slug:
            article = find_article_by_slug(articles, args.slug)
            if article is None:
                parser.error(f"unknown article slug: {args.slug}")
            items = [analyze_article_locale(article)]
        else:
            items = analyze_articles_locale(articles)
        print(render_locale_report(items))
        return 0

    if args.command == "social-brief":
        article = find_article_by_slug(articles, args.slug)
        if article is None:
            parser.error(f"unknown article slug: {args.slug}")
        brief = build_social_brief(article)
        if args.json:
            print(render_social_brief_json(brief))
        else:
            print(render_social_brief(brief))
        return 0

    if args.command == "social-queue":
        items = build_social_queue(articles)
        if args.json:
            print(render_social_queue_json(items))
        else:
            print(render_social_queue(items))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
