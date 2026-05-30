from pathlib import Path

import yaml

from libreprimus.token_block.stage5cc import (
    validate_stage5cc_active_planning_input_preflight,
    validate_stage5cc_no_byte_stream_transition_gate,
    validate_stage5cc_no_execution_transition_gate,
    validate_stage5cc_sidecar_gates,
)
from test_stage5cc_common import load_yaml


def test_stage5cc_summary_identity_and_blocked_status() -> None:
    summary = load_yaml("data/project-state/stage5cc-summary.yaml")
    assert summary["stage_id"] == "stage-5cc"
    assert summary["stage5cb_verdict"] == "accept_with_warnings"
    assert summary["active_planning_input_authorized_now"] is False
    assert summary["no_byte_stream_transition_gate_status"] == "closed"
    assert summary["no_execution_transition_gate_status"] == "closed"
    assert summary["future_token_block_execution_remains_blocked"] is True


def test_stage5cc_active_planning_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-active-planning-input-proposal-preflight.yaml")
    payload["active_planning_input_authorized_now"] = True
    candidate = tmp_path / "preflight.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_active_planning_input_preflight(preflight=candidate)
    assert counts["stage5cc_active_planning_input_preflight_valid"] is False
    assert "active_planning_input_authorized_now must be false" in errors


def test_stage5cc_byte_stream_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-no-byte-stream-transition-gate.yaml")
    payload["real_byte_stream_generated"] = True
    candidate = tmp_path / "byte_gate.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_no_byte_stream_transition_gate(gate=candidate)
    assert counts["stage5cc_no_byte_stream_transition_gate_valid"] is False
    assert "real_byte_stream_generated must be false" in errors


def test_stage5cc_execution_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-no-execution-transition-gate.yaml")
    payload["cuda_execution_performed"] = True
    candidate = tmp_path / "execution_gate.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_no_execution_transition_gate(gate=candidate)
    assert counts["stage5cc_no_execution_transition_gate_valid"] is False
    assert "cuda_execution_performed must be false" in errors


def test_stage5cc_stage5bd_count_changed_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-stage5bd-plan-preservation.yaml")
    payload["stage5bd_run_plan_id_count"] = 11
    candidate = tmp_path / "stage5bd.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_sidecar_gates(stage5bd_preservation=candidate)
    assert counts["stage5cc_sidecar_gates_valid"] is False
    assert "Stage 5BD run-plan count must remain 10" in errors


def test_stage5cc_deprecated_stage5aw_path_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-active-lineage-preservation.yaml")
    payload["preserved_active_record_paths"][1] = (
        "data/token-block/stage5aw-repaired-branch-manifest.yaml"
    )
    candidate = tmp_path / "active_lineage.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_sidecar_gates(active_lineage=candidate)
    assert counts["stage5cc_sidecar_gates_valid"] is False
    assert "deprecated_stage5aw_path_present" in errors


def test_stage5cc_codex_output_usage_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/source-harvester/stage5cc-codex-handoff-policy.yaml")
    payload["codex_output_used"] = True
    candidate = tmp_path / "handoff.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_sidecar_gates(handoff=candidate)
    assert counts["stage5cc_sidecar_gates_valid"] is False
    assert "codex_output_used must be false" in errors


def test_stage5cc_dwh_quarantine_and_lineage_preserved() -> None:
    dwh = load_yaml("data/historical-route/stage5cc-dwh-quarantine-reaffirmation.yaml")
    lineage = load_yaml("data/token-block/stage5cc-active-lineage-preservation.yaml")
    assert dwh["dwh_quarantine_status"] == "reaffirmed_active"
    assert lineage["active_lineage_record_count"] == 8
    assert lineage["deprecated_stage5aw_path_included"] is False
