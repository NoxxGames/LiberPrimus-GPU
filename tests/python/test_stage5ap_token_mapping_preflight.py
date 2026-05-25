from __future__ import annotations

from libreprimus.token_block.alphabets import build_alphabet_registry
from libreprimus.token_block.mapping import build_mapping_preflight, token_to_value, validate_mapping_preflight
from libreprimus.token_block.transcription import build_transcription


def test_stage5ap_primary60_mapping_preflight_bounds_and_known_values(tmp_path) -> None:
    transcription = tmp_path / "transcription.yaml"
    alphabet = tmp_path / "alphabet.yaml"
    build_transcription(out=transcription)
    build_alphabet_registry(transcription=transcription, out=alphabet)
    record = build_mapping_preflight(transcription=transcription, alphabet_registry=alphabet, out=tmp_path / "mapping.yaml")
    assert token_to_value("00") == 0
    assert token_to_value("4F") == 255
    assert record["value_min"] == 0
    assert record["value_max"] == 255
    assert record["all_values_in_byte_range"] is True
    assert record["decode_attempted"] is False
    assert validate_mapping_preflight(record) == []
