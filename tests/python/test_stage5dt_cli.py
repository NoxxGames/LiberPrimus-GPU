from __future__ import annotations

from test_stage5dt_common import ensure_stage5dt_built, run_token_block_cli


def test_stage5dt_cli_validate_and_summary() -> None:
    ensure_stage5dt_built()
    output = run_token_block_cli("validate-stage5dt")
    assert "token_block_stage5dt_valid=true" in output

    summary = run_token_block_cli("stage5dt-summary")
    assert "recommended_next_stage_id=stage-5du" in summary
    assert "number_fact_backfill_performed_now=false" in summary


def test_stage5dt_focused_validators_registered() -> None:
    ensure_stage5dt_built()
    validators = [
        ("validate-stage5dt-number-fact-card-model", "token_block_stage5dt_number_fact_card_model_valid=true"),
        ("validate-stage5dt-number-fact-overlays", "token_block_stage5dt_number_fact_overlays_valid=true"),
        ("validate-stage5dt-reviewability-audit", "token_block_stage5dt_reviewability_audit_valid=true"),
        ("validate-stage5dt-review-batch-plan", "token_block_stage5dt_review_batch_plan_valid=true"),
        ("validate-stage5dt-source-browser-loadability", "token_block_stage5dt_source_browser_loadability_valid=true"),
        ("validate-stage5dt-gui-fact-card-contract", "token_block_stage5dt_gui_fact_card_contract_valid=true"),
        ("validate-stage5dt-stage5ds-preservation", "token_block_stage5dt_stage5ds_preservation_valid=true"),
        ("validate-stage5dt-stage5bd-preservation", "token_block_stage5dt_stage5bd_preservation_valid=true"),
        ("validate-stage5dt-active-lineage-preservation", "token_block_stage5dt_active_lineage_preservation_valid=true"),
        ("validate-stage5dt-sidecar-gates", "token_block_stage5dt_sidecar_gates_valid=true"),
        ("validate-stage5dt-handoff-continuity", "token_block_stage5dt_handoff_continuity_valid=true"),
        ("validate-stage5dt-credential-redaction-policy", "token_block_stage5dt_credential_redaction_policy_valid=true"),
        ("validate-stage5dt-governance-scope", "token_block_stage5dt_governance_scope_valid=true"),
    ]
    for command, marker in validators:
        assert marker in run_token_block_cli(command)
