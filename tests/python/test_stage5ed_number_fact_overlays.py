from __future__ import annotations

from test_stage5ed_common import ensure_stage5ed_built, load_yaml


def test_stage5ed_overlay_collection_has_expected_disk_visual_method_cards() -> None:
    ensure_stage5ed_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5ed-review-batch-004-disk-visual-method-overlays.yaml"
    )
    labels = {overlay["display_label"] for overlay in collection["overlays"]}
    ids = {overlay["overlay_id"] for overlay in collection["overlays"]}

    assert collection["overlay_count"] == 25
    assert "stage5ed_disk_alberti_model_components_overlay" in ids
    assert "stage5ed_disk_doublet_suppression_448_89_overlay" in ids
    assert "stage5ed_solved_magic_square_1033_overlay" in ids
    assert "stage5ed_page56_hash_contract_128_64_512_overlay" in ids
    assert "stage5ed_visual_method_cluster_summary_overlay" in ids
    assert any("DiskCipher candidate has 8 claimed model components" in label for label in labels)
    assert any("expected 448 doublets to observed 89" in label for label in labels)
    assert any("magic constant 1033" in label for label in labels)


def test_stage5ed_overlays_are_not_decision_or_execution_seeds() -> None:
    ensure_stage5ed_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5ed-review-batch-004-disk-visual-method-overlays.yaml"
    )

    for overlay in collection["overlays"]:
        assert overlay["review_state"] == "overlay_enriched_fact"
        assert overlay["usable_for_decision_now"] is False
        assert {"proof", "route_seed", "execution_seed", "solve_claim"} <= set(overlay["not_allowed_as"])
        assert overlay["risk_notes"]
