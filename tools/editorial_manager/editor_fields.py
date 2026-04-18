"""Editable field contract for the local article editor.

The browser UI is deliberately thin. This module is the source of truth for
which article fields can be edited by non-technical users.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from .locales import editable_locale_specs, is_required_locale, locale_label


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
    readonly_key: str = ""


LOCALIZED_MAIN_FIELDS = (
    ("title", "Titre", "text", True),
    ("dek", "Chapeau", "textarea", True),
    ("epigraph", "Epigraphe", "textarea", True),
    ("seo.meta_description", "Description SEO", "textarea", True),
    ("media.hero_alt", "Texte alternatif de l'image principale", "textarea", True),
    ("around.note", "Note de l'article lie", "textarea", False),
)


def localized_main_fields() -> tuple[EditableField, ...]:
    fields: list[EditableField] = []
    for locale in editable_locale_specs():
        for path_suffix, label, control, required_in_source in LOCALIZED_MAIN_FIELDS:
            fields.append(
                EditableField(
                    f"content.{locale.code}.{path_suffix}",
                    f"{label} {locale.label}",
                    control,
                    required=required_in_source and locale.required,
                )
            )
    return tuple(fields)


EDITABLE_FIELDS: tuple[EditableField, ...] = (
    EditableField("status", "Statut de publication", "select", required=True, choices=STATUS_VALUES),
    EditableField("media.hero.src", "Image principale", "image-select", required=True, group="Image principale"),
    *localized_main_fields(),
)

EDITABLE_FIELD_BY_PATH = {field.path: field for field in EDITABLE_FIELDS}
EDITABLE_LOCALE_PATTERN = "|".join(re.escape(locale.code) for locale in editable_locale_specs())
SECTION_FIELD_RE = re.compile(rf"^content\.({EDITABLE_LOCALE_PATTERN})\.sections\.(0|[1-9]\d*)\.(heading|body)$")
PRACTICAL_ITEM_FIELD_RE = re.compile(rf"^content\.({EDITABLE_LOCALE_PATTERN})\.practical_items\.(0|[1-9]\d*)\.value$")
SUPPORT_IMAGE_FIELD_RE = re.compile(r"^media\.support\.(0|[1-9]\d*)\.src$")
SECTION_LOCALES = tuple((locale.code, locale.label) for locale in editable_locale_specs())
SECTION_PROPERTIES = (("heading", "titre", "text"), ("body", "texte", "textarea"))
PRACTICAL_ITEM_LABELS = {
    "city": "Ville",
    "country": "Pays",
    "style": "Style",
    "architect": "Architecte",
    "address": "Adresse",
    "date": "Date",
    "access": "Acces",
}


def editable_field_payload() -> list[dict[str, Any]]:
    return [editable_field_to_payload(field) for field in EDITABLE_FIELDS]


def editable_fields_for_article(article: Article) -> list[EditableField]:
    return [
        *EDITABLE_FIELDS,
        *support_image_editable_fields(article),
        *section_editable_fields(article),
        *practical_item_editable_fields(article),
    ]


def editable_field_for_path(article: Article, path: str) -> EditableField | None:
    field = EDITABLE_FIELD_BY_PATH.get(path)
    if field is not None:
        return field

    support_match = SUPPORT_IMAGE_FIELD_RE.match(path)
    if support_match:
        index = int(support_match.group(1))
        support_images = get_path(article, "media.support")
        if (
            isinstance(support_images, list)
            and index < len(support_images)
            and isinstance(support_images[index], dict)
        ):
            return support_image_editable_field(index, path)
        return None

    practical_match = PRACTICAL_ITEM_FIELD_RE.match(path)
    if practical_match:
        locale, index_text = practical_match.groups()
        practical_items = get_path(article, f"content.{locale}.practical_items")
        index = int(index_text)
        if (
            isinstance(practical_items, list)
            and index < len(practical_items)
            and isinstance(practical_items[index], dict)
        ):
            return practical_item_editable_field(locale, index, practical_items[index], path)
        return None

    match = SECTION_FIELD_RE.match(path)
    if not match:
        return None

    locale, index_text, property_name = match.groups()
    sections = get_path(article, f"content.{locale}.sections")
    index = int(index_text)
    if not isinstance(sections, list) or index >= len(sections) or not isinstance(sections[index], dict):
        return None

    current_locale_label = locale_label(locale)
    property_label = "titre" if property_name == "heading" else "texte"
    control = "text" if property_name == "heading" else "textarea"
    return EditableField(
        path,
        f"Section {index + 1} - {property_label} ({current_locale_label})",
        control,
        required=is_required_locale(locale),
        group=f"Sections {current_locale_label}",
    )


def section_editable_fields(article: Article) -> list[EditableField]:
    fields: list[EditableField] = []
    for locale, current_locale_label in SECTION_LOCALES:
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
                        f"Section {index + 1} - {property_label} ({current_locale_label})",
                        control,
                        required=is_required_locale(locale),
                        group=f"Sections {current_locale_label}",
                    )
                )
    return fields


def practical_item_editable_fields(article: Article) -> list[EditableField]:
    fields: list[EditableField] = []
    for locale, _current_locale_label in SECTION_LOCALES:
        practical_items = get_path(article, f"content.{locale}.practical_items")
        if not isinstance(practical_items, list):
            continue
        for index, item in enumerate(practical_items):
            if not isinstance(item, dict):
                continue
            fields.append(
                practical_item_editable_field(
                    locale,
                    index,
                    item,
                    f"content.{locale}.practical_items.{index}.value",
                )
            )
    return fields


def practical_item_editable_field(locale: str, index: int, item: dict[str, Any], path: str) -> EditableField:
    current_locale_label = locale_label(locale)
    key = normalize_path_value(item.get("key"))
    label = PRACTICAL_ITEM_LABELS.get(key, key.replace("_", " ").capitalize() if key else f"Ligne {index + 1}")
    return EditableField(
        path,
        f"{label} ({current_locale_label})",
        "text",
        required=is_required_locale(locale),
        group=f"Informations pratiques {current_locale_label}",
        readonly_key=key,
    )


def support_image_editable_fields(article: Article) -> list[EditableField]:
    support_images = get_path(article, "media.support")
    if not isinstance(support_images, list):
        return []

    fields: list[EditableField] = []
    for index, image in enumerate(support_images):
        if not isinstance(image, dict):
            continue
        fields.append(support_image_editable_field(index, f"media.support.{index}.src"))
    return fields


def support_image_editable_field(index: int, path: str) -> EditableField:
    return EditableField(
        path,
        f"Image support {index + 1}",
        "image-select",
        required=True,
        group="Images support",
    )


def editable_field_to_payload(field: EditableField) -> dict[str, Any]:
    return {
        "path": field.path,
        "label": field.label,
        "control": field.control,
        "required": field.required,
        "choices": list(field.choices),
        "group": field.group,
        "readonly_key": field.readonly_key,
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
