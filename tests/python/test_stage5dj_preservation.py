from __future__ import annotations

from libreprimus.token_block.stage5dj import (
    validate_stage5dj_active_lineage_preservation,
    validate_stage5dj_governance_scope,
    validate_stage5dj_sidecar_gates,
    validate_stage5dj_stage5bd_preservation,
    validate_stage5dj_stage5dg_preservation,
)

from test_stage5dj_common import ensure_stage5dj_built, load_yaml, write_temp_yaml


def test_stage5dj_preserves_operator_approval_without_opening_gate() -> None:
    ensure_stage5dj_built()

    counts, errors = validate_stage5dj_stage5dg_preservation()
    assert errors == []
    assert counts["stage5dg_operator_approval_record_preserved"] is True
    assert counts["operator_approval_component_satisfied_now"] is True
    assert counts["combined_approval_gate_satisfied_now"] is False


def test_stage5dj_preserves_stage5bd_and_active_lineage_counts() -> None:
    ensure_stage5dj_built()

    stage5bd_counts, stage5bd_errors = validate_stage5dj_stage5bd_preservation()
    lineage_counts, lineage_errors = validate_stage5dj_active_lineage_preservation()
    assert stage5bd_errors == []
    assert lineage_errors == []
    assert stage5bd_counts["stage5bd_run_plan_id_count"] == 10
    assert lineage_counts["active_lineage_record_count"] == 8


def test_stage5dj_sidecar_and_governance_gates_stay_closed() -> None:
    ensure_stage5dj_built()

    sidecar_counts, sidecar_errors = validate_stage5dj_sidecar_gates()
    governance_counts, governance_errors = validate_stage5dj_governance_scope()
    assert sidecar_errors == []
    assert governance_errors == []
    assert sidecar_counts["no_active_ingestion_status"] == "closed"
    assert sidecar_counts["no_byte_stream_transition_gate_status"] == "closed"
    assert sidecar_counts["no_execution_transition_gate_status"] == "closed"
    assert governance_counts["guardrail_status"] == "closed"


def test_stage5dj_governance_rejects_audio_stego(tmp_path) -> None:
    ensure_stage5dj_built()
    payload = load_yaml("data/project-state/stage5dj-governance-scope-control.yaml")
    payload["audio_stego_performed_now"] = True
    temp = write_temp_yaml(tmp_path / "bad.yaml", payload)

    _, errors = validate_stage5dj_governance_scope(governance=temp)
    assert any("audio_stego_performed_now" in error for error in errors)
