"""Basic deterministic image transforms."""

from __future__ import annotations

from PIL import Image, ImageOps

from libreprimus.image_analysis.grayscale_stats import to_grayscale
from libreprimus.image_transforms.models import THRESHOLDS


def basic_transform_images(image: Image.Image) -> list[tuple[str, dict, Image.Image]]:
    """Return grayscale, inverse, contrast, posterize, and threshold previews."""
    gray = to_grayscale(image)
    transforms: list[tuple[str, dict, Image.Image]] = [
        ("grayscale", {}, gray),
        ("invert", {}, ImageOps.invert(gray)),
        ("autocontrast", {}, ImageOps.autocontrast(gray)),
        ("posterize_2bit", {"bits": 2}, ImageOps.posterize(gray.convert("RGB"), 2).convert("L")),
    ]
    for threshold in THRESHOLDS:
        transforms.append(
            (
                f"threshold_{threshold}",
                {"threshold": threshold},
                gray.point(lambda pixel, t=threshold: 0 if pixel <= t else 255, mode="L"),
            )
        )
    return transforms
