from __future__ import annotations

from test_stage5eb_common import ensure_stage5eb_built, run_token_block_cli


def test_stage5eb_cli_summary_and_validators() -> None:
    ensure_stage5eb_built()

    summary = run_token_block_cli("stage5eb-summary")

    assert "recommended_next_stage=stage-5ec" in summary
    assert "number_fact_review_batch_3_performed_now=false" in summary
    assert "number_fact_review_batch_3_deferred_to_stage5ec=true" in summary
    assert "local_parallel_default_workers=10" in summary
    assert "full_serial_pytest_default_for_future_stages=false" in summary
    assert "token_block_stage5eb_valid=true" in run_token_block_cli("validate-stage5eb")
    assert "token_block_stage5eb_parallel_worker_policy_valid=true" in run_token_block_cli(
        "validate-stage5eb-parallel-worker-policy"
    )
    assert "token_block_stage5eb_current_stage_registry_policy_valid=true" in run_token_block_cli(
        "validate-stage5eb-current-stage-registry-policy"
    )
