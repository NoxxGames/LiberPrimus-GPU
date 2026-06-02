from libreprimus.token_block.stage5cw import FUTURE_REAL_DECISION_INPUTS

from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_future_real_decision_requirements_are_review_only() -> None:
    ensure_stage5cw_built()
    payload = load_yaml(
        "data/token-block/stage5cw-future-real-operator-decision-package-requirements.yaml"
    )

    assert set(payload["required_future_inputs"]) == set(FUTURE_REAL_DECISION_INPUTS)
    assert payload["required_future_input_count"] == len(FUTURE_REAL_DECISION_INPUTS)
    assert payload["real_decision_package_created_now"] is False
    assert payload["real_decision_package_valid_now"] is False
    assert payload["selected_option_id"] is None
