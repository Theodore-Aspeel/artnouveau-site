"""Editable field contract for the local article editor.

The browser UI is deliberately thin. This module is the source of truth for
which article fields can be edited by non-technical users.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
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
    group: str = "Champs principaux"


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
SECTION_FIELD_RE = re.compile(r"^content\.(fr|en)\.sections\.(0|[1-9]\d*)\.(heading|body)$")
SECTION_LOCALES = (("fr", "FR"), ("en", "EN"))
SECTION_PROPERTIES = (("heading", "titre", "text"), ("body", "texte", "textarea"))


def editable_field_payload() -> list[dict[str, Any]]:
    return [editable_field_to_payload(field) for field in EDITABLE_FIELDS]


def editable_fields_for_article(article: Article) -> list[EditableField]:
    return [*EDITABLE_FIELDS, *section_editable_fields(article)]


def editable_field_for_path(article: Article, path: str) -> EditableField | None:
    field = EDITABLE_FIELD_BY_PATH.get(path)
    if field is not None:
        return field

    match = SECTION_FIELD_RE.match(path)
    if not match:
        return None

    locale, index_text, property_name = match.groups()
    sections = get_path(article, f"content.{locale}.sections")
    index = int(index_text)
    if not isinstance(sections, list) or index >= len(sections) or not isinstance(sections[index], dict):
        return None

    locale_label = "FR" if locale == "fr" else "EN"
    property_label = "titre" if property_name == "heading" else "texte"
    control = "text" if property_name == "heading" else "textarea"
    return EditableField(
        path,
        f"Section {index + 1} - {property_label} ({locale_label})",
        control,
        required=locale == "fr",
        group=f"Sections {locale_label}",
    )


def section_editable_fields(article: Article) -> list[EditableField]:
    fields: list[EditableField] = []
    for locale, locale_label in SECTION_LOCALES:
        sections = get_path(article, f"content.{locale}.sections")
        if not isinstance(sections, list):
            continue
        for index, section in enumerate(sections):
            if not isinstance(section, dict):
                continue
            for property_name, property_label, control in SECTION_PROPERTIES:
                fields.append(
                    EditableField(
                        f"content.{locale}.sections.{index}.{property_name}",
                        f"Section {index + 1} - {property_label} ({locale_label})",
                        control,
                        required=locale == "fr",
                        group=f"Sections {locale_label}",
                    )
                )
    return fields


def editable_field_to_payload(field: EditableField) -> dict[str, Any]:
    return {
        "path": field.path,
        "label": field.label,
        "control": field.control,
        "required": field.required,
        "choices": list(field.choices),
        "group": field.group,
    }


def editable_field_value_payload(article: Article, field: EditableField) -> dict[str, Any]:
    payload = editable_field_to_payload(field)
    payload["value"] = normalize_path_value(get_path(article, field.path))
    return payload


def normalize_path_value(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _path_parts(path: str) -> list[str]:
    return path.split(".")


def _list_index(part: str) -> int | None:
    if not part.isdigit():
        return None
    return int(part)


def get_path(article: Article, path: str) -> Any:
    current: Any = article
    for part in _path_parts(path):
        if isinstance(current, dict):
            current = current.get(part)
            continue

        index = _list_index(part)
        if isinstance(current, list) and index is not None and index < len(current):
            current = current[index]
            continue

        return ""
    return current


def set_path(article: Article, path: str, value: Any) -> None:
    parts = _path_parts(path)
    current: Any = article
    for part in parts[:-1]:
        if isinstance(current, dict):
            child = current.get(part)
            if not isinstance(child, (dict, list)):
                child = {}
                current[part] = child
            current = child
            continue

        index = _list_index(part)
        if isinstance(current, list) and index is not None and index < len(current):
            current = current[index]
            continue

        raise ValueError(f"Cannot set missing path segment: {part}")

    final_part = parts[-1]
    if isinstance(current, dict):
        current[final_part] = value
        return

    index = _list_index(final_part)
    if isinstance(current, list) and index is not None and index < len(current):
        current[index] = value
        return

    raise ValueError(f"Cannot set path: {path}")
