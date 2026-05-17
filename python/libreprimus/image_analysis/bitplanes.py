"""Bit-plane density summaries for 8-bit grayscale images."""

from __future__ import annotations

from typing import Any

from PIL import Image


def bitplane_records(image_id: str, gray: Image.Image) -> list[dict[str, Any]]:
    """Return one/zero density records for grayscale bit planes 0 through 7."""
    histogram = gray.histogram()
    total = sum(histogram)
    records: list[dict[str, Any]] = []
    for bitplane in range(8):
        one_count = sum(count for value, count in enumerate(histogram) if value & (1 << bitplane))
        one_ratio = round(one_count / total, 8) if total else 0.0
        records.append(
            {
                "record_type": "image_bitplane_summary",
                "image_id": image_id,
                "bitplane": bitplane,
                "one_ratio": one_ratio,
                "zero_ratio": round(1.0 - one_ratio, 8),
                "trusted_as_canonical": False,
                "solve_claim": False,
            }
        )
    return records
