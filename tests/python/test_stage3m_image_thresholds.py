from __future__ import annotations

from PIL import Image

from libreprimus.image_analysis.thresholds import threshold_and_component_records


def test_threshold_foreground_ratios_are_deterministic() -> None:
    image = Image.new("L", (2, 2))
    image.putdata([0, 64, 128, 255])

    threshold_records, _ = threshold_and_component_records("synthetic", image, thresholds=(64,))

    record = threshold_records[0]
    assert record["threshold"] == 64
    assert record["foreground_ratio"] == 0.5
    assert record["background_ratio"] == 0.5
    assert record["trusted_as_canonical"] is False
    assert record["solve_claim"] is False
