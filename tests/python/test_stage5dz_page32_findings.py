from __future__ import annotations

from libreprimus.token_block.stage5dz import PAGE32_PATHS, PRIME_INDICES, ROUTE_VALUES
from test_stage5dz_common import ensure_stage5dz_built, load_yaml


def test_stage5dz_page32_findings_exact_values() -> None:
    ensure_stage5dz_built()

    route = load_yaml(PAGE32_PATHS["page32_red_header_anchored_3299_to_2472_route_candidate"])
    fold = load_yaml(PAGE32_PATHS["page32_full16_mobius_fold_candidate"])
    negative = load_yaml(PAGE32_PATHS["page32_direct_extraction_negative_result_review"])
    naming = load_yaml(PAGE32_PATHS["page32_grid_vs_tree_polar_naming_clarification"])

    assert route["red_header_cumulative_index_total"] == 463
    assert route["prime_463_one_indexed"] == 3299
    assert route["red_header_progressive_gp_sum"] == 2472
    assert route["route_segment_values"] == ROUTE_VALUES
    assert route["route_segment_prime_indices"] == PRIME_INDICES
    assert len(route["route_segment_values"]) == 12
    assert fold["front_side_candidate"] == ROUTE_VALUES
    assert fold["back_side_or_fold_candidate"] == [1820, 708, 1206, 4516]
    assert len(fold["full_spiral_sequence"]) == 16
    assert negative["result"] == "no_validated_plaintext_found"
    assert "not_a_disproof" in negative["important_warning"]
    assert len(naming["surfaces"]) == 2
    assert naming["future_records_should_use_explicit_surface_id"] is True
