from __future__ import annotations

from test_stage5dt_common import ensure_stage5dt_built, load_yaml


def test_stage5dt_preserves_prior_stage_counts_and_guardrails() -> None:
    ensure_stage5dt_built()
    summary = load_yaml("data/project-state/stage5dt-summary.yaml")
    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["active_lineage_record_count"] == 8
    assert summary["historical_source_lock_records_rewritten"] is False
    assert summary["number_fact_backfill_performed_now"] is False
    assert summary["pivot_target_selected_now"] is False
    assert summary["execution_performed"] is False
    assert summary["solve_claim"] is False
