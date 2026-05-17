from __future__ import annotations

from PIL import Image

from libreprimus.image_analysis.components import CONNECTIVITY, component_summary


def test_component_count_uses_documented_four_connected_rule() -> None:
    image = Image.new("L", (3, 3), 255)
    image.putpixel((0, 0), 0)
    image.putpixel((1, 1), 0)

    summary = component_summary(image, threshold=32)

    assert CONNECTIVITY == "4-connected"
    assert summary.connectivity == "4-connected"
    assert summary.component_count == 2
    assert summary.largest_components[0]["area"] == 1
