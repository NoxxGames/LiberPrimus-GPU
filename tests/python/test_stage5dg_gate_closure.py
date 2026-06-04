from __future__ import annotations

from libreprimus.token_block.stage5dg import (
    validate_stage5dg_combined_gate,
    validate_stage5dg_deep_research_absence,
    validate_stage5dg_real_record_boundary,
    validate_stage5dg_sidecar_gates,
)

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_combined_gate_remains_unsatisfied() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_combined_gate()

    assert errors == []
    assert counts["operator_approval_component_satisfied_now"] is True
    assert counts["deep_research_acceptance_component_satisfied_now"] is False
    assert counts["combined_approval_gate_satisfied_now"] is False


def test_stage5dg_real_record_boundary_and_sidecar_gates() -> None:
    ensure_stage5dg_built()
    boundary_counts, boundary_errors = validate_stage5dg_real_record_boundary()
    sidecar_counts, sidecar_errors = validate_stage5dg_sidecar_gates()
    absence_counts, absence_errors = validate_stage5dg_deep_research_absence()

    assert boundary_errors == []
    assert sidecar_errors == []
    assert absence_errors == []
    assert boundary_counts["created_real_record_class_count"] == 1
    assert sidecar_counts["no_byte_stream_transition_gate_status"] == "closed"
    assert absence_counts["real_deep_research_acceptance_record_present_now"] is False

    payload = load_yaml("data/token-block/stage5dg-real-record-creation-boundary.yaml")
    created = [item for item in payload["real_record_classes"] if item["created_now"]]
    assert [item["record_class"] for item in created] == ["real_operator_approval_record"]
