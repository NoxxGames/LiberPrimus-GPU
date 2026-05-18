from __future__ import annotations

from PIL import Image

from libreprimus.image_transforms.edges import difference_edge_map


def test_simple_edge_map_is_deterministic() -> None:
    image = Image.new("L", (2, 2))
    image.putdata([0, 255, 0, 255])

    edge, metrics = difference_edge_map(image)

    assert list(edge.getdata()) == [0, 255, 0, 255]
    assert metrics["edge_density_ratio"] == 0.5
