from __future__ import annotations

from libreprimus.token_block.stage5di import (
    validate_stage5di,
    validate_stage5di_governance_scope,
    validate_stage5di_sidecar_gates,
)

from test_stage5di_common import ensure_stage5di_built, load_yaml


def test_stage5di_combined_gate_activation_bytes_and_execution_stay_closed() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di()

    assert errors == []
    assert counts["combined_approval_gate_satisfied_now"] is False
    assert counts["activation_authorized_now"] is False
    assert counts["byte_stream_generation_authorized_now"] is False
    assert counts["execution_authorized_now"] is False


def test_stage5di_sidecar_and_governance_gates_stay_closed() -> None:
    ensure_stage5di_built()
    sidecar_counts, sidecar_errors = validate_stage5di_sidecar_gates()
    governance_counts, governance_errors = validate_stage5di_governance_scope()

    assert sidecar_errors == []
    assert governance_errors == []
    assert sidecar_counts["no_active_ingestion_status"] == "closed"
    assert sidecar_counts["no_byte_stream_transition_gate_status"] == "closed"
    assert sidecar_counts["no_execution_transition_gate_status"] == "closed"
    assert governance_counts["guardrail_status"] == "closed"


def test_stage5di_summary_records_no_target_validation_tor_or_solve_claim() -> None:
    ensure_stage5di_built()
    payload = load_yaml("data/project-state/stage5di-summary.yaml")

    assert payload["target_class_validation_implemented"] is False
    assert payload["tor_network_access_performed"] is False
    assert payload["solve_claim"] is False
    assert payload["parallel_worker_cap_for_stage5di_and_later"] == 8
