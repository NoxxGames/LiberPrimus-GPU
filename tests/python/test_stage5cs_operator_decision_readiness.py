from libreprimus.token_block.stage5cs import (
    validate_stage5cs_actual_record_rejection,
    validate_stage5cs_operator_decision_readiness,
)

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_operator_decision_readiness_is_package_only() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-operator-decision-readiness-package.yaml")
    assert payload["operator_decision_readiness_package_status"] == "readiness_package_only"
    assert payload["operator_decision_option_selected_now"] is False
    assert payload["selected_option_id"] is None
    assert payload["operator_decision_package_authorizes_approval"] is False
    counts, errors = validate_stage5cs_operator_decision_readiness()
    assert not errors
    assert counts["stage5cs_operator_decision_readiness_valid"] is True


def test_stage5cs_rejects_real_operator_decision_created_now() -> None:
    errors = validate_stage5cs_actual_record_rejection(
        {"real_operator_decision_record_created_now": True}
    )
    assert errors
