from __future__ import annotations

from test_stage5ea_common import ensure_stage5ea_built, run_token_block_cli


def test_stage5ea_cli_summary_and_validators() -> None:
    ensure_stage5ea_built()

    summary = run_token_block_cli("stage5ea-summary")

    assert "recommended_next_stage=stage-5eb" in summary
    assert "number_fact_review_batch_3_performed_now=false" in summary
    assert "number_fact_review_batch_3_deferred_to_stage5eb=true" in summary
    assert "token_block_stage5ea_valid=true" in run_token_block_cli("validate-stage5ea")
    assert "token_block_stage5ea_current_stage_registry_valid=true" in run_token_block_cli(
        "validate-stage5ea-current-stage-registry"
    )
    assert "token_block_stage5ea_source_browser_performance_valid=true" in run_token_block_cli(
        "validate-stage5ea-source-browser-performance"
    )
