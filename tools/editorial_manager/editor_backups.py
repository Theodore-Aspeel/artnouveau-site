"""Local safety backups for the Editorial Manager article store."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any
from uuid import uuid4

from .repository import ARTICLES_JSON, PROJECT_ROOT


BACKUP_DIRECTORY_NAME = ".editor-backups"
DEFAULT_BACKUP_LIMIT = 5


def create_articles_backup(
    path: Path = ARTICLES_JSON,
    *,
    project_root: Path = PROJECT_ROOT,
    keep: int = DEFAULT_BACKUP_LIMIT,
) -> dict[str, Any]:
    """Copy the current article payload to the local backup directory."""
    if keep < 1:
        raise ValueError("keep must be at least 1.")

    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Article data file not found: {source}")

    # Refuse to back up malformed data: a safety copy must be restorable JSON.
    _load_articles_payload(source)

    backup_dir = _backup_directory(Path(project_root))
    backup_dir.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc)
    backup_id = f"{created_at.strftime('%Y%m%dT%H%M%S%fZ')}-{uuid4().hex[:8]}"
    destination = backup_dir / f"{backup_id}.json"
    shutil.copyfile(source, destination)

    _prune_backups(backup_dir, keep)
    return _backup_metadata(destination, Path(project_root))


def list_article_backups(*, project_root: Path = PROJECT_ROOT) -> list[dict[str, Any]]:
    """Return available backups, newest first."""
    root = Path(project_root)
    backup_dir = _backup_directory(root)
    if not backup_dir.is_dir():
        return []

    backups = [item for item in backup_dir.glob("*.json") if item.is_file()]
    backups.sort(key=lambda item: (item.stat().st_mtime_ns, item.name), reverse=True)
    return [_backup_metadata(item, root) for item in backups]


def restore_articles_backup(
    backup_id: str | None,
    path: Path = ARTICLES_JSON,
    *,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Atomically restore one known local backup into the article store."""
    if not isinstance(backup_id, str) or not backup_id:
        raise ValueError("A backup id is required.")

    root = Path(project_root)
    available = {item["id"]: item for item in list_article_backups(project_root=root)}
    metadata = available.get(backup_id)
    if metadata is None:
        raise FileNotFoundError(f"Unknown article backup: {backup_id}")

    backup_path = root / metadata["path"]
    payload = _load_articles_payload(backup_path)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, destination)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    return metadata


def _backup_directory(project_root: Path) -> Path:
    return project_root / BACKUP_DIRECTORY_NAME


def _load_articles_payload(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("articles"), list):
        raise ValueError(f"{path} must contain an articles list.")
    return payload


def _backup_metadata(path: Path, project_root: Path) -> dict[str, Any]:
    modified_at = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
    return {
        "id": path.stem,
        "label": modified_at.astimezone().strftime("%Y-%m-%d %H:%M:%S"),
        "path": path.relative_to(project_root).as_posix(),
        "created_at": modified_at.isoformat(),
    }


def _prune_backups(backup_dir: Path, keep: int) -> None:
    backups = [item for item in backup_dir.glob("*.json") if item.is_file()]
    backups.sort(key=lambda item: (item.stat().st_mtime_ns, item.name), reverse=True)
    for stale_backup in backups[keep:]:
        stale_backup.unlink()
