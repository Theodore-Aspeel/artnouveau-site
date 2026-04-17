"""Editable field contract for the local article editor.

The browser UI is deliberately thin. This module is the source of truth for
which article fields can be edited by non-technical users.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


Article = dict[str, Any]

STATUS_VALUES = ("draft", "ready", "published")


@dataclass(frozen=True)
class EditableField:
    path: str
    label: str
    control: str
    required: bool = False
    choices: tuple[str, ...] = ()


EDITABLE_FIELDS: tuple[EditableField, ...] = (
    EditableField("status", "Statut de publication", "select", required=True, choices=STATUS_VALUES),
    EditableField("content.fr.title", "Titre français", "text", required=True),
    EditableField("content.en.title", "Titre anglais", "text"),
    EditableField("content.fr.dek", "Chapeau français", "textarea", required=True),
    EditableField("content.en.dek", "Chapeau anglais", "textarea"),
    EditableField("content.fr.epigraph", "Épigraphe française", "textarea", required=True),
    EditableField("content.en.epigraph", "Épigraphe anglaise", "textarea"),
    EditableField("content.fr.seo.meta_description", "Description SEO française", "textarea", required=True),
    EditableField("content.en.seo.meta_description", "Description SEO anglaise", "textarea"),
    EditableField("content.fr.media.hero_alt", "Texte alternatif français de l'image principale", "textarea", required=True),
    EditableField("content.en.media.hero_alt", "Texte alternatif anglais de l'image principale", "textarea"),
    EditableField("content.fr.around.note", "Note française de l'article lié", "textarea"),
    EditableField("content.en.around.note", "Note anglaise de l'article lié", "textarea"),
)

EDITABLE_FIELD_BY_PATH = {field.path: field for field in EDITABLE_FIELDS}


def editable_field_payload() -> list[dict[str, Any]]:
    return [
        {
            "path": field.path,
            "label": field.label,
            "control": field.control,
            "required": field.required,
            "choices": list(field.choices),
        }
        for field in EDITABLE_FIELDS
    ]


def get_path(article: Article, path: str) -> Any:
    current: Any = article
    for part in path.split("."):
        if not isinstance(current, dict):
            return ""
        current = current.get(part)
    return current


def set_path(article: Article, path: str, value: Any) -> None:
    parts = path.split(".")
    current: Any = article
    for part in parts[:-1]:
        child = current.get(part)
        if not isinstance(child, dict):
            child = {}
            current[part] = child
        current = child
    current[parts[-1]] = value
