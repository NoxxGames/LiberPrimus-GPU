from __future__ import annotations

from libreprimus.token_block.stage5dz import EXPECTED_OVERLAY_COUNT, OPERATOR_CONSOLE_PATHS
from test_stage5dz_common import ensure_stage5dz_built, load_yaml


def test_stage5dz_overlay_collection_is_review_only() -> None:
    ensure_stage5dz_built()

    collection = load_yaml(OPERATOR_CONSOLE_PATHS["number_fact_overlays"])
    overlays = collection["overlays"]
    overlay_ids = {overlay["overlay_id"] for overlay in overlays}

    assert collection["overlay_count"] == EXPECTED_OVERLAY_COUNT
    assert len(overlays) == EXPECTED_OVERLAY_COUNT
    assert collection["overlay_only_fact_cards_supported"] is True
    assert collection["number_fact_review_batch_3_performed_now"] is False
    assert "stage5dz_pdd153_way_anchor_mod29_overlay" in overlay_ids
    assert "stage5dz_page32_red_header_start_stop_overlay" in overlay_ids
    for overlay in overlays:
        assert overlay["usable_for_decision_now"] is False
        assert {"proof", "route_seed", "execution_seed", "solve_claim"}.issubset(overlay["not_allowed_as"])
