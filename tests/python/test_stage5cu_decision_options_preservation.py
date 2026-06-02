from libreprimus.token_block.stage5cu import (
    OPERATOR_DECISION_OPTIONS,
    validate_stage5cu_decision_options_preservation,
)

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_preserves_stage5cs_six_option_scaffold_unselected() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-stage5cs-decision-options-preservation.yaml")
    assert payload["stage5cs_real_approval_decision_options_status_preserved"] == "options_scaffold_only"
    assert payload["stage5cs_option_count_preserved"] == len(OPERATOR_DECISION_OPTIONS)
    assert payload["operator_decision_option_selected_now"] is False
    assert payload["selected_option_id"] is None
    assert {option["option_id"] for option in payload["options"]} == {
        option["option_id"] for option in OPERATOR_DECISION_OPTIONS
    }
    counts, errors = validate_stage5cu_decision_options_preservation()
    assert not errors
    assert counts["stage5cu_decision_options_preservation_valid"] is True
