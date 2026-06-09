from __future__ import annotations

from libreprimus.token_block.stage5dv import FORBIDDEN_FALSE_FLAGS
from test_stage5dv_common import ensure_stage5dv_built, load_yaml


def test_stage5dv_summary_preserves_closed_scope_and_routes_to_stage5dw() -> None:
    ensure_stage5dv_built()
    summary = load_yaml("data/project-state/stage5dv-summary.yaml")
    assert summary["status"] == "complete"
    assert summary["recommended_next_stage_id"] == "stage-5dw"
    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["active_lineage_record_count"] == 8
    assert summary["parallel_worker_cap"] == 8
    assert summary["source_browser_path_canonicalization_repair_performed"] is True
    assert summary["number_fact_review_batch_1_performed_now"] is False
    assert summary["historical_source_lock_records_rewritten"] is False

    for flag in FORBIDDEN_FALSE_FLAGS:
        assert summary[flag] is False


def test_stage5dv_stage_preservation_records() -> None:
    ensure_stage5dv_built()
    stage5du = load_yaml("data/project-state/stage5dv-stage5du-preservation.yaml")
    stage5dt = load_yaml("data/project-state/stage5dv-stage5dt-preservation.yaml")
    stage5dg = load_yaml("data/token-block/stage5dv-stage5dg-preservation.yaml")
    stage5bd = load_yaml("data/token-block/stage5dv-stage5bd-preservation.yaml")
    active = load_yaml("data/token-block/stage5dv-active-lineage-preservation.yaml")

    assert stage5du["stage5du_status"] == "complete"
    assert stage5du["stage5du_candidate_records_created"] == 72
    assert stage5dt["stage5dt_complete"] is True
    assert stage5dt["number_fact_review_batch_1_performed_now"] is False
    assert stage5dg["stage5dg_operator_approval_record_preserved"] is True
    assert stage5dg["combined_approval_gate_satisfied_now"] is False
    assert stage5bd["stage5bd_run_plan_id_count"] == 10
    assert active["active_lineage_record_count"] == 8
