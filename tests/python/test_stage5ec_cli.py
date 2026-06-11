from __future__ import annotations

from test_stage5ec_common import ensure_stage5ec_built, run_token_block_cli


def test_stage5ec_cli_summary_and_fast_validators() -> None:
    ensure_stage5ec_built()

    summary = run_token_block_cli("stage5ec-summary")

    assert "reviewed_entry_count=20" in summary
    assert "overlay_count=25" in summary
    assert "recommended_next_stage_id=stage-5ed" in summary
    assert "local_parallel_default_workers=10" in summary
    assert "token_block_stage5ec_review_batch_selection_valid=true" in run_token_block_cli(
        "validate-stage5ec-review-batch-selection"
    )
    assert "token_block_stage5ec_number_fact_overlays_valid=true" in run_token_block_cli(
        "validate-stage5ec-number-fact-overlays"
    )
    assert "token_block_stage5ec_governance_scope_valid=true" in run_token_block_cli(
        "validate-stage5ec-governance-scope"
    )
