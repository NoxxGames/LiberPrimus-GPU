from __future__ import annotations

from pathlib import Path

import yaml


def _yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5ar_pixel_coordinate_records_are_bounded() -> None:
    payload = _yaml("data/token-block/stage5ar-token-pixel-coordinate-records.yaml")
    assert payload["coordinate_record_count"] == 256
    for record in payload["records"]:
        assert record["bbox_width"] > 0
        assert record["bbox_height"] > 0
        assert 0 <= record["bbox_x_min"] < record["bbox_x_max"] <= record["original_image_width"]
        assert 0 <= record["bbox_y_min"] < record["bbox_y_max"] <= record["original_image_height"]
        assert record["coordinate_source_class"] == "original_liber_primus_page_image"
