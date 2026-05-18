from __future__ import annotations

from PIL import Image

from libreprimus.image_transforms.channel_transforms import channel_transform_images


def test_rgb_channel_split_works_on_synthetic_image() -> None:
    image = Image.new("RGB", (1, 1), (10, 20, 30))

    transforms, warnings = channel_transform_images(image)
    outputs = {name: output for name, _, output in transforms}

    assert warnings == []
    assert outputs["red_channel"].getpixel((0, 0)) == 10
    assert outputs["green_channel"].getpixel((0, 0)) == 20
    assert outputs["blue_channel"].getpixel((0, 0)) == 30


def test_non_rgb_channel_split_warns_without_failure() -> None:
    transforms, warnings = channel_transform_images(Image.new("L", (1, 1), 128))

    assert transforms == []
    assert warnings == ["channel_split_skipped_mode_L"]
