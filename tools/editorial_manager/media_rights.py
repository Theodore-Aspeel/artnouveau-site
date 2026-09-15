"""Deterministic media-rights checks for runtime images."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Any

from .repository import PROJECT_ROOT


REGISTRY_PATH = PROJECT_ROOT / "research" / "media-rights.json"
EXPECTED_CONTRACT = ("artnouveau.media_rights", 1)
SOURCE_TYPES = {"original_photography"}
RIGHTS_STATUSES = {"cleared", "pending", "restricted"}
CONFIRMATION_BASES = {"project_owner_statement"}
STATIC_PUBLIC_PAGES = (
    "src/pages/index.html",
    "src/pages/about.html",
    "src/pages/mentions.html",
    "src/pages/article-redirect.html",
)
SITE_IMAGE_REF_RE = re.compile(
    r"""(?:src|srcset|href|content)=["']([^"']*assets/images/site/[^"']+)["']""",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class MediaRightsIssue:
    severity: str
    code: str
    src: str
    message: str


@dataclass(frozen=True)
class MediaRightsReport:
    status: str
    runtime_asset_count: int
    cleared_count: int
    issues: tuple[MediaRightsIssue, ...]

    @property
    def ok(self) -> bool:
        return not any(issue.severity == "ERROR" for issue in self.issues)

    def to_payload(self) -> dict[str, Any]:
        return {
            "contract": {
                "name": "artnouveau.media_rights_report",
                "version": 1,
            },
            "status": self.status,
            "runtime_asset_count": self.runtime_asset_count,
            "cleared_count": self.cleared_count,
            "issues": [asdict(issue) for issue in self.issues],
        }


def load_media_rights_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def collect_runtime_assets(articles: list[dict[str, Any]], project_root: Path = PROJECT_ROOT) -> list[str]:
    assets: set[str] = set()
    for article in articles:
        assets.update(collect_article_assets(article))

    for relative_path in STATIC_PUBLIC_PAGES:
        page_path = project_root / relative_path
        if not page_path.is_file():
            continue
        raw = page_path.read_text(encoding="utf-8")
        for match in SITE_IMAGE_REF_RE.finditer(raw):
            src = match.group(1).strip().replace("\\", "/")
            while src.startswith("../"):
                src = src[3:]
            if src.startswith("assets/images/"):
                assets.add(src)
    return sorted(assets)


def check_media_rights(
    runtime_assets: list[str],
    registry: dict[str, Any],
    *,
    project_root: Path = PROJECT_ROOT,
    warn_unused: bool = True,
    image_probe=None,
) -> MediaRightsReport:
    issues: list[MediaRightsIssue] = []
    registry_entries = flatten_registry(registry, issues)
    unique_runtime_assets = sorted(set(clean(asset) for asset in runtime_assets if clean(asset)))

    contract = registry.get("contract")
    contract_name = contract.get("name") if isinstance(contract, dict) else None
    contract_version = contract.get("version") if isinstance(contract, dict) else None
    if (contract_name, contract_version) != EXPECTED_CONTRACT:
        issues.append(error("invalid-contract", "", "Registry must use artnouveau.media_rights@1."))

    existing_assets: list[str] = []
    for src in unique_runtime_assets:
        entry = registry_entries.get(src)
        if entry is None:
            issues.append(error("missing-rights-record", src, "Runtime image is absent from the rights registry."))
            continue
        if entry["rights_status"] != "cleared":
            issues.append(
                error("rights-not-cleared", src, f"Rights status is {entry['rights_status'] or 'missing'}.")
            )
        if not entry["public_credit"]:
            issues.append(error("missing-public-credit", src, "Rights record has no public credit."))
        asset_path = project_root / "src" / src
        if not asset_path.is_file():
            issues.append(error("missing-image-file", src, "Registered runtime image file does not exist."))
        else:
            existing_assets.append(src)

    probe = image_probe or probe_image_files
    probe_results = probe(existing_assets, project_root)
    for src in existing_assets:
        if not probe_results.get(src, False):
            issues.append(error("invalid-image-content", src, "Runtime image cannot be decoded as a valid image."))

    if warn_unused:
        for src in sorted(set(registry_entries) - set(unique_runtime_assets)):
            issues.append(warning("unused-rights-record", src, "Registered image is not used by the public runtime."))

    error_count = sum(issue.severity == "ERROR" for issue in issues)
    warning_count = sum(issue.severity == "WARNING" for issue in issues)
    status = "blocked" if error_count else ("needs-review" if warning_count else "ready")
    cleared_count = sum(
        src in registry_entries and registry_entries[src]["rights_status"] == "cleared"
        for src in unique_runtime_assets
    )
    return MediaRightsReport(
        status=status,
        runtime_asset_count=len(unique_runtime_assets),
        cleared_count=cleared_count,
        issues=tuple(issues),
    )


def flatten_registry(
    registry: dict[str, Any],
    issues: list[MediaRightsIssue],
) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    collections = registry.get("collections")
    if not isinstance(collections, list):
        issues.append(error("invalid-collections", "", "Registry collections must be an array."))
        return entries

    for index, collection in enumerate(collections):
        if not isinstance(collection, dict):
            issues.append(error("invalid-collection", "", f"Collection #{index + 1} must be an object."))
            continue
        assets = collection.get("assets")
        if not isinstance(assets, list):
            issues.append(error("invalid-assets", "", f"Collection #{index + 1} assets must be an array."))
            continue
        metadata = {
            "id": clean(collection.get("id")),
            "creator": clean(collection.get("creator")),
            "rights_holder": clean(collection.get("rights_holder")),
            "public_credit": clean(collection.get("public_credit")),
            "source_type": clean(collection.get("source_type")),
            "rights_status": clean(collection.get("rights_status")),
            "confirmed_on": clean(collection.get("confirmed_on")),
            "confirmation_basis": clean(collection.get("confirmation_basis")),
        }
        for field, value in metadata.items():
            if not value:
                issues.append(
                    error(
                        f"missing-{field.replace('_', '-')}",
                        "",
                        f"Collection #{index + 1} is missing {field}.",
                    )
                )
        if metadata["source_type"] and metadata["source_type"] not in SOURCE_TYPES:
            issues.append(error("invalid-source-type", "", f"Collection #{index + 1} has an unsupported source type."))
        if metadata["rights_status"] and metadata["rights_status"] not in RIGHTS_STATUSES:
            issues.append(error("invalid-rights-status", "", f"Collection #{index + 1} has an invalid rights status."))
        if metadata["confirmation_basis"] and metadata["confirmation_basis"] not in CONFIRMATION_BASES:
            issues.append(
                error("invalid-confirmation-basis", "", f"Collection #{index + 1} has an unsupported confirmation basis.")
            )
        if metadata["confirmed_on"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata["confirmed_on"]):
            issues.append(error("invalid-confirmed-on", "", f"Collection #{index + 1} confirmed_on must be YYYY-MM-DD."))
        for asset in assets:
            src = clean(asset)
            if not src:
                issues.append(error("invalid-asset-path", "", "Registry asset paths must be non-empty strings."))
                continue
            if not src.startswith("assets/images/") or src.startswith("/") or "://" in src:
                issues.append(error("invalid-asset-path", src, "Registry asset must be a local assets/images path."))
                continue
            if src in entries:
                issues.append(error("duplicate-rights-record", src, "Image occurs more than once in the registry."))
                continue
            entries[src] = metadata

    return entries


def collect_article_assets(article: dict[str, Any]) -> list[str]:
    media = article.get("media")
    if isinstance(media, dict):
        entries = [media.get("hero")]
        support = media.get("support")
        if isinstance(support, list):
            entries.extend(support)
    else:
        entries = [article.get("hero_image")]
        support = article.get("support_images")
        if isinstance(support, list):
            entries.extend(support)

    assets: set[str] = set()
    for entry in entries:
        if isinstance(entry, str):
            src = clean(entry)
        elif isinstance(entry, dict):
            src = clean(entry.get("src") or entry.get("path") or entry.get("image"))
        else:
            src = ""
        if src:
            assets.add(src)
    return sorted(assets)


def probe_image_files(assets: list[str], project_root: Path) -> dict[str, bool]:
    if not assets:
        return {}
    script_path = PROJECT_ROOT / "scripts" / "probe-images.mjs"
    absolute_paths = [(project_root / "src" / src).resolve() for src in assets]
    completed = subprocess.run(
        ["node", str(script_path), *(str(path) for path in absolute_paths)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {src: False for src in assets}
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {src: False for src in assets}
    return {
        src: payload.get(str(absolute_path), False) is True
        for src, absolute_path in zip(assets, absolute_paths)
    }


def render_media_rights_report(report: MediaRightsReport) -> str:
    lines = [
        "Media rights check",
        f"Status: {report.status}",
        f"Runtime assets: {report.runtime_asset_count}",
        f"Cleared assets: {report.cleared_count}",
    ]
    if report.issues:
        lines.append("Issues:")
        lines.extend(
            f"  {issue.severity} {issue.code}: {issue.src or '-'} - {issue.message}"
            for issue in report.issues
        )
    else:
        lines.append("Issues: none")
    return "\n".join(lines)


def clean(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def error(code: str, src: str, message: str) -> MediaRightsIssue:
    return MediaRightsIssue("ERROR", code, src, message)


def warning(code: str, src: str, message: str) -> MediaRightsIssue:
    return MediaRightsIssue("WARNING", code, src, message)
