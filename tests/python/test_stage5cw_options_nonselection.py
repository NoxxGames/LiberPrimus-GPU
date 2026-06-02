from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_options_remain_unselected() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-operator-options-nonselection-proof.yaml")

    assert payload["all_options_unselected"] is True
    assert payload["operator_decision_option_selected_now"] is False
    assert payload["selected_option_id"] is None
    assert all(option["selected_now"] is False for option in payload["options"])
