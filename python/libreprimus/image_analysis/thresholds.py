"""Threshold summary helpers."""

from __future__ import annotations

from typing import Any

from PIL import Image

from libreprimus.image_analysis.components import component_summary

DEFAULT_THRESHOLDS = (32, 64, 96, 128, 160, 192, 224)


def threshold_and_component_records(
    image_id: str,
    gray: Image.Image,
    *,
    thresholds: tuple[int, ...] = DEFAULT_THRESHOLDS,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Build threshold and component records for a grayscale image."""
    histogram = gray.histogram()
    total = sum(histogram)
    threshold_records: list[dict[str, Any]] = []
    component_records: list[dict[str, Any]] = []
    for threshold in thresholds:
        foreground_count = sum(histogram[: threshold + 1])
        foreground_ratio = round(foreground_count / total, 8) if total else 0.0
        component = component_summary(gray, threshold=threshold)
        base = {
            "image_id": image_id,
            "threshold": threshold,
            "component_count": component.component_count,
            "component_analysis_width": component.analysis_width,
            "component_analysis_height": component.analysis_height,
            "component_connectivity": component.connectivity,
            "trusted_as_canonical": False,
            "solve_claim": False,
        }
        threshold_records.append(
            {
                "record_type": "image_threshold_summary",
                **base,
                "foreground_ratio": foreground_ratio,
                "background_ratio": round(1.0 - foreground_ratio, 8),
                "largest_component_area_ratio": round(component.largest_component_area_ratio, 8),
            }
        )
        component_records.append(
            {
                "record_type": "image_component_summary",
                **base,
                "largest_components": component.largest_components,
            }
        )
    return threshold_records, component_records
