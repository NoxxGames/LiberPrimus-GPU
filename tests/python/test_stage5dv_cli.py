from __future__ import annotations

from test_stage5dv_common import ensure_stage5dv_built, run_token_block_cli


def test_stage5dv_cli_summary_and_fast_validators() -> None:
    ensure_stage5dv_built()
    summary = run_token_block_cli("stage5dv-summary")
    assert "recommended_next_stage_id=stage-5dw" in summary
    assert "number_fact_review_batch_1_performed_now=false" in summary

    assert "token_block_stage5dv_chatgpt_context_valid=true" in run_token_block_cli(
        "validate-stage5dv-chatgpt-context"
    )
    assert "token_block_stage5dv_governance_scope_valid=true" in run_token_block_cli(
        "validate-stage5dv-governance-scope"
    )


def test_stage5dv_focused_preservation_validators_registered() -> None:
    ensure_stage5dv_built()
    validators = [
        ("validate-stage5dv-stage5du-preservation", "token_block_stage5dv_stage5du_preservation_valid=true"),
        ("validate-stage5dv-stage5dt-preservation", "token_block_stage5dv_stage5dt_preservation_valid=true"),
        ("validate-stage5dv-stage5dg-preservation", "token_block_stage5dv_stage5dg_preservation_valid=true"),
        ("validate-stage5dv-stage5bd-preservation", "token_block_stage5dv_stage5bd_preservation_valid=true"),
        (
            "validate-stage5dv-active-lineage-preservation",
            "token_block_stage5dv_active_lineage_preservation_valid=true",
        ),
        ("validate-stage5dv-sidecar-gates", "token_block_stage5dv_sidecar_gates_valid=true"),
        ("validate-stage5dv-handoff-continuity", "token_block_stage5dv_handoff_continuity_valid=true"),
        (
            "validate-stage5dv-credential-redaction-policy",
            "token_block_stage5dv_credential_redaction_policy_valid=true",
        ),
    ]
    for command, marker in validators:
        assert marker in run_token_block_cli(command)
