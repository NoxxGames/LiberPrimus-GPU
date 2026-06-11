from __future__ import annotations

from libreprimus.token_block.stage5ec import (
    validate_stage5ec_active_lineage_preservation,
    validate_stage5ec_governance_scope,
    validate_stage5ec_stage5bd_preservation,
    validate_stage5ec_stage5dg_preservation,
    validate_stage5ec_stage5du_preservation,
    validate_stage5ec_stage5dv_preservation,
    validate_stage5ec_stage5dw_preservation,
    validate_stage5ec_stage5dx_preservation,
    validate_stage5ec_stage5eb_preservation,
)
from test_stage5ec_common import ensure_stage5ec_built, load_yaml


def test_stage5ec_preserves_prior_governance_layers() -> None:
    ensure_stage5ec_built()
    validators = [
        validate_stage5ec_stage5eb_preservation,
        validate_stage5ec_stage5dx_preservation,
        validate_stage5ec_stage5dw_preservation,
        validate_stage5ec_stage5dv_preservation,
        validate_stage5ec_stage5du_preservation,
        validate_stage5ec_stage5dg_preservation,
        validate_stage5ec_stage5bd_preservation,
        validate_stage5ec_active_lineage_preservation,
        validate_stage5ec_governance_scope,
    ]

    for validator in validators:
        assert validator().validation_error_count == 0


def test_stage5ec_preserves_stage5eb_ten_worker_policy() -> None:
    ensure_stage5ec_built()
    summary = load_yaml("data/project-state/stage5ec-summary.yaml")

    assert summary["local_parallel_default_workers"] == 10
    assert summary["local_parallel_default_pytest_workers"] == 10
    assert summary["maximum_supported_workers"] == 10
    assert summary["maximum_supported_pytest_workers"] == 10
    assert summary["full_serial_pytest_required_for_normal_stage_completion"] is False
