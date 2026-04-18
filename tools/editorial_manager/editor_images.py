"""Controlled image catalog for the local article editor."""

from __future__ import annotations

from pathlib import Path
import re
import unicodedata

from .repository import PROJECT_ROOT


IMAGE_EXTENSIONS = {".avif", ".gif", ".jpg", ".jpeg", ".png", ".webp"}
IMAGE_SRC_PREFIX = "assets/images/"
IMAGE_IMPORT_DIR = Path("src") / "assets" / "images" / "articles" / "imported"
IMAGE_IMPORT_MAX_BYTES = 20 * 1024 * 1024


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


def import_editor_image(filename: str, payload: bytes, project_root: Path = PROJECT_ROOT) -> dict[str, str]:
    """Copy one uploaded local image into the controlled editor image catalog."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("Le fichier image est vide.")
    if len(payload) > IMAGE_IMPORT_MAX_BYTES:
        raise ValueError("Le fichier image depasse la limite de 20 Mo.")

    safe_name = normalized_image_filename(filename)
    target_dir = safe_import_dir(project_root)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = available_import_path(target_dir, safe_name)

    with target_path.open("xb") as handle:
        handle.write(payload)

    src = image_src_from_path(target_path, project_root)
    return {"src": src, "label": src.removeprefix(IMAGE_SRC_PREFIX)}


def normalized_image_filename(filename: str) -> str:
    """Return a safe lowercase image filename with an allowed extension."""
    raw_name = Path(str(filename or "")).name
    suffix = Path(raw_name).suffix.lower()
    if suffix not in IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(IMAGE_EXTENSIONS))
        raise ValueError(f"Extension non autorisee. Extensions acceptees: {allowed}.")

    stem = raw_name[: -len(Path(raw_name).suffix)] if Path(raw_name).suffix else raw_name
    ascii_stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_stem).strip("-").lower()
    if not normalized:
        normalized = "image"
    return f"{normalized}{suffix}"


def safe_import_dir(project_root: Path) -> Path:
    """Resolve the import folder and keep it below src/assets/images/articles."""
    target_dir = (project_root / IMAGE_IMPORT_DIR).resolve()
    articles_root = (project_root / "src" / "assets" / "images" / "articles").resolve()
    try:
        target_dir.relative_to(articles_root)
    except ValueError as exc:
        raise ValueError("Dossier d'import image invalide.") from exc
    return target_dir


def available_import_path(target_dir: Path, filename: str) -> Path:
    """Return a non-existing path, adding -2, -3... on clear collisions."""
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    candidate = target_dir / filename
    index = 2
    while candidate.exists():
        candidate = target_dir / f"{stem}-{index}{suffix}"
        index += 1
    return candidate


def project_root_from_articles_path(path: Path) -> Path:
    """Infer a project root from src/data/articles.json, with repository fallback."""
    resolved = path.resolve()
    if resolved.name == "articles.json" and resolved.parent.name == "data" and resolved.parent.parent.name == "src":
        return resolved.parent.parent.parent
    return PROJECT_ROOT


def image_src_from_path(image_path: Path, project_root: Path) -> str:
    relative = image_path.resolve().relative_to((project_root / "src").resolve())
    return relative.as_posix()
