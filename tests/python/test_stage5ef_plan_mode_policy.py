from __future__ import annotations

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_plan_mode_evidence_is_recorded() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_plan_mode_policy()
    policy = load_yaml("data/project-state/stage5ef-plan-mode-codex-run-policy.yaml")

    assert result.validation_error_count == 0
    assert policy["plan_mode_used_for_stage5ef"] is True
    assert policy["plan_review_performed_before_editing"] is True
    assert policy["plan_amendment_applied_before_editing"] is True
    assert policy["plan_deviation_count"] == 0
    assert policy["full_serial_pytest_required_for_normal_completion"] is False
    assert policy["full_parallel_workers"] == 10
    assert policy["full_parallel_pytest_workers"] == 10
