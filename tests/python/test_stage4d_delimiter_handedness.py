from __future__ import annotations

from libreprimus.bounded_numeric.delimiter_handedness import audit_delimiter_handedness


def test_stage4d_delimiter_audit_does_not_infer_reset_meaning() -> None:
    records = audit_delimiter_handedness(
        {
            "manifest_id": "exp_stage4b_delimiter_handedness_v1",
            "candidate_count_upper_bound": 16,
        },
        [
            {
                "task_id": "delimiter",
                "delimiter_type": "mirrored_three_dot_variant",
                "orientation": "unknown_pending_annotation",
                "handedness": "unknown_pending_annotation",
                "coordinate_system": "unknown_pending_annotation",
                "annotation_status": "needs_human_coordinates",
            }
        ],
    )

    assert records[0]["reset_boundary_hypothesis"] is False
    assert records[0]["meaning_inferred"] is False
    assert records[0]["unresolved_coordinates"] is True
