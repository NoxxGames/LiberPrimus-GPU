from __future__ import annotations

from libreprimus.token_block import stage5eg
from test_stage5eg_common import ensure_stage5eg_built, stage5eg_data


def test_daily_automation_outcome_is_truthful_and_report_only() -> None:
    ensure_stage5eg_built()

    result = stage5eg_data("automation_scheduling_result")
    setup = stage5eg_data("daily_automation_setup")

    assert result["automation_creation_attempted"] is True
    assert result["automation_created_or_updated"] is True
    assert result["manual_operator_setup_required"] is False
    assert result["automation_auto_commit_enabled"] is False
    assert result["automation_edits_allowed"] is False
    assert setup["report_only"] is True
    assert setup["execution_allowed"] is False


def test_stage5eg_routing_records_lag5_then_batch006() -> None:
    summary = stage5eg_data("summary")
    decision = stage5eg_data("next_stage_decision")

    assert summary["stage5ef_recommended_stage5eg_number_fact_batch_006"] is True
    assert summary["operator_inserted_doc_staleness_guardian_stage_before_lag5"] is True
    assert summary["lag5_source_lock_deferred_to_stage5eh"] is True
    assert summary["number_fact_review_batch_006_deferred_to_stage5ei"] is True
    assert decision["selected_next_stage_id"] == "stage-5eh"
    assert decision["normal_batch006_deferred_to_stage5ei"] is True


def test_stage5eg_guardrail_flags_remain_false() -> None:
    summary = stage5eg_data("summary")

    for key in stage5eg.FALSE_GUARDRAILS:
        assert summary[key] is False


def test_stage5eg_validators_pass() -> None:
    ensure_stage5eg_built()

    for validator in [
        stage5eg.validate_stage5eg_stage5ef_preservation,
        stage5eg.validate_stage5eg_stale_current_claim_scanner,
        stage5eg.validate_stage5eg_doc_policy_repair,
        stage5eg.validate_stage5eg_custom_agents,
        stage5eg.validate_stage5eg_hooks,
        stage5eg.validate_stage5eg_daily_automation,
        stage5eg.validate_stage5eg_source_browser_loadability,
        stage5eg.validate_stage5eg_sidecar_gates,
        stage5eg.validate_stage5eg_handoff_continuity,
        stage5eg.validate_stage5eg_credential_redaction_policy,
        stage5eg.validate_stage5eg_governance_scope,
    ]:
        result = validator()
        assert result.validation_error_count == 0, result.errors
