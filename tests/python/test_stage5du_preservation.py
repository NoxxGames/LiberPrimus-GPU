from __future__ import annotations

from libreprimus.token_block.stage5du import FORBIDDEN_FALSE_FLAGS
from test_stage5du_common import ensure_stage5du_built, load_yaml


def test_stage5du_summary_preserves_prior_stage_and_closed_gates() -> None:
    ensure_stage5du_built()
    summary = load_yaml("data/project-state/stage5du-summary.yaml")
    assert summary["status"] == "complete"
    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["active_lineage_record_count"] == 8
    assert summary["parallel_worker_cap"] == 8
    assert summary["recommended_next_stage_id"] == "stage-5dv"
    assert summary["number_fact_review_batch_1_still_required_after_this_stage"] is True

    for flag in FORBIDDEN_FALSE_FLAGS:
        assert summary[flag] is False


def test_stage5du_stage5dt_review_batch_remains_pending() -> None:
    ensure_stage5du_built()
    preservation = load_yaml("data/project-state/stage5du-stage5dt-preservation.yaml")
    decision = load_yaml("data/project-state/stage5du-next-stage-decision.yaml")
    assert preservation["source_lock_entry_batch_review_performed_now"] is False
    assert preservation["number_fact_backfill_performed_now"] is False
    assert decision["recommended_next_stage_id"] == "stage-5dv"
    assert decision["selected_next_stage_authorizes_execution"] is False
