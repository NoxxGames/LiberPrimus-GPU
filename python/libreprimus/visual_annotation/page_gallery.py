"""Page-image helpers for generated Stage 4C annotation sites."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import shutil

from PIL import Image


def relevant_images(
    tasks: list[dict[str, Any]], image_artifacts: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return image artifacts referenced by Stage 4C tasks."""

    wanted = {image_ref for task in tasks for image_ref in task.get("image_refs", [])}
    return [artifact for artifact in image_artifacts if artifact.get("image_id") in wanted]


def copy_or_thumbnail_image(source: Path, target: Path, *, max_size: int = 1200) -> tuple[int, int]:
    """Create a generated review-size copy for the local site."""

    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(source) as image:
            image.thumbnail((max_size, max_size))
            image.convert("RGB").save(target)
            return image.width, image.height
    except Exception:
        shutil.copy2(source, target)
        return 0, 0
