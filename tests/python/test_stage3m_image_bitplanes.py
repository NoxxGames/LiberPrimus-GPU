from __future__ import annotations

from PIL import Image

from libreprimus.image_analysis.bitplanes import bitplane_records


def test_bitplane_one_ratio_is_deterministic() -> None:
    image = Image.new("L", (2, 1))
    image.putdata([0b00000001, 0b00000011])

    records = bitplane_records("synthetic", image)

    assert records[0]["one_ratio"] == 1.0
    assert records[1]["one_ratio"] == 0.5
    assert records[7]["one_ratio"] == 0.0
    assert all(record["solve_claim"] is False for record in records)
