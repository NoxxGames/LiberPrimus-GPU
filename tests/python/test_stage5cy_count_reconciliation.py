from test_stage5cy_common import ensure_stage5cy_built, load_yaml


def test_stage5cy_reconciles_stage5cw_pytest_count_warning_without_opening_gate() -> None:
    ensure_stage5cy_built()
    reconciliation = load_yaml("data/project-state/stage5cy-validation-count-reconciliation.yaml")

    assert reconciliation["stage5cw_committed_compact_pytest_count"] == 2446
    assert reconciliation["stage5cw_committed_compact_pytest_count_from_record"] == 2446
    assert reconciliation["stage5cw_final_issue_completion_trail_pytest_count"] == 2466
    assert reconciliation["reconciliation_status"] == "superseding_reconciliation_record"
    assert reconciliation["count_mismatch_class"] == "reviewability_count_reconciliation_warning"
    assert reconciliation["gate_opening"] is False
    assert reconciliation["activation_defect"] is False
    assert reconciliation["history_rewritten"] is False
    assert reconciliation["historical_stage5cw_metadata_changed"] is False
