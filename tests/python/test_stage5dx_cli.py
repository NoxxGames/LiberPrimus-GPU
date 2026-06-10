from __future__ import annotations

from test_stage5dx_common import ensure_stage5dx_built, run_token_block_cli


def test_stage5dx_cli_summary_and_fast_validators() -> None:
    ensure_stage5dx_built()

    summary = run_token_block_cli("stage5dx-summary")

    assert "reviewed_entry_count=20" in summary
    assert "overlay_count=23" in summary
    assert "recommended_next_stage_id=stage-5dy" in summary
    assert "token_block_stage5dx_review_batch_selection_valid=true" in run_token_block_cli(
        "validate-stage5dx-review-batch-selection"
    )
    assert "token_block_stage5dx_number_fact_overlays_valid=true" in run_token_block_cli(
        "validate-stage5dx-number-fact-overlays"
    )
    assert "token_block_stage5dx_governance_scope_valid=true" in run_token_block_cli(
        "validate-stage5dx-governance-scope"
    )
