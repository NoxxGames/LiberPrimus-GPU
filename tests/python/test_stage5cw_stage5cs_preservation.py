from libreprimus.token_block.stage5cu import OPERATOR_DECISION_OPTIONS

from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_preserves_stage5cs_options_exactly() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-stage5cs-decision-options-preservation.yaml")

    expected_ids = {option["option_id"] for option in OPERATOR_DECISION_OPTIONS}
    observed_ids = {option["option_id"] for option in payload["options"]}
    assert payload["stage5cs_real_approval_decision_options_status_preserved"] == (
        "options_scaffold_only"
    )
    assert payload["stage5cs_option_count_preserved"] == 6
    assert payload["stage5cs_exact_option_set_preserved"] is True
    assert observed_ids == expected_ids
    assert payload["operator_decision_option_selected_now"] is False
    assert payload["selected_option_id"] is None
    for option in payload["options"]:
        assert option["selected_now"] is False
        assert option["authorizes_execution_now"] is False
