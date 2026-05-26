from __future__ import annotations

from libreprimus.token_block.stage5av import classify_primary60_token


def test_stage5av_primary60_classifier_preserves_unmappable_reasons() -> None:
    assert classify_primary60_token("00")["primary60_value"] == 0
    assert classify_primary60_token("4F")["primary60_value"] == 255
    assert classify_primary60_token("Z1")["primary60_error"] == "first_symbol_not_in_0_to_4"
    assert classify_primary60_token("1!")["primary60_error"] == "suffix_not_in_primary_60_alphabet"
    assert classify_primary60_token("123")["primary60_error"] == "token_length_not_2"
