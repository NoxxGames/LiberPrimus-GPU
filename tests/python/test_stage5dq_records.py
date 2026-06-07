from __future__ import annotations

from test_stage5dq_common import ensure_stage5dq_built, load_yaml


def test_stage5dq_summary_and_guardrails() -> None:
    ensure_stage5dq_built()
    summary = load_yaml("data/project-state/stage5dq-summary.yaml")

    assert summary["stage_id"] == "stage-5dq"
    assert summary["status"] == "complete"
    assert summary["operator_console_shell_implemented_now"] is True
    assert summary["source_browser_component_implemented_now"] is True
    assert summary["source_browser_gui_implemented_now"] is True
    assert summary["source_browser_entries_loaded"] >= 1200
    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["active_lineage_record_count"] == 8
    assert summary["parallel_worker_cap"] == 8
    assert summary["pivot_target_selected_now"] is False
    assert summary["execution_performed"] is False
    assert summary["source_browser_runs_ocr"] is False
    assert summary["source_browser_runs_image_forensics"] is False
    assert summary["source_browser_executes_source_files"] is False
    assert summary["recommended_next_stage_id"] == "stage-5dr"


def test_stage5dq_scope_control_deferred_modules() -> None:
    ensure_stage5dq_built()
    scope = load_yaml("data/project-state/stage5dq-operator-console-scope-control.yaml")

    assert scope["scope"] == "operator_console_source_browser_v0_only"
    assert scope["committed_source_lock_records_read_only"] is True
    assert "operator_approval_records" in scope["future_modules_deferred"]
    assert scope["experiment_execution_ui_implemented_now"] is False
