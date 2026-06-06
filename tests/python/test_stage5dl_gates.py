from __future__ import annotations

from libreprimus.token_block import stage5dl
from test_stage5dl_common import ensure_stage5dl_built, load_yaml, write_temp_yaml


def test_stage5dl_summary_records_future_preference_without_selection() -> None:
    ensure_stage5dl_built()
    summary = load_yaml("data/project-state/stage5dl-summary.yaml")

    assert summary["operator_future_priority_preference_recorded"] is True
    assert summary["operator_preferred_future_target_family_id"] == (
        "pdd_153_triangle_word_prime_route_v1"
    )
    assert summary["selected_next_solve_target_id"] is None
    assert summary["pivot_target_selected_now"] is False
    assert summary["target_priority_decision_created_now"] is False
    assert summary["operator_target_priority_decision_created_now"] is False
    assert summary["recommended_next_stage_id"] == "stage-5dm"


def test_stage5dl_preserves_stage5dg_stage5bd_and_lineage() -> None:
    ensure_stage5dl_built()
    stage5dg = load_yaml("data/token-block/stage5dl-stage5dg-approval-preservation.yaml")
    stage5bd = load_yaml("data/token-block/stage5dl-stage5bd-plan-preservation.yaml")
    lineage = load_yaml("data/token-block/stage5dl-active-lineage-preservation.yaml")

    assert stage5dg["stage5dg_operator_approval_record_preserved"] is True
    assert stage5dg["operator_approval_component_satisfied_now"] is True
    assert stage5dg["deep_research_acceptance_present_now"] is False
    assert stage5dg["combined_approval_gate_satisfied_now"] is False
    assert stage5bd["stage5bd_run_plan_id_count"] == 10
    assert lineage["active_lineage_record_count"] == 8


def test_stage5dl_sidecar_gates_remain_closed() -> None:
    ensure_stage5dl_built()
    no_active = load_yaml("data/token-block/stage5dl-no-active-ingestion-proof.yaml")
    no_byte = load_yaml("data/token-block/stage5dl-no-byte-stream-transition-gate.yaml")
    no_execution = load_yaml("data/token-block/stage5dl-no-execution-transition-gate.yaml")

    assert no_active["active_planning_input_selected_now"] is False
    assert no_active["active_ingestion_authorized"] is False
    assert no_byte["byte_stream_generation_authorized"] is False
    assert no_byte["variant_byte_streams_generated"] is False
    assert no_execution["execution_authorized"] is False
    assert no_execution["execution_performed"] is False
    assert no_execution["route_extraction_performed_now"] is False


def test_stage5dl_aggregate_validator_rejects_target_selection(
    monkeypatch: object, tmp_path
) -> None:
    ensure_stage5dl_built()
    summary = load_yaml("data/project-state/stage5dl-summary.yaml")
    summary["selected_next_solve_target_id"] = "pdd_153_triangle_word_prime_route_v1"
    summary["pivot_target_selected_now"] = True
    path = write_temp_yaml(tmp_path / "stage5dl-summary.yaml", summary)

    monkeypatch.setitem(stage5dl.DATA_PATHS, "summary", path)

    result = stage5dl.validate_stage5dl_governance_scope()
    assert result.validation_error_count > 0


def test_stage5dl_no_codex_output_underscore_and_worker_cap() -> None:
    ensure_stage5dl_built()
    summary = load_yaml("data/project-state/stage5dl-summary.yaml")

    assert summary["canonical_codex_handoff_root"] == "codex-output"
    assert summary["codex_output_used"] is False
    assert summary["parallel_worker_cap_for_stage5dl_and_later"] == 8
