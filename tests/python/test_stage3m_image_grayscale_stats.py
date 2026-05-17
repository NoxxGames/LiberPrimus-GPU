from __future__ import annotations

from PIL import Image

from libreprimus.image_analysis.grayscale_stats import average_hash_8x8, histogram_stats, to_grayscale


def test_synthetic_grayscale_stats_are_deterministic() -> None:
    image = Image.new("L", (2, 2))
    image.putdata([0, 64, 128, 255])

    stats = histogram_stats(image)

    assert stats["grayscale_min"] == 0
    assert stats["grayscale_max"] == 255
    assert stats["grayscale_mean"] == 111.75
    assert stats["black_pixel_ratio"] == 0.25
    assert stats["white_pixel_ratio"] == 0.25


def test_rgb_conversion_to_grayscale_is_stable() -> None:
    image = Image.new("RGB", (1, 1), (255, 0, 0))
    gray = to_grayscale(image)

    assert gray.mode == "L"
    assert list(gray.getdata()) == [76]


def test_average_hash_is_compact_deterministic_hex() -> None:
    image = Image.new("L", (8, 8), 255)

    assert average_hash_8x8(image) == "ffffffffffffffff"
