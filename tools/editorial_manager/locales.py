"""Central locale contract for editorial tooling.

This module prepares optional locales without making them public content
requirements. French remains the required source locale.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocaleSpec:
    code: str
    label: str
    required: bool = False
    public: bool = False
    preview: bool = False
    editable: bool = False


SUPPORTED_LOCALES: tuple[LocaleSpec, ...] = (
    LocaleSpec("fr", "FR", required=True, public=True, preview=True, editable=True),
    LocaleSpec("en", "EN", required=False, public=True, preview=True, editable=True),
    LocaleSpec("nl", "NL", required=False, public=False, preview=True, editable=True),
)

DEFAULT_LOCALE = "fr"
FALLBACK_LOCALES = ("fr", "en")


def normalize_locale(locale: str | None, default: str = DEFAULT_LOCALE) -> str:
    candidate = (locale or "").strip().lower().split("-", 1)[0]
    return candidate if candidate in supported_locale_codes() else default


def supported_locale_codes() -> tuple[str, ...]:
    return tuple(locale.code for locale in SUPPORTED_LOCALES)


def required_locale_codes() -> tuple[str, ...]:
    return tuple(locale.code for locale in SUPPORTED_LOCALES if locale.required)


def optional_locale_codes() -> tuple[str, ...]:
    return tuple(locale.code for locale in SUPPORTED_LOCALES if not locale.required)


def public_locale_codes() -> tuple[str, ...]:
    return tuple(locale.code for locale in SUPPORTED_LOCALES if locale.public)


def preview_locale_codes() -> tuple[str, ...]:
    return tuple(locale.code for locale in SUPPORTED_LOCALES if locale.preview)


def editable_locale_specs() -> tuple[LocaleSpec, ...]:
    return tuple(locale for locale in SUPPORTED_LOCALES if locale.editable)


def locale_label(locale: str) -> str:
    normalized = normalize_locale(locale)
    for spec in SUPPORTED_LOCALES:
        if spec.code == normalized:
            return spec.label
    return normalized.upper()


def is_required_locale(locale: str) -> bool:
    normalized = normalize_locale(locale)
    return normalized in required_locale_codes()


def locale_status_choices() -> tuple[str, ...]:
    choices = ["fr-only"]
    for locale in optional_locale_codes():
        missing_status = "fr-only" if locale == "en" else f"{locale}-missing"
        if missing_status not in choices:
            choices.append(missing_status)
        choices.extend((f"{locale}-partial", f"{locale}-ready"))
    return tuple(choices)
