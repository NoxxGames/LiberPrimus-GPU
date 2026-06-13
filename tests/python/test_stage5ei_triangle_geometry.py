from __future__ import annotations

from test_stage5ei_common import stage5ei_data


def test_stage5ei_records_exact_t17_geometry() -> None:
    payload = stage5ei_data("pdd153_geometry_candidates")
    anchors = {anchor["position"]: anchor for anchor in payload["anchor_coordinates"]}

    assert payload["position_formula"] == "position n = T(r-1) + c"
    assert payload["diagonal_formula"] == "d = r - c + 1"
    assert payload["path_56311_positions"] == [41, 46, 52, 55, 66]
    assert payload["path_56311_cumulative_offsets"] == [5, 11, 14, 25]
    assert payload["d4_diagonal_positions"] == [7, 12, 18, 25, 33, 42, 52, 63, 75, 88, 102, 117, 133, 150]
    assert anchors[41]["row"] == 9
    assert anchors[41]["column"] == 5
    assert anchors[52]["d"] == 4
    assert anchors[106]["line_family"] == "left_edge"


def test_stage5ei_records_22_vs_24_taxonomy_ambiguity() -> None:
    payload = stage5ei_data("triangular_transposition_taxonomy")

    assert payload["operator_supplied_claim_22_distinct_triangular_transpositions"] is True
    assert payload["claim_22_distinct_transpositions_verified_now"] is False
    assert payload["natural_triangular_readout_family_count_observed_by_assistant"] == 24
    assert payload["transposition_count_taxonomy_ambiguous"] is True
    assert payload["route_stream_generated_now"] is False


def test_stage5ei_records_bottom_row_quarantine_bridge() -> None:
    payload = stage5ei_data("bottom_row_page32_quarantine_bridge")

    assert payload["pdd153_bottom_row_sum"] == 2465
    assert payload["pdd153_bottom_row_sum_factorization_or_relation"] == "85 * 29"
    assert payload["wynn_w_zero_based_index"] == 7
    assert payload["page32_bridge_value"] == 2472
    assert payload["expression"] == "2465 + 7 = 2472"
    assert payload["quarantine_bridge"] is True
    assert payload["not_route_evidence_now"] is True

