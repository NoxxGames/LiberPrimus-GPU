from test_stage5cy_common import ensure_stage5cy_built, load_yaml


EXPECTED_OPTION_IDS = [
    "defer_for_more_review",
    "prepare_real_operator_approval_record",
    "prepare_real_deep_research_acceptance_record",
    "prepare_combined_gate_validation",
    "prepare_activation_decision_review",
    "keep_blocked_no_action",
]


def test_stage5cy_operator_facing_preflight_is_not_a_real_decision() -> None:
    ensure_stage5cy_built()
    preflight = load_yaml("data/token-block/stage5cy-operator-option-selection-preflight.yaml")

    assert preflight["operator_facing_option_selection_preflight_created"] is True
    assert preflight["operator_facing_option_selection_preflight_status"] == "review_preflight_only"
    assert preflight["operator_facing_option_selection_preflight_is_real_operator_decision"] is False
    assert preflight["operator_facing_option_selection_preflight_selects_option"] is False
    assert preflight["operator_facing_option_selection_preflight_authorizes_approval"] is False
    assert preflight["operator_facing_option_selection_preflight_authorizes_activation"] is False
    assert preflight["operator_facing_option_selection_preflight_authorizes_active_input"] is False
    assert preflight["operator_facing_option_selection_preflight_authorizes_dry_run_ingestion"] is False
    assert preflight["operator_facing_option_selection_preflight_authorizes_bytes"] is False
    assert preflight["operator_facing_option_selection_preflight_authorizes_execution"] is False


def test_stage5cy_preserves_exact_six_options_and_selects_none() -> None:
    ensure_stage5cy_built()
    options = load_yaml("data/token-block/stage5cy-options-nonselection-proof.yaml")

    assert [option["option_id"] for option in options["operator_decision_options"]] == EXPECTED_OPTION_IDS
    assert options["stage5cs_exact_option_set_preserved"] is True
    assert options["operator_decision_option_count"] == 6
    assert options["operator_decision_option_selected_now"] is False
    assert options["selected_option_id"] is None
    assert all(option["selected_now"] is False for option in options["operator_decision_options"])
    assert options["option_addition_allowed_now"] is False
    assert options["option_removal_allowed_now"] is False
    assert options["option_rename_allowed_now"] is False
