"""Deterministic grayscale, channel, border, and compact hash helpers."""

from __future__ import annotations

from math import sqrt
from typing import Any

from PIL import Image, ImageOps

BLACK_THRESHOLD = 32
WHITE_THRESHOLD = 224


def to_grayscale(image: Image.Image) -> Image.Image:
    """Return a deterministic 8-bit grayscale view without modifying the source image."""
    return ImageOps.grayscale(image)


def histogram_stats(gray: Image.Image) -> dict[str, Any]:
    """Compute deterministic grayscale summary statistics from a PIL grayscale image."""
    histogram = gray.histogram()
    total = sum(histogram)
    if total == 0:
        raise ValueError("image contains no pixels")
    values = [value for value, count in enumerate(histogram) if count]
    mean = sum(value * count for value, count in enumerate(histogram)) / total
    variance = sum(((value - mean) ** 2) * count for value, count in enumerate(histogram)) / total
    return {
        "grayscale_min": min(values),
        "grayscale_max": max(values),
        "grayscale_mean": round(mean, 6),
        "grayscale_median": _median_from_histogram(histogram, total),
        "grayscale_stddev": round(sqrt(variance), 6),
        "black_pixel_ratio": _ratio(sum(histogram[: BLACK_THRESHOLD + 1]), total),
        "white_pixel_ratio": _ratio(sum(histogram[WHITE_THRESHOLD:]), total),
        "midtone_ratio": _ratio(sum(histogram[BLACK_THRESHOLD + 1 : WHITE_THRESHOLD]), total),
    }


def channel_statistics(image: Image.Image) -> dict[str, Any]:
    """Compute deterministic per-channel statistics for RGB-like input."""
    if image.mode == "L":
        return {"mode": "L", "grayscale": _channel_histogram_stats(image)}
    rgb = image.convert("RGB")
    stats: dict[str, Any] = {"mode": "RGB"}
    for channel_name, channel in zip(("red", "green", "blue"), rgb.split(), strict=True):
        stats[channel_name] = _channel_histogram_stats(channel)
    return stats


def border_statistics(gray: Image.Image, *, threshold: int = BLACK_THRESHOLD) -> dict[str, float | int]:
    """Compute dark-pixel ratios for simple border strips."""
    width, height = gray.size
    strip = max(1, min(width, height) // 20)
    crops = {
        "top": gray.crop((0, 0, width, strip)),
        "bottom": gray.crop((0, height - strip, width, height)),
        "left": gray.crop((0, 0, strip, height)),
        "right": gray.crop((width - strip, 0, width, height)),
    }
    stats: dict[str, float | int] = {"strip_width": strip}
    for name, crop in crops.items():
        histogram = crop.histogram()
        total = sum(histogram)
        stats[f"{name}_dark_ratio"] = _ratio(sum(histogram[: threshold + 1]), total)
    return stats


def foreground_bbox(gray: Image.Image, *, threshold: int = WHITE_THRESHOLD) -> list[int] | None:
    """Return the bounding box of non-white foreground pixels, or None for blank images."""
    mask = gray.point(lambda pixel: 255 if pixel <= threshold else 0)
    bbox = mask.getbbox()
    return list(bbox) if bbox is not None else None


def average_hash_8x8(gray: Image.Image) -> str:
    """Return a compact deterministic 64-bit average hash as 16 lowercase hex digits."""
    resample = getattr(Image, "Resampling", Image).LANCZOS
    small = gray.resize((8, 8), resample=resample)
    pixels = list(small.getdata())
    mean = sum(pixels) / len(pixels)
    value = 0
    for pixel in pixels:
        value = (value << 1) | int(pixel >= mean)
    return f"{value:016x}"


def _channel_histogram_stats(channel: Image.Image) -> dict[str, float | int]:
    histogram = channel.histogram()
    total = sum(histogram)
    mean = sum(value * count for value, count in enumerate(histogram)) / total
    variance = sum(((value - mean) ** 2) * count for value, count in enumerate(histogram)) / total
    return {
        "mean": round(mean, 6),
        "stddev": round(sqrt(variance), 6),
        "black_pixel_ratio": _ratio(sum(histogram[: BLACK_THRESHOLD + 1]), total),
        "white_pixel_ratio": _ratio(sum(histogram[WHITE_THRESHOLD:]), total),
    }


def _median_from_histogram(histogram: list[int], total: int) -> float:
    midpoint = (total - 1) / 2
    cumulative = 0
    lower: int | None = None
    upper: int | None = None
    for value, count in enumerate(histogram):
        previous = cumulative
        cumulative += count
        if lower is None and previous <= midpoint < cumulative:
            lower = value
        if previous <= total / 2 < cumulative:
            upper = value
            break
    if lower is None:
        lower = 0
    if upper is None:
        upper = lower
    return round((lower + upper) / 2, 6)


def _ratio(count: int, total: int) -> float:
    return round(count / total, 8) if total else 0.0
