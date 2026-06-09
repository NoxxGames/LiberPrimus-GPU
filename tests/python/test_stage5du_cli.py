from __future__ import annotations

from test_stage5du_common import ensure_stage5du_built, run_token_block_cli


def test_stage5du_cli_validate_and_summary() -> None:
    ensure_stage5du_built()
    output = run_token_block_cli("validate-stage5du")
    assert "token_block_stage5du_valid=true" in output

    summary = run_token_block_cli("stage5du-summary")
    assert "recommended_next_stage_id=stage-5dv" in summary
    assert "community_code_executed_now=false" in summary
    assert "ocr_performed=false" in summary


def test_stage5du_focused_validators_registered() -> None:
    ensure_stage5du_built()
    validators = [
        (
            "validate-stage5du-community-thread-source-locks",
            "token_block_stage5du_community_thread_source_locks_valid=true",
        ),
        (
            "validate-stage5du-thread-file-inventory",
            "token_block_stage5du_thread_file_inventory_valid=true",
        ),
        (
            "validate-stage5du-canonical-page-root-crosslink",
            "token_block_stage5du_canonical_page_root_crosslink_valid=true",
        ),
        (
            "validate-stage5du-number-fact-cards",
            "token_block_stage5du_number_fact_cards_valid=true",
        ),
        (
            "validate-stage5du-stage5dt-preservation",
            "token_block_stage5du_stage5dt_preservation_valid=true",
        ),
        (
            "validate-stage5du-sidecar-gates",
            "token_block_stage5du_sidecar_gates_valid=true",
        ),
        (
            "validate-stage5du-governance-scope",
            "token_block_stage5du_governance_scope_valid=true",
        ),
    ]
    for command, marker in validators:
        assert marker in run_token_block_cli(command)
