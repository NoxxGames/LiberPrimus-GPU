from __future__ import annotations

from libreprimus.bounded_numeric.visual_negative_controls import (
    audit_dot_ambiguity,
    audit_visual_negative_controls,
)


def test_stage4d_dot_claimed_reading_uniqueness_false_with_multiple_readings() -> None:
    records = audit_dot_ambiguity(
        {"manifest_id": "exp_stage4b_dot_ambiguity_audit_v1", "candidate_count_upper_bound": 140},
        [
            {
                "task_id": "dot",
                "possible_readings": ["13", "31", "7"],
                "claimed_readings": ["13", "31"],
                "ordering_policy": "unknown_pending_annotation",
                "polarity_policy": "unknown_pending_annotation",
            }
        ],
    )

    assert records[0]["claimed_reading_uniqueness"] is False
    assert records[0]["solve_claim"] is False


def test_stage4d_visual_negative_control_ambiguity_metrics_generated() -> None:
    records = audit_visual_negative_controls(
        {
            "manifest_id": "exp_stage4b_visual_negative_controls_v1",
            "candidate_count_upper_bound": 60,
        },
        [
            {
                "task_id": "braille",
                "false_positive_class": "braille_dot_readings",
                "why_dangerous": "too many readings",
                "required_null_control": "visual nulls",
            }
        ],
    )

    assert records[0]["possible_reading_count"] == 64
    assert records[0]["polarity_orientation_dependent"] is True
    assert records[0]["solve_claim"] is False
