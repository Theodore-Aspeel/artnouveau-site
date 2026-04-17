"""Controlled image catalog for the local article editor."""

from __future__ import annotations

from pathlib import Path

from .repository import PROJECT_ROOT


IMAGE_EXTENSIONS = {".avif", ".gif", ".jpg", ".jpeg", ".png", ".webp"}
IMAGE_SRC_PREFIX = "assets/images/"


def list_editor_image_options(project_root: Path = PROJECT_ROOT) -> list[dict[str, str]]:
    """Return existing project images as runtime paths usable by article media."""
    image_root = project_root / "src" / "assets" / "images"
    if not image_root.exists():
        return []

    options: list[dict[str, str]] = []
    for image_path in sorted(image_root.rglob("*"), key=lambda item: image_src_from_path(item, project_root).lower()):
        if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        src = image_src_from_path(image_path, project_root)
        options.append({"src": src, "label": src.removeprefix(IMAGE_SRC_PREFIX)})
    return options


def is_valid_editor_image_src(src: str, project_root: Path = PROJECT_ROOT) -> bool:
    """Return True only for existing images under src/assets/images."""
    if not isinstance(src, str):
        return False

    normalized = src.strip().replace("\\", "/")
    if not normalized.startswith(IMAGE_SRC_PREFIX):
        return False
    if ".." in Path(normalized).parts:
        return False
    if Path(normalized).suffix.lower() not in IMAGE_EXTENSIONS:
        return False

    candidate = (project_root / "src" / normalized).resolve()
    image_root = (project_root / "src" / "assets" / "images").resolve()
    try:
        candidate.relative_to(image_root)
    except ValueError:
        return False

    return candidate.is_file()


def editor_image_path(src: str, project_root: Path = PROJECT_ROOT) -> Path | None:
    """Resolve a validated editor image src to a local file path."""
    if not is_valid_editor_image_src(src, project_root):
        return None
    return (project_root / "src" / src.strip().replace("\\", "/")).resolve()


def project_root_from_articles_path(path: Path) -> Path:
    """Infer a project root from src/data/articles.json, with repository fallback."""
    resolved = path.resolve()
    if resolved.name == "articles.json" and resolved.parent.name == "data" and resolved.parent.parent.name == "src":
        return resolved.parent.parent.parent
    return PROJECT_ROOT


def image_src_from_path(image_path: Path, project_root: Path) -> str:
    relative = image_path.resolve().relative_to((project_root / "src").resolve())
    return relative.as_posix()
