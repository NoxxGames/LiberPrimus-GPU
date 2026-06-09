from __future__ import annotations

from test_stage5du_common import ensure_stage5du_built, load_yaml


FAMILY_PATHS = [
    "data/historical-route/stage5du-red-runes-gateless-gate-koan20-title-candidate-v0.yaml",
    "data/historical-route/stage5du-big-gap-vertical-phase-shift-candidate-v0.yaml",
    "data/historical-route/stage5du-star-artifacts-exact254-mask-method-v0.yaml",
    "data/historical-route/stage5du-page15-your-truth-crib-pointer-candidate-v0.yaml",
    "data/historical-route/stage5du-page54-55-a-postlude-red-heading-candidate-v1.yaml",
    "data/historical-route/stage5du-mobius-totient-zero-class-gp-alphabet-candidate-v0.yaml",
]


def test_stage5du_candidate_families_remain_review_only() -> None:
    ensure_stage5du_built()
    for path in FAMILY_PATHS:
        record = load_yaml(path)
        assert record["metadata_only"] is True
        assert record["selected_now"] is False
        assert record["usable_as_experiment_seed_now"] is False
        assert record["usable_for_target_priority_now"] is False
        assert record["route_extraction_performed_now"] is False
        assert record["solve_claim"] is False


def test_stage5du_red_runes_candidate_keeps_selection_bias_controls() -> None:
    ensure_stage5du_built()
    record = load_yaml(
        "data/historical-route/stage5du-red-runes-gateless-gate-koan20-title-candidate-v0.yaml"
    )
    assert record["target_title"] == "THE ENLIGHTENED MAN"
    assert record["grouping_match_2_11_3"] is True
    assert record["red_rune_transcription_verification_required"] is True
    assert "selection-bias review" in record["control_requirements"]


def test_stage5du_star_artifact_candidate_blocks_image_forensics() -> None:
    ensure_stage5du_built()
    record = load_yaml("data/historical-route/stage5du-star-artifacts-exact254-mask-method-v0.yaml")
    assert record["semantic_image_interpretation_performed"] is False
    assert record["image_forensics_performed"] is False
    assert record["usable_for_target_priority_now"] is False
