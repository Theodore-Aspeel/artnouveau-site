"""Validation helpers for exported Reel pilot handoff payloads."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .reel_pilot import REEL_PILOT_CONTRACT_NAME, REEL_PILOT_CONTRACT_VERSION


ALLOWED_PILOT_STATUSES = {
    "needs_editorial_input",
    "needs_upstream_review",
    "ready_for_human_storyboard_review",
}


@dataclass(frozen=True)
class ReelPilotValidationResult:
    ok: bool
    errors: tuple[str, ...]


def validate_reel_pilot_file(path: str | Path) -> ReelPilotValidationResult:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as error:
        return ReelPilotValidationResult(False, (f"Could not read file: {error}",))
    except json.JSONDecodeError as error:
        return ReelPilotValidationResult(False, (f"Invalid JSON: {error}",))
    return validate_reel_pilot_payload(payload)


def validate_reel_pilot_payload(payload: Any) -> ReelPilotValidationResult:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ReelPilotValidationResult(False, ("Payload must be a JSON object.",))

    _expect_contract(payload.get("contract"), errors)
    _expect_text(payload.get("slug"), "slug", errors)
    if payload.get("pilot_status") not in ALLOWED_PILOT_STATUSES:
        errors.append("pilot_status is not supported.")

    format_block = _mapping(payload.get("format"), "format", errors)
    if format_block:
        if format_block.get("aspect_ratio") != "9:16":
            errors.append("format.aspect_ratio must be '9:16'.")
        if format_block.get("width_px") != 1080 or format_block.get("height_px") != 1920:
            errors.append("format dimensions must be 1080 x 1920.")

    creative = _mapping(payload.get("creative"), "creative", errors)
    if creative:
        hooks = creative.get("hook_options")
        if not isinstance(hooks, list) or not hooks:
            errors.append("creative.hook_options must be a non-empty array.")
        storyboard = creative.get("storyboard")
        if not isinstance(storyboard, list) or not storyboard:
            errors.append("creative.storyboard must be a non-empty array.")

    link_plan = _mapping(payload.get("link_plan"), "link_plan", errors)
    if link_plan:
        _expect_text(link_plan.get("tracked_url"), "link_plan.tracked_url", errors)
        _mapping(link_plan.get("utm"), "link_plan.utm", errors)

    gates = payload.get("human_gates")
    if not isinstance(gates, list) or len(gates) < 4:
        errors.append("human_gates must contain the four review gates.")

    limits = _mapping(payload.get("automation_limits"), "automation_limits", errors)
    for key in ("renders_video", "uploads_media", "publishes_to_instagram", "stores_credentials"):
        if limits and limits.get(key) is not False:
            errors.append(f"automation_limits.{key} must be false.")

    return ReelPilotValidationResult(not errors, tuple(errors))


def _expect_contract(value: Any, errors: list[str]) -> None:
    contract = _mapping(value, "contract", errors)
    if not contract:
        return
    if contract.get("name") != REEL_PILOT_CONTRACT_NAME:
        errors.append(f"contract.name must be {REEL_PILOT_CONTRACT_NAME!r}.")
    if contract.get("version") != REEL_PILOT_CONTRACT_VERSION:
        errors.append(f"contract.version must be {REEL_PILOT_CONTRACT_VERSION}.")
    if contract.get("kind") != "read_only_reel_pilot_handoff":
        errors.append("contract.kind must be 'read_only_reel_pilot_handoff'.")


def _mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object.")
        return {}
    return value


def _expect_text(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty string.")
