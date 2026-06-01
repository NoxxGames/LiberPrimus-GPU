from libreprimus.token_block.stage5cq import (
    validate_stage5cq_actual_record_rejection,
    validate_stage5cq_operator_decision_package,
)

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_operator_decision_package_is_scaffold_only() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/token-block/stage5cq-operator-decision-package-scaffold.yaml")
    assert payload["operator_decision_package_status"] == "scaffold_only"
    assert payload["operator_decision_package_authorizes_approval"] is False
    assert payload["operator_decision_package_authorizes_activation"] is False
    assert payload["operator_decision_package_authorizes_active_input"] is False
    assert payload["operator_decision_package_authorizes_execution"] is False
    counts, errors = validate_stage5cq_operator_decision_package()
    assert not errors
    assert counts["stage5cq_operator_decision_package_valid"] is True


def test_stage5cq_rejects_operator_decision_satisfied_now() -> None:
    assert validate_stage5cq_actual_record_rejection({"operator_decision_satisfied_now": True})
