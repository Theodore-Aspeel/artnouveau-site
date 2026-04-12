"""File access for the read-only Editorial Manager CLI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTICLES_JSON = PROJECT_ROOT / "src" / "data" / "articles.json"


def load_articles(path: Path = ARTICLES_JSON) -> list[dict[str, Any]]:
    """Load article entries from the public runtime JSON file."""
    with path.open("r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)

    articles = payload.get("articles")
    if not isinstance(articles, list):
        raise ValueError(f"{path} must contain an articles list.")

    return [article for article in articles if isinstance(article, dict)]


def find_article_by_slug(articles: list[dict[str, Any]], slug: str) -> dict[str, Any] | None:
    for article in articles:
        if article.get("slug") == slug:
            return article
    return None
