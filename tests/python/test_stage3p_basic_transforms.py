from __future__ import annotations

from PIL import Image

from libreprimus.image_transforms.basic_transforms import basic_transform_images


def test_basic_grayscale_invert_and_threshold_transforms_are_deterministic() -> None:
    image = Image.new("RGB", (2, 2))
    image.putdata([(0, 0, 0), (255, 255, 255), (96, 96, 96), (200, 200, 200)])

    transforms = {name: output for name, _, output in basic_transform_images(image)}

    assert list(transforms["grayscale"].getdata()) == [0, 255, 96, 200]
    assert list(transforms["invert"].getdata()) == [255, 0, 159, 55]
    assert list(transforms["threshold_128"].getdata()) == [0, 255, 0, 255]
    assert transforms["posterize_2bit"].mode == "L"
