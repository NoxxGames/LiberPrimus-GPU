from libreprimus.token_block.stage5cm import (
    FUTURE_REAL_READINESS_CRITERIA,
    validate_stage5cm_real_approval_readiness,
)

from test_stage5cm_common import load_yaml


def test_stage5cm_real_approval_readiness_is_future_only() -> None:
    payload = load_yaml("data/token-block/stage5cm-real-approval-record-readiness-preflight.yaml")
    assert payload["real_approval_readiness_preflight_created"] is True
    assert payload["real_operator_approval_record_created_now"] is False
    assert payload["real_deep_research_acceptance_record_created_now"] is False
    assert payload["real_combined_gate_validation_record_created_now"] is False
    assert payload["real_activation_decision_record_created_now"] is False
    assert payload["real_approval_readiness_satisfied_now"] is False
    assert set(payload["real_approval_readiness_criteria"]) == set(FUTURE_REAL_READINESS_CRITERIA)

    counts, errors = validate_stage5cm_real_approval_readiness()
    assert errors == []
    assert counts["real_approval_readiness_criteria_count"] == len(FUTURE_REAL_READINESS_CRITERIA)
