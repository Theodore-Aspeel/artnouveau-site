"""Small guarded article creation helper for v2 draft articles."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata
from typing import Any, Callable

from .editor_images import is_valid_editor_image_src, project_root_from_articles_path
from .repository import ARTICLES_JSON, PROJECT_ROOT


Article = dict[str, Any]
Payload = dict[str, Any]

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORMAT_VALUES = ("long", "short")
CONTROLLED_STYLE_KEYS = {
    "art_nouveau",
    "art_nouveau_geometric",
    "art_deco",
    "liberty_art_nouveau",
    "vienna_secession",
}
CONTROLLED_TAG_KEYS = {
    "art_nouveau",
    "art_deco",
    "public_building",
    "commerce",
    "facade",
    "habitat",
    "liberty",
    "floral_motif",
    "threshold",
    "vienna_secession",
    "urban_lettering",
}
DEFAULT_TAG_BY_STYLE = {
    "art_nouveau": "art_nouveau",
    "art_nouveau_geometric": "art_nouveau",
    "art_deco": "art_deco",
    "liberty_art_nouveau": "liberty",
    "vienna_secession": "vienna_secession",
}
PRACTICAL_ITEM_KEYS = ("city", "country", "style", "architect", "address", "date", "access")
STYLE_LABELS_FR = {
    "art_nouveau": "Art Nouveau",
    "art_nouveau_geometric": "Art Nouveau géométrique",
    "art_deco": "Art Déco",
    "liberty_art_nouveau": "Liberty / Art Nouveau",
    "vienna_secession": "Sécession viennoise",
}


@dataclass(frozen=True)
class ArticleCreationInput:
    slug: str
    title_fr: str
    dek_fr: str
    epigraph_fr: str
    meta_description_fr: str
    hero_alt_fr: str
    section_heading_fr: str
    section_body_fr: str
    hero_src: str
    city: str
    country: str
    style_key: str
    tag_keys: tuple[str, ...] = ()
    format: str = "long"
    order: int | None = None
    canonical_name: str = ""
    exact_name: str = ""
    address: str = ""
    architect: str = ""
    date: str = ""
    access: str = ""
    author: str = "Antoine Aspeel"


@dataclass(frozen=True)
class ArticleCreationResult:
    ok: bool
    article: Article | None = None
    errors: tuple[str, ...] = ()
    written: bool = False
    rolled_back: bool = False


def create_article(
    creation_input: ArticleCreationInput,
    path: Path = ARTICLES_JSON,
    *,
    write: bool = False,
    validator: Callable[[], tuple[bool, list[str]]] | None = None,
) -> ArticleCreationResult:
    """Build one v2 draft article and optionally append it to articles.json."""
    payload = load_payload(path)
    articles = [article for article in payload.get("articles", []) if isinstance(article, dict)]
    project_root = project_root_from_articles_path(path)
    errors = validate_creation_input(creation_input, articles, project_root)
    if errors:
        return ArticleCreationResult(ok=False, errors=tuple(errors))

    article = build_article(creation_input, next_order(articles) if creation_input.order is None else creation_input.order)

    if not write:
        return ArticleCreationResult(ok=True, article=article)

    original_payload = deepcopy(payload)
    payload["articles"].append(article)
    write_payload_atomic(path, payload)

    validate = validator or run_project_validation
    try:
        ok, validation_errors = validate()
    except Exception as exc:
        ok = False
        validation_errors = [f"Project validation could not run: {exc}"]

    if not ok:
        write_payload_atomic(path, original_payload)
        return ArticleCreationResult(
            ok=False,
            article=article,
            errors=tuple(validation_errors),
            written=False,
            rolled_back=True,
        )

    return ArticleCreationResult(ok=True, article=article, written=True)


def validate_creation_input(
    creation_input: ArticleCreationInput,
    existing_articles: list[Article],
    project_root: Path = PROJECT_ROOT,
) -> list[str]:
    errors: list[str] = []
    slug = clean(creation_input.slug)

    if not slug:
        errors.append("slug is required.")
    elif not SLUG_RE.fullmatch(slug):
        errors.append("slug must use lowercase letters, numbers and single hyphens only.")
    elif any(clean(article.get("slug")) == slug for article in existing_articles):
        errors.append(f"slug already exists: {slug}.")

    required_fields = {
        "title_fr": creation_input.title_fr,
        "dek_fr": creation_input.dek_fr,
        "epigraph_fr": creation_input.epigraph_fr,
        "meta_description_fr": creation_input.meta_description_fr,
        "hero_alt_fr": creation_input.hero_alt_fr,
        "section_heading_fr": creation_input.section_heading_fr,
        "section_body_fr": creation_input.section_body_fr,
        "hero_src": creation_input.hero_src,
        "city": creation_input.city,
        "country": creation_input.country,
        "style_key": creation_input.style_key,
    }
    for name, value in required_fields.items():
        if not clean(value):
            errors.append(f"{name} is required.")

    if clean(creation_input.format) not in FORMAT_VALUES:
        errors.append(f"format must be one of {', '.join(FORMAT_VALUES)}.")

    style_key = clean(creation_input.style_key)
    if style_key and style_key not in CONTROLLED_STYLE_KEYS:
        errors.append(f"style_key must be one of {', '.join(sorted(CONTROLLED_STYLE_KEYS))}.")

    for tag_key in normalized_tag_keys(creation_input):
        if tag_key not in CONTROLLED_TAG_KEYS:
            errors.append(f"tag key must be one of {', '.join(sorted(CONTROLLED_TAG_KEYS))}: {tag_key}.")

    if creation_input.order is not None:
        if creation_input.order < 1:
            errors.append("order must be a positive integer.")
        elif any(article_order(article) == creation_input.order for article in existing_articles):
            errors.append(f"publication order already exists: {creation_input.order}.")

    if clean(creation_input.hero_src) and not is_valid_editor_image_src(creation_input.hero_src, project_root):
        errors.append("hero_src must be an existing image under src/assets/images.")

    return errors


def build_article(creation_input: ArticleCreationInput, order: int) -> Article:
    slug = clean(creation_input.slug)
    style_key = clean(creation_input.style_key)
    tag_keys = normalized_tag_keys(creation_input)
    practical_fr = practical_items_fr(creation_input)

    return {
        "schema_version": 2,
        "id": slug,
        "slug": slug,
        "status": "draft",
        "format": clean(creation_input.format) or "long",
        "publication": {
            "order": order,
            "published_on": None,
            "updated_on": None,
        },
        "identity": {
            "type": "building",
            "canonical_name": clean(creation_input.canonical_name) or clean(creation_input.title_fr),
            "exact_name": clean(creation_input.exact_name) or clean(creation_input.title_fr),
        },
        "taxonomy": {
            "style_key": style_key,
            "tag_keys": tag_keys,
            "place_keys": {
                "city": key_from_text(creation_input.city),
                "country": key_from_text(creation_input.country),
            },
        },
        "facts": {
            "location": {
                "city": clean(creation_input.city),
                "country": clean(creation_input.country),
                "country_code": None,
                "address": clean(creation_input.address) or None,
            },
            "dates": {
                "built": clean(creation_input.date) or None,
            },
            "people": people(creation_input),
            "notes": None,
        },
        "media": {
            "hero": {
                "src": clean(creation_input.hero_src),
                "credit": None,
            },
            "support": [],
        },
        "sources": {
            "quote": None,
        },
        "relations": {
            "around": None,
        },
        "editorial": {
            "author": clean(creation_input.author),
            "image_credit": None,
            "source_note": None,
            "method_note": None,
            "gaps": [],
            "flags": [],
        },
        "content": {
            "fr": {
                "title": clean(creation_input.title_fr),
                "dek": clean(creation_input.dek_fr),
                "epigraph": clean(creation_input.epigraph_fr),
                "sections": [
                    {
                        "heading": clean(creation_input.section_heading_fr),
                        "body": clean(creation_input.section_body_fr),
                    }
                ],
                "seo": {
                    "meta_description": clean(creation_input.meta_description_fr),
                },
                "media": {
                    "hero_alt": clean(creation_input.hero_alt_fr),
                },
                "around": {
                    "note": "",
                },
                "practical_items": practical_fr,
            },
            "en": empty_locale_content(practical_fr),
            "nl": empty_locale_content(practical_fr),
        },
    }


def practical_items_fr(creation_input: ArticleCreationInput) -> list[dict[str, str]]:
    values = {
        "city": creation_input.city,
        "country": creation_input.country,
        "style": STYLE_LABELS_FR.get(clean(creation_input.style_key), clean(creation_input.style_key)),
        "architect": creation_input.architect,
        "address": creation_input.address,
        "date": creation_input.date,
        "access": creation_input.access,
    }
    return [
        {"key": key, "value": clean(value)}
        for key, value in values.items()
        if key in PRACTICAL_ITEM_KEYS and clean(value)
    ]


def empty_locale_content(practical_fr: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "title": "",
        "dek": "",
        "epigraph": "",
        "sections": [
            {
                "heading": "",
                "body": "",
            }
        ],
        "seo": {
            "meta_description": "",
        },
        "media": {
            "hero_alt": "",
        },
        "around": {
            "note": "",
        },
        "practical_items": [{"key": item["key"], "value": ""} for item in practical_fr],
    }


def people(creation_input: ArticleCreationInput) -> list[dict[str, str]]:
    architect = clean(creation_input.architect)
    if not architect:
        return []
    return [{"role": "architect", "name": architect}]


def normalized_tag_keys(creation_input: ArticleCreationInput) -> list[str]:
    keys = [clean(key) for key in creation_input.tag_keys if clean(key)]
    default_tag = DEFAULT_TAG_BY_STYLE.get(clean(creation_input.style_key))
    if default_tag and default_tag not in keys:
        keys.insert(0, default_tag)
    return list(dict.fromkeys(keys))


def next_order(articles: list[Article]) -> int:
    orders = [article_order(article) or 0 for article in articles]
    return max(orders, default=0) + 1


def article_order(article: Article) -> int | None:
    publication = article.get("publication")
    if isinstance(publication, dict) and isinstance(publication.get("order"), int):
        return publication["order"]
    legacy_order = article.get("publication_order_recommended")
    return legacy_order if isinstance(legacy_order, int) else None


def clean(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def key_from_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", clean(value)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", normalized.lower()).strip("_")


def load_payload(path: Path) -> Payload:
    with path.open("r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("articles"), list):
        raise ValueError(f"{path} must contain an articles list.")
    return payload


def write_payload_atomic(path: Path, payload: Payload) -> None:
    data = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as file_handle:
        temp_path = Path(file_handle.name)
        file_handle.write(data)

    temp_path.replace(path)


def run_project_validation() -> tuple[bool, list[str]]:
    completed = subprocess.run(
        [npm_executable(), "run", "validate"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return True, []

    messages = [completed.stdout.strip(), completed.stderr.strip()]
    return False, [message for message in messages if message]


def npm_executable() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"
