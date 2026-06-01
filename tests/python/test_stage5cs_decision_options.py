from libreprimus.token_block.stage5cs import (
    OPERATOR_DECISION_OPTIONS,
    validate_stage5cs_decision_options,
)

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_decision_options_are_unselected_scaffold_only() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-real-approval-decision-options-scaffold.yaml")
    assert payload["real_approval_decision_options_status"] == "options_scaffold_only"
    assert payload["operator_decision_option_count"] == 6
    assert {option["option_id"] for option in payload["options"]} == {
        option["option_id"] for option in OPERATOR_DECISION_OPTIONS
    }
    assert all(option["selected_now"] is False for option in payload["options"])
    counts, errors = validate_stage5cs_decision_options()
    assert not errors
    assert counts["stage5cs_decision_options_valid"] is True


def test_stage5cs_decision_options_validator_rejects_selected_option() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-real-approval-decision-options-scaffold.yaml")
    payload["options"][0]["selected_now"] = True
    errors: list[str] = []
    from libreprimus.token_block.stage5cs import _validate_decision_options_payload

    _validate_decision_options_payload(payload, errors)
    assert errors
