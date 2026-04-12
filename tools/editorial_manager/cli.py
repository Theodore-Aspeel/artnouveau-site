"""Command line interface for the read-only Editorial Manager."""

from __future__ import annotations

import argparse

from .checks import check_article, check_articles
from .repository import find_article_by_slug, load_articles
from .reporting import render_article_detail, render_article_list, render_check_report, render_summary


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

    parser.error(f"unknown command: {args.command}")
    return 2
