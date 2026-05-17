"""Deterministic symmetry metrics for grayscale images."""

from __future__ import annotations

from typing import Any

from PIL import Image, ImageChops, ImageStat

DEFAULT_MAX_DIMENSION = 512


def symmetry_record(image_id: str, gray: Image.Image, *, max_dimension: int = DEFAULT_MAX_DIMENSION) -> dict[str, Any]:
    """Compute normalized mean absolute differences for simple mirror/rotation metrics."""
    analysis = _analysis_image(gray, max_dimension=max_dimension)
    return {
        "record_type": "image_symmetry_record",
        "image_id": image_id,
        "horizontal_mirror_difference": _difference(
            analysis, analysis.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        ),
        "vertical_mirror_difference": _difference(
            analysis, analysis.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        ),
        "rotational_180_difference": _difference(analysis, analysis.transpose(Image.Transpose.ROTATE_180)),
        "diagonal_difference": _diagonal_difference(analysis),
        "symmetry_rank_fields": [
            "horizontal_mirror_difference",
            "vertical_mirror_difference",
            "rotational_180_difference",
        ],
        "analysis_width": analysis.width,
        "analysis_height": analysis.height,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }


def _analysis_image(gray: Image.Image, *, max_dimension: int) -> Image.Image:
    width, height = gray.size
    largest = max(width, height)
    if largest <= max_dimension:
        return gray.copy()
    scale = max_dimension / largest
    resized = (max(1, round(width * scale)), max(1, round(height * scale)))
    resample = getattr(Image, "Resampling", Image).BILINEAR
    return gray.resize(resized, resample=resample)


def _difference(left: Image.Image, right: Image.Image) -> float:
    diff = ImageChops.difference(left, right)
    mean = ImageStat.Stat(diff).mean[0]
    return round(mean / 255.0, 8)


def _diagonal_difference(gray: Image.Image) -> float | None:
    if gray.width != gray.height:
        return None
    return _difference(gray, gray.transpose(Image.Transpose.TRANSPOSE))
