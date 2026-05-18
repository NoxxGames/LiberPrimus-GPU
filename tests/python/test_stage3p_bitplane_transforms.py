from __future__ import annotations

from PIL import Image

from libreprimus.image_transforms.bitplanes import bitplane_transform_images


def test_bitplane_transform_and_density_are_deterministic() -> None:
    image = Image.new("L", (2, 1))
    image.putdata([1, 2])

    records = {name: (output, metrics) for name, _, output, metrics in bitplane_transform_images(image)}

    assert list(records["bitplane_0"][0].getdata()) == [255, 0]
    assert records["bitplane_0"][1]["one_ratio"] == 0.5
    assert list(records["bitplane_1"][0].getdata()) == [0, 255]
    assert records["bitplane_1"][1]["one_ratio"] == 0.5
