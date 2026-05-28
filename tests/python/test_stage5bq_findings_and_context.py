from test_stage5bq_common import load_yaml


def test_stage5bq_findings_preserve_accept_with_warnings() -> None:
    payload = load_yaml("data/project-state/stage5bq-stage5bp-findings-integration.yaml")

    assert payload["stage5bp_verdict"] == "accept_with_warnings"
    assert "errata_classification_coarse_use_explicit_deltas" in payload["stage5bp_warnings"]
    assert payload["execution_selected"] is False


def test_stage5bq_string4_context_is_full_match_but_inactive() -> None:
    payload = load_yaml("data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml")

    assert payload["string4_branch_membership_status_after_errata"] == "full_branch_match"
    assert payload["string4_planning_context_status"] == "inactive_branch_context_only"
    assert payload["string4_active_input_allowed"] is False
    assert payload["string4_dry_run_ingestion_allowed_now"] is False
    assert payload["execution_allowed"] is False
