from __future__ import annotations

from test_stage5ec_common import ensure_stage5ec_built, load_yaml


def test_stage5ec_overlay_collection_has_expected_triangle_page32_token_music_cards() -> None:
    ensure_stage5ec_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5ec-review-batch-003-triangle-page32-token-music-overlays.yaml"
    )
    labels = {overlay["display_label"] for overlay in collection["overlays"]}
    ids = {overlay["overlay_id"] for overlay in collection["overlays"]}

    assert collection["overlay_count"] == 25
    assert "stage5ec_pdd153_triangle_t17_center41_overlay" in ids
    assert "stage5ec_page32_grid_spiral_values_overlay" in ids
    assert "stage5ec_token_block_primary60_byte_surface_overlay" in ids
    assert "stage5ec_instar_205_prime205_1259_overlay" in ids
    assert "stage5ec_self_reference_529_square23_overlay" in ids
    assert any("PDD triangle body has 153 words" in label for label in labels)
    assert any("Page32 4x4 grid spiral starts 3299" in label for label in labels)
    assert any("Token-block primary60 surface is 32x8" in label for label in labels)


def test_stage5ec_overlays_are_not_decision_or_execution_seeds() -> None:
    ensure_stage5ec_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5ec-review-batch-003-triangle-page32-token-music-overlays.yaml"
    )

    for overlay in collection["overlays"]:
        assert overlay["review_state"] == "overlay_enriched_fact"
        assert overlay["usable_for_decision_now"] is False
        assert {"proof", "route_seed", "execution_seed", "solve_claim"} <= set(overlay["not_allowed_as"])
        assert overlay["risk_notes"]
