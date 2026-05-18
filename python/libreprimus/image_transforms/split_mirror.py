"""Split, mirror, and difference transforms."""

from __future__ import annotations

from PIL import Image, ImageChops, ImageOps

from libreprimus.image_analysis.grayscale_stats import to_grayscale


def split_mirror_transform_images(image: Image.Image) -> list[tuple[str, dict, Image.Image, dict[str, float]]]:
    """Return split/mirror previews and normalized difference metrics."""
    gray = to_grayscale(image)
    width, height = gray.size
    mid_x = width // 2
    mid_y = height // 2
    left = gray.crop((0, 0, mid_x, height))
    right = gray.crop((width - mid_x, 0, width, height))
    top = gray.crop((0, 0, width, mid_y))
    bottom = gray.crop((0, height - mid_y, width, height))

    left_mirrored = ImageOps.mirror(left)
    right_mirrored = ImageOps.mirror(right)
    top_mirrored = ImageOps.flip(top)
    bottom_mirrored = ImageOps.flip(bottom)
    left_right_diff = ImageChops.difference(left_mirrored, right)
    top_bottom_diff = ImageChops.difference(top_mirrored, bottom)
    rotation_diff = ImageChops.difference(gray, gray.rotate(180))

    return [
        ("left_half", {}, left, {}),
        ("right_half", {}, right, {}),
        ("left_mirrored", {}, left_mirrored, {}),
        ("right_mirrored", {}, right_mirrored, {}),
        (
            "left_right_mirror_difference",
            {},
            left_right_diff,
            {"mirror_difference": normalized_difference(left_mirrored, right)},
        ),
        ("top_half", {}, top, {}),
        ("bottom_half", {}, bottom, {}),
        ("top_mirrored", {}, top_mirrored, {}),
        ("bottom_mirrored", {}, bottom_mirrored, {}),
        (
            "top_bottom_mirror_difference",
            {},
            top_bottom_diff,
            {"mirror_difference": normalized_difference(top_mirrored, bottom)},
        ),
        (
            "rotation_180_difference",
            {},
            rotation_diff,
            {"rotation_difference": normalized_difference(gray, gray.rotate(180))},
        ),
    ]


def normalized_difference(first: Image.Image, second: Image.Image) -> float:
    """Return mean absolute grayscale difference normalized to 0..1."""
    diff = ImageChops.difference(first.convert("L"), second.convert("L"))
    pixels = list(diff.getdata())
    if not pixels:
        return 0.0
    return round(sum(pixels) / (len(pixels) * 255), 8)
