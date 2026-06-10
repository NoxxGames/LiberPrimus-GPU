from __future__ import annotations

from test_stage5dy_common import ensure_stage5dy_built, run_token_block_cli


def test_stage5dy_cli_summary_and_validators() -> None:
    ensure_stage5dy_built()

    summary = run_token_block_cli("stage5dy-summary")

    assert "parallel_worker_cap=8" in summary
    assert "full_serial_pytest_default=False" in summary
    assert "recommended_next_stage_id=stage-5dz" in summary
    assert "token_block_stage5dy_valid=true" in run_token_block_cli("validate-stage5dy")
    assert "token_block_stage5dy_validation_profile_registry_valid=true" in run_token_block_cli(
        "validate-stage5dy-validation-profile-registry"
    )
    assert "token_block_stage5dy_stage_isolation_policy_valid=true" in run_token_block_cli(
        "validate-stage5dy-stage-isolation-policy"
    )
