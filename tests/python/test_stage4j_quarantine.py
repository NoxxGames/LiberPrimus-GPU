from __future__ import annotations

from libreprimus.observation_review.quarantine import build_quarantine_record


def test_stage4j_negative_control_can_be_used_as_control_not_truth() -> None:
    record = build_quarantine_record(_decision("negative_control", "negative_control"))
    assert record is not None
    assert record["allowed_control_use"] is True
    assert record["truth_acceptance"] is False
    assert record["usable_as_experiment_seed"] is False


def test_stage4j_quarantine_record_includes_why_dangerous() -> None:
    record = build_quarantine_record(
        {
            **_decision("visual_dot_pattern_candidate", "quarantined"),
            "rationale": "forced 13/31 dot reading",
        }
    )
    assert record is not None
    assert record["false_positive_class"] == "forced_13_31_readings"
    assert "13/31" in record["why_dangerous"]


def _decision(observation_type: str, state: str) -> dict:
    return {
        "review_decision_id": "decision-1",
        "observation_id": "obs-1",
        "source_family": "test",
        "observation_type": observation_type,
        "review_state": state,
        "promotion_blocked_reasons": [],
        "false_positive_class": None,
        "rationale": "",
        "solve_claim": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
    }
