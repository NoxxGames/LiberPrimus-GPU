from test_stage5bs_common import load_yaml


def test_stage5bs_integrates_stage5br_accept_with_warnings() -> None:
    findings = load_yaml("data/project-state/stage5bs-stage5br-findings-integration.yaml")
    summary = load_yaml("data/project-state/stage5bs-summary.yaml")

    assert findings["stage5br_verdict"] == "accept_with_warnings"
    assert summary["stage5br_findings_integrated"] is True
    assert summary["stage5br_verdict"] == "accept_with_warnings"


def test_stage5bs_planning_ingestion_gate_is_closed() -> None:
    gate = load_yaml("data/token-block/stage5bs-string4-planning-ingestion-gate.yaml")

    assert gate["string4_branch_membership_status_after_errata"] == "full_branch_match"
    assert gate["string4_planning_context_status"] == "inactive_branch_context_only"
    assert gate["string4_planning_ingestion_gate_status"] == "closed_gate_no_active_ingestion"
    assert gate["string4_active_input_allowed"] is False
    assert gate["string4_dry_run_ingestion_allowed_now"] is False
    assert gate["string4_execution_input_allowed"] is False


def test_stage5bs_future_runner_citation_policy_fails_closed() -> None:
    policy = load_yaml("data/token-block/stage5bs-future-runner-citation-policy.yaml")

    assert policy["future_runner_citation_status"] == "citation_required_fail_closed"
    assert "data/token-block/stage5bs-string4-planning-ingestion-gate.yaml" in policy["future_runner_must_cite"]
    assert "citation_missing" in policy["fail_closed_if"]
    assert "active_ingestion_authorization_missing" in policy["fail_closed_if"]
