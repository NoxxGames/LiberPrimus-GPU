"""Bitplane preview transforms."""

from __future__ import annotations

from PIL import Image

from libreprimus.image_analysis.grayscale_stats import to_grayscale


def bitplane_transform_images(image: Image.Image) -> list[tuple[str, dict, Image.Image, dict[str, float]]]:
    """Return grayscale bitplane previews and density metrics."""
    gray = to_grayscale(image)
    pixels = list(gray.getdata())
    total = max(1, len(pixels))
    records: list[tuple[str, dict, Image.Image, dict[str, float]]] = []
    for bitplane in range(8):
        mask = 1 << bitplane
        out_pixels = [255 if pixel & mask else 0 for pixel in pixels]
        preview = Image.new("L", gray.size)
        preview.putdata(out_pixels)
        one_ratio = sum(1 for pixel in pixels if pixel & mask) / total
        records.append(
            (
                f"bitplane_{bitplane}",
                {"bitplane": bitplane},
                preview,
                {"one_ratio": round(one_ratio, 8), "zero_ratio": round(1.0 - one_ratio, 8)},
            )
        )
    return records
