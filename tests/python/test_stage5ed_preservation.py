from __future__ import annotations

from libreprimus.token_block.stage5ed import (
    validate_stage5ed_active_lineage_preservation,
    validate_stage5ed_governance_scope,
    validate_stage5ed_stage5bd_preservation,
    validate_stage5ed_stage5dg_preservation,
    validate_stage5ed_stage5du_preservation,
    validate_stage5ed_stage5dv_preservation,
    validate_stage5ed_stage5dw_preservation,
    validate_stage5ed_stage5dx_preservation,
    validate_stage5ed_stage5eb_validation_policy,
    validate_stage5ed_stage5ec_preservation,
)
from test_stage5ed_common import ensure_stage5ed_built, load_yaml


def test_stage5ed_preserves_prior_governance_layers() -> None:
    ensure_stage5ed_built()
    validators = [
        validate_stage5ed_stage5ec_preservation,
        validate_stage5ed_stage5eb_validation_policy,
        validate_stage5ed_stage5dx_preservation,
        validate_stage5ed_stage5dw_preservation,
        validate_stage5ed_stage5dv_preservation,
        validate_stage5ed_stage5du_preservation,
        validate_stage5ed_stage5dg_preservation,
        validate_stage5ed_stage5bd_preservation,
        validate_stage5ed_active_lineage_preservation,
        validate_stage5ed_governance_scope,
    ]

    for validator in validators:
        assert validator().validation_error_count == 0


def test_stage5ed_preserves_stage5eb_ten_worker_policy() -> None:
    ensure_stage5ed_built()
    summary = load_yaml("data/project-state/stage5ed-summary.yaml")

    assert summary["local_parallel_default_workers"] == 10
    assert summary["local_parallel_default_pytest_workers"] == 10
    assert summary["maximum_supported_workers"] == 10
    assert summary["maximum_supported_pytest_workers"] == 10
    assert summary["full_serial_pytest_required_for_normal_stage_completion"] is False


def test_stage5ed_preserves_stage5ec_overlay_batch() -> None:
    ensure_stage5ed_built()
    record = load_yaml("data/project-state/stage5ed-stage5ec-preservation.yaml")

    assert record["stage5ec_preserved"] is True
    assert record["stage5ec_reviewed_entry_count"] == 20
    assert record["stage5ec_overlay_count"] == 25
    assert record["stage5ec_source_browser_validation_error_count"] == 0
