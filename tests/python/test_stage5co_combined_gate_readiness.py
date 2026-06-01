from libreprimus.token_block.stage5co import (
    COMBINED_GATE_REQUIREMENTS,
    validate_stage5co_actual_record_rejection,
    validate_stage5co_real_combined_gate_readiness,
)

from test_stage5co_common import load_yaml


def test_stage5co_combined_gate_remains_unsatisfied() -> None:
    payload = load_yaml(
        "data/token-block/stage5co-real-combined-gate-validation-readiness-preflight.yaml"
    )
    assert payload["real_combined_gate_validation_readiness_preflight_created"] is True
    assert payload["combined_approval_gate_satisfied_now"] is False
    assert payload["combined_approval_gate_authorizes_activation_now"] is False
    assert set(COMBINED_GATE_REQUIREMENTS).issubset(payload["required_future_validations"])

    counts, errors = validate_stage5co_real_combined_gate_readiness()
    assert errors == []
    assert counts["stage5co_real_combined_gate_readiness_valid"] is True


def test_stage5co_rejects_synthetic_combined_gate_satisfied_now() -> None:
    errors = validate_stage5co_actual_record_rejection(
        {"combined_approval_gate_satisfied_now": True}
    )
    assert errors
