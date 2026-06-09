from __future__ import annotations

from test_stage5dw_common import ensure_stage5dw_built, run_token_block_cli


def test_stage5dw_cli_summary_and_fast_validators() -> None:
    ensure_stage5dw_built()

    summary = run_token_block_cli("stage5dw-summary")

    assert "reviewed_entry_count=20" in summary
    assert "overlay_count=37" in summary
    assert "recommended_next_stage_id=stage-5dx" in summary
    assert "token_block_stage5dw_review_batch_selection_valid=true" in run_token_block_cli(
        "validate-stage5dw-review-batch-selection"
    )
    assert "token_block_stage5dw_number_fact_overlays_valid=true" in run_token_block_cli(
        "validate-stage5dw-number-fact-overlays"
    )
    assert "token_block_stage5dw_governance_scope_valid=true" in run_token_block_cli(
        "validate-stage5dw-governance-scope"
    )
