from __future__ import annotations

from PIL import Image

from libreprimus.image_analysis.symmetry import symmetry_record


def test_vertical_symmetry_metric_detects_symmetric_image() -> None:
    image = Image.new("L", (4, 4), 255)
    for y in range(4):
        image.putpixel((0, y), 0)
        image.putpixel((3, y), 0)

    record = symmetry_record("synthetic", image)

    assert record["vertical_mirror_difference"] == 0
    assert record["solve_claim"] is False


def test_horizontal_and_180_metrics_are_deterministic() -> None:
    image = Image.new("L", (2, 2))
    image.putdata([0, 255, 128, 64])

    first = symmetry_record("synthetic", image)
    second = symmetry_record("synthetic", image)

    assert first["horizontal_mirror_difference"] == second["horizontal_mirror_difference"]
    assert first["rotational_180_difference"] == second["rotational_180_difference"]
