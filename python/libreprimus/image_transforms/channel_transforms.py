"""Channel split transforms."""

from __future__ import annotations

from PIL import Image


def channel_transform_images(image: Image.Image) -> tuple[list[tuple[str, dict, Image.Image]], list[str]]:
    """Return RGB/RGBA channel previews or warnings for non-RGB images."""
    if image.mode not in {"RGB", "RGBA"}:
        return [], [f"channel_split_skipped_mode_{image.mode}"]
    rgba = image.convert("RGBA")
    red, green, blue, alpha = rgba.split()
    transforms: list[tuple[str, dict, Image.Image]] = [
        ("red_channel", {"channel": "red"}, red),
        ("green_channel", {"channel": "green"}, green),
        ("blue_channel", {"channel": "blue"}, blue),
    ]
    if image.mode == "RGBA" or alpha.getextrema() != (255, 255):
        transforms.append(("alpha_channel", {"channel": "alpha"}, alpha))
    return transforms, []
