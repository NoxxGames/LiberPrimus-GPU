from __future__ import annotations

from PIL import Image

from libreprimus.image_transforms.split_mirror import split_mirror_transform_images


def test_vertical_and_horizontal_split_mirror_detect_asymmetry() -> None:
    image = Image.new("L", (4, 4), 255)
    for y in range(4):
        image.putpixel((0, y), 0)
    for x in range(4):
        image.putpixel((x, 0), 0)

    metrics = {}
    for name, _, _, record_metrics in split_mirror_transform_images(image):
        metrics.update({f"{name}_{key}": value for key, value in record_metrics.items()})

    assert metrics["left_right_mirror_difference_mirror_difference"] > 0.3
    assert metrics["top_bottom_mirror_difference_mirror_difference"] > 0.3
    assert metrics["rotation_180_difference_rotation_difference"] >= 0.0
