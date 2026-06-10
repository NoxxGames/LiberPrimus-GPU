from __future__ import annotations

from libreprimus.token_block.stage5dz import PROJECT_STATE_PATHS
from test_stage5dz_common import ensure_stage5dz_built, load_yaml, run_token_block_cli


def test_stage5dz_preserves_stage5dy_validation_profile_policy() -> None:
    ensure_stage5dz_built()

    payload = load_yaml(PROJECT_STATE_PATHS["validation_performance_compliance"])

    assert payload["stage5dy_validation_profiles_preserved"] is True
    assert payload["parallel_worker_cap"] == 8
    assert payload["full_serial_pytest_default_for_future_stages"] is False
    assert payload["stage_specific_schema_paths_used"] is True
    assert "token_block_stage5dz_validation_performance_compliance_valid=true" in run_token_block_cli(
        "validate-stage5dz-validation-performance-compliance"
    )
