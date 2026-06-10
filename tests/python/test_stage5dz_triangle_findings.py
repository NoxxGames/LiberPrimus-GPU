from __future__ import annotations

from libreprimus.token_block.stage5dz import TRIANGLE_PATHS
from test_stage5dz_common import ensure_stage5dz_built, load_yaml


def test_stage5dz_triangle_findings_exact_values() -> None:
    ensure_stage5dz_built()

    heading = load_yaml(TRIANGLE_PATHS["pdd153_heading_transcription_canonicalization_warning"])
    way = load_yaml(TRIANGLE_PATHS["pdd153_way_anchor_ordinal_arithmetic_review"])
    bridge = load_yaml(TRIANGLE_PATHS["pdd153_56311_center_word52_way_bridge_review"])
    ouro = load_yaml(TRIANGLE_PATHS["pdd153_ouroboric_route_surface_interpretation"])
    negative = load_yaml(TRIANGLE_PATHS["pdd153_direct_decode_negative_result_review"])

    assert heading["historical_records_rewritten_now"] is False
    assert heading["working_heading_ordinal_values"] == [13, 23, 2]
    assert way["heading_ordinal_values"] == [13, 23, 2]
    assert way["word52_reversed_ordinal_values"] == [6, 28, 5]
    assert way["operation_values"] == ["13 - 6 mod 29 = 7", "23 - 28 mod 29 = 24", "2 - 5 mod 29 = 26"]
    assert way["result_ordinal_values"] == [7, 24, 26]
    assert way["result_latin"] == "WAY"
    assert bridge["triangle_center_word_index"] == 41
    assert bridge["word52_reached_from_center"] is True
    assert bridge["positions_from_center"] == [46, 52, 55, 66]
    assert ouro["sequence_sum"] == 25
    assert ouro["modulus"] == 153
    assert ouro["gcd_25_153"] == 1
    assert ouro["closed_state_period"] == 612
    assert negative["result"] == "no_validated_plaintext_found"
    assert "not_a_disproof" in negative["important_warning"]
