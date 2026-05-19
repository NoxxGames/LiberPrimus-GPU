"""Local image metadata extraction for Stage 4M."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from libreprimus.image_analysis.basic_metadata import read_image_metadata
from libreprimus.image_preflight.models import COMMON_FALSE_FLAGS, IMAGE_EXTENSIONS


def iter_local_images(image_dir: Path) -> list[Path]:
    """Return supported local image paths sorted deterministically."""

    if not image_dir.is_dir():
        return []
    return sorted(
        path
        for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def sha256_file(path: Path) -> str:
    """Compute a SHA-256 digest for a local file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_record(path: Path, *, repo_root: Path) -> dict[str, Any]:
    """Build a deterministic metadata record for a local image."""

    metadata = read_image_metadata(path)
    relative_path = _display_path(path, repo_root)
    file_name = path.name
    image_id = _image_id(file_name)
    return {
        "record_type": "image_preflight_metadata_record",
        "image_id": image_id,
        "relative_path": relative_path,
        "file_name": file_name,
        "extension": path.suffix.lower(),
        "sha256": sha256_file(path),
        "file_size_bytes": path.stat().st_size,
        "width": metadata.width,
        "height": metadata.height,
        "color_mode": metadata.color_mode,
        "image_format": metadata.image_format,
        **COMMON_FALSE_FLAGS,
    }


def build_metadata_records(image_dir: Path, *, repo_root: Path) -> list[dict[str, Any]]:
    """Build records for all supported images under the local page-image directory."""

    return [metadata_record(path, repo_root=repo_root) for path in iter_local_images(image_dir)]


def _image_id(file_name: str) -> str:
    stem = Path(file_name).stem.lower().replace(" ", "-").replace("_", "-")
    return f"stage4m-lp-image-{stem}"


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()
