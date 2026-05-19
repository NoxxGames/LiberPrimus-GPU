from __future__ import annotations

from libreprimus.source_lock_triage.visual_intake import build_visual_observations, count_by_family


def test_stage4b_cuneiform_observation_is_review_only() -> None:
    records = build_visual_observations()
    cuneiform = next(record for record in records if record["observation_family"] == "cuneiform_base60")

    assert cuneiform["review_status"] == "human_review_required"
    assert cuneiform["usable_as_experiment_seed"] is False
    assert cuneiform["trusted_as_canonical"] is False
    assert cuneiform["solve_claim"] is False
    assert cuneiform["derived_values"]["pair_55_1_base60"] == 3301


def test_stage4b_dot_13_31_observation_is_ambiguous_unforced() -> None:
    records = build_visual_observations()
    dot = next(record for record in records if record["observation_family"] == "dot_binary_ambiguity")

    assert "unforced" in dot["ambiguity_notes"].lower() or "ambiguous" in dot["ambiguity_notes"].lower()
    assert dot["usable_as_experiment_seed"] is False
    assert dot["false_positive_risk"] in {"high", "extreme"}


def test_stage4b_visual_family_counts() -> None:
    records = build_visual_observations()

    assert count_by_family(records, "cuneiform_base60") == 1
    assert count_by_family(records, "mirrored_three_dot_delimiter") == 2
    assert count_by_family(records, "dot_binary_ambiguity") == 1
