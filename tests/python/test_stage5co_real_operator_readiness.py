from libreprimus.token_block.stage5co import (
    FORBIDDEN_CURRENT_RECORD_CLASSES,
    REAL_OPERATOR_REQUIREMENTS,
    validate_stage5co_actual_record_rejection,
    validate_stage5co_real_operator_readiness,
)

from test_stage5co_common import load_yaml


def test_stage5co_real_operator_readiness_is_absent_now() -> None:
    payload = load_yaml(
        "data/token-block/stage5co-real-operator-approval-readiness-preflight.yaml"
    )
    assert payload["real_operator_approval_readiness_preflight_created"] is True
    assert payload["real_operator_approval_record_present_now"] is False
    assert set(REAL_OPERATOR_REQUIREMENTS).issubset(payload["required_future_fields"])
    assert set(payload["future_record_must_not_be"]) == set(FORBIDDEN_CURRENT_RECORD_CLASSES)

    counts, errors = validate_stage5co_real_operator_readiness()
    assert errors == []
    assert counts["stage5co_real_operator_readiness_valid"] is True


def test_stage5co_rejects_synthetic_operator_present_now() -> None:
    errors = validate_stage5co_actual_record_rejection(
        {"real_operator_approval_record_present_now": True}
    )
    assert errors
