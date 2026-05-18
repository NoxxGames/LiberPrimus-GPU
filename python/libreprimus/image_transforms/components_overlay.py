"""Largest-component overlay transforms."""

from __future__ import annotations

from PIL import Image, ImageDraw

from libreprimus.image_analysis.components import component_summary
from libreprimus.image_analysis.grayscale_stats import to_grayscale
from libreprimus.image_transforms.models import COMPONENT_OVERLAY_THRESHOLDS


def component_overlay_images(image: Image.Image) -> list[tuple[str, dict, Image.Image, dict[str, float]]]:
    """Overlay largest threshold-component boxes for selected thresholds."""
    gray = to_grayscale(image)
    records: list[tuple[str, dict, Image.Image, dict[str, float]]] = []
    for threshold in COMPONENT_OVERLAY_THRESHOLDS:
        summary = component_summary(gray, threshold=threshold, top_k=5)
        preview = gray.convert("RGB")
        draw = ImageDraw.Draw(preview)
        scale_x = gray.width / max(1, summary.analysis_width)
        scale_y = gray.height / max(1, summary.analysis_height)
        for component in summary.largest_components:
            min_x, min_y, max_x, max_y = component["bbox"]
            box = [
                round(min_x * scale_x),
                round(min_y * scale_y),
                round(max_x * scale_x),
                round(max_y * scale_y),
            ]
            draw.rectangle(box, outline=(255, 0, 0), width=max(1, gray.width // 256))
        records.append(
            (
                f"component_overlay_{threshold}",
                {"threshold": threshold, "connectivity": summary.connectivity},
                preview,
                {
                    "component_count": float(summary.component_count),
                    "largest_component_area_ratio": summary.largest_component_area_ratio,
                },
            )
        )
    return records
