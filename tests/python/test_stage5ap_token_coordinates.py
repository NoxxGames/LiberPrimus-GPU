from __future__ import annotations

from libreprimus.token_block.coordinates import build_coordinate_records
from libreprimus.token_block.transcription import build_transcription


def test_stage5ap_coordinates_are_logical_not_pixel(tmp_path) -> None:
    transcription = tmp_path / "transcription.yaml"
    build_transcription(out=transcription)
    record = build_coordinate_records(transcription=transcription, out=tmp_path / "coordinates.yaml")
    assert record["coordinate_record_count"] == 256
    assert record["pixel_coordinates_available"] is False
    assert record["page_boundaries_final"] is False
    assert record["records"][0]["logical_coordinate"] == "r01c01"
    assert record["records"][-1]["logical_coordinate"] == "r32c08"
