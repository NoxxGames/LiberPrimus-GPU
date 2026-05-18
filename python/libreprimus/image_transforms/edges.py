"""Dependency-free edge-map transform."""

from __future__ import annotations

from PIL import Image

from libreprimus.image_analysis.grayscale_stats import to_grayscale


def difference_edge_map(image: Image.Image) -> tuple[Image.Image, dict[str, float]]:
    """Return a simple finite-difference edge magnitude map."""
    gray = to_grayscale(image)
    width, height = gray.size
    pixels = list(gray.getdata())
    out = bytearray(width * height)
    total = 0
    high = 0
    for y in range(height):
        for x in range(width):
            index = y * width + x
            current = pixels[index]
            left = pixels[index - 1] if x > 0 else current
            up = pixels[index - width] if y > 0 else current
            value = min(255, abs(current - left) + abs(current - up))
            out[index] = value
            total += value
            if value >= 64:
                high += 1
    edge = Image.new("L", gray.size)
    edge.putdata(out)
    count = max(1, width * height)
    return edge, {
        "edge_mean": round(total / (count * 255), 8),
        "edge_density_ratio": round(high / count, 8),
    }
