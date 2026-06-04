from __future__ import annotations

from test_stage5de_common import ensure_stage5de_built, load_yaml


def test_stage5de_does_not_create_real_approval_or_combined_gate() -> None:
    ensure_stage5de_built()
    summary = load_yaml("data/project-state/stage5de-summary.yaml")

    assert summary["real_operator_approval_record_created_now"] is False
    assert summary["real_operator_approval_record_present_now"] is False
    assert summary["real_approval_records_created"] is False
    assert summary["approval_gate_satisfied_now"] is False
    assert summary["combined_approval_gate_satisfied_now"] is False


def test_stage5de_keeps_activation_input_bytes_and_execution_blocked() -> None:
    ensure_stage5de_built()
    summary = load_yaml("data/project-state/stage5de-summary.yaml")

    assert summary["activation_decision_valid_now"] is False
    assert summary["activation_authorized_now"] is False
    assert summary["active_planning_input_selected_now"] is False
    assert summary["byte_stream_generation_authorized_now"] is False
    assert summary["execution_authorized_now"] is False
    assert summary["no_active_ingestion_status"] == "closed"
    assert summary["no_byte_stream_transition_gate_status"] == "closed"
    assert summary["no_execution_transition_gate_status"] == "closed"


def test_stage5de_real_record_boundary_blocks_real_records() -> None:
    ensure_stage5de_built()
    boundary = load_yaml("data/token-block/stage5de-real-record-creation-boundary.yaml")

    assert boundary["real_operator_approval_preparation_package_is_only_new_stage5de_package"] is True
    assert boundary["future_real_records_created_now"] is False
    assert boundary["blocked_real_record_class_count"] == 9
    assert all(record["created_now"] is False for record in boundary["blocked_real_record_classes"])
