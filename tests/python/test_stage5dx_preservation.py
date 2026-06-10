from __future__ import annotations

from libreprimus.token_block.stage5dx import (
    validate_stage5dx_active_lineage_preservation,
    validate_stage5dx_governance_scope,
    validate_stage5dx_stage5bd_preservation,
    validate_stage5dx_stage5dg_preservation,
    validate_stage5dx_stage5du_preservation,
    validate_stage5dx_stage5dv_preservation,
    validate_stage5dx_stage5dw_preservation,
)
from test_stage5dx_common import ensure_stage5dx_built, load_yaml


def test_stage5dx_preserves_prior_governance_layers() -> None:
    ensure_stage5dx_built()
    validators = [
        validate_stage5dx_stage5dw_preservation,
        validate_stage5dx_stage5dv_preservation,
        validate_stage5dx_stage5du_preservation,
        validate_stage5dx_stage5dg_preservation,
        validate_stage5dx_stage5bd_preservation,
        validate_stage5dx_active_lineage_preservation,
        validate_stage5dx_governance_scope,
    ]

    for validator in validators:
        assert validator().validation_error_count == 0


def test_stage5dx_run_plan_active_lineage_and_worker_cap_are_preserved() -> None:
    ensure_stage5dx_built()
    summary = load_yaml("data/project-state/stage5dx-summary.yaml")

    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["active_lineage_record_count"] == 8
    assert summary["parallel_worker_cap"] == 8
    assert summary["old_16_worker_default_reintroduced"] is False
