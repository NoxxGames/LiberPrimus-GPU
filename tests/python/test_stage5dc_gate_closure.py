from __future__ import annotations

from test_stage5dc_common import ensure_stage5dc_built, load_yaml


def test_stage5dc_does_not_create_approval_acceptance_or_gate_records() -> None:
    ensure_stage5dc_built()
    summary = load_yaml("data/project-state/stage5dc-summary.yaml")

    assert summary["real_operator_approval_record_created_now"] is False
    assert summary["real_deep_research_acceptance_record_created_now"] is False
    assert summary["real_combined_gate_validation_record_created_now"] is False
    assert summary["combined_approval_gate_satisfied_now"] is False
    assert summary["approval_gate_satisfied_now"] is False


def test_stage5dc_keeps_activation_input_bytes_and_execution_blocked() -> None:
    ensure_stage5dc_built()
    summary = load_yaml("data/project-state/stage5dc-summary.yaml")

    assert summary["activation_decision_valid_now"] is False
    assert summary["activation_authorized_now"] is False
    assert summary["active_planning_input_selected_now"] is False
    assert summary["byte_stream_generation_authorized_now"] is False
    assert summary["execution_authorized_now"] is False
    assert summary["no_active_ingestion_status"] == "closed"
    assert summary["no_byte_stream_transition_gate_status"] == "closed"
    assert summary["no_execution_transition_gate_status"] == "closed"
