from __future__ import annotations

from libreprimus.token_block.stage5ee import (
    validate_stage5ee_active_lineage_preservation,
    validate_stage5ee_governance_scope,
    validate_stage5ee_stage5bd_preservation,
    validate_stage5ee_stage5dg_preservation,
    validate_stage5ee_stage5eb_validation_policy,
    validate_stage5ee_stage5ed_preservation,
)
from test_stage5ee_common import ensure_stage5ee_built, load_yaml


def test_stage5ee_preserves_prior_governance_layers() -> None:
    ensure_stage5ee_built()
    validators = [
        validate_stage5ee_stage5ed_preservation,
        validate_stage5ee_stage5eb_validation_policy,
        validate_stage5ee_stage5dg_preservation,
        validate_stage5ee_stage5bd_preservation,
        validate_stage5ee_active_lineage_preservation,
        validate_stage5ee_governance_scope,
    ]

    for validator in validators:
        assert validator().validation_error_count == 0


def test_stage5ee_preserves_stage5eb_ten_worker_policy() -> None:
    ensure_stage5ee_built()
    summary = load_yaml("data/project-state/stage5ee-summary.yaml")

    assert summary["local_parallel_default_workers"] == 10
    assert summary["local_parallel_default_pytest_workers"] == 10
    assert summary["maximum_supported_workers"] == 10
    assert summary["maximum_supported_pytest_workers"] == 10
    assert summary["full_serial_pytest_required_for_normal_stage_completion"] is False


def test_stage5ee_preserves_stage5ed_overlay_batch() -> None:
    ensure_stage5ee_built()
    record = load_yaml("data/project-state/stage5ee-stage5ed-preservation.yaml")

    assert record["stage5ed_preserved"] is True
    assert record["stage5ed_reviewed_entry_count"] == 20
    assert record["stage5ed_overlay_count"] == 25
    assert record["stage5ed_fact_card_count_after_stage5ed"] == 142
    assert record["stage5ed_source_browser_validation_error_count"] == 0
