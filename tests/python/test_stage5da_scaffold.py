from __future__ import annotations

from test_stage5da_common import ensure_stage5da_built, load_yaml


EXPECTED_OPTION_IDS = [
    "defer_for_more_review",
    "prepare_real_operator_approval_record",
    "prepare_real_deep_research_acceptance_record",
    "prepare_combined_gate_validation",
    "prepare_activation_decision_review",
    "keep_blocked_no_action",
]


def test_stage5da_integrates_stage5cz_accept_with_warnings() -> None:
    ensure_stage5da_built()
    findings = load_yaml("data/project-state/stage5da-stage5cz-findings-integration.yaml")

    assert findings["stage5cz_verdict"] == "accept_with_warnings"
    assert findings["stage5cz_findings_integrated"] is True
    assert findings["stage5cz_did_not_recommend_execution"] is True
    assert findings["stage5cz_did_not_provide_operator_choice"] is True


def test_stage5da_choice_pause_scaffold_is_not_a_decision() -> None:
    ensure_stage5da_built()
    scaffold = load_yaml("data/token-block/stage5da-operator-choice-pause-decision-scaffold.yaml")

    assert scaffold["operator_choice_pause_decision_scaffold_status"] == "scaffold_only"
    assert scaffold["operator_choice_or_pause_record_created_now"] is False
    assert scaffold["operator_choice_or_pause_record_valid_now"] is False
    assert scaffold["explicit_operator_choice_provided_now"] is False
    assert scaffold["explicit_pause_provided_now"] is False
    assert scaffold["automatic_option_selection_allowed"] is False
    assert scaffold["selected_option_id"] is None


def test_stage5da_preserves_exact_six_options_and_selects_none() -> None:
    ensure_stage5da_built()
    nonselection = load_yaml(
        "data/token-block/stage5da-operator-choice-pause-nonselection-proof.yaml"
    )

    options = nonselection["operator_decision_options"]
    assert nonselection["operator_decision_option_count"] == 6
    assert [option["option_id"] for option in options] == EXPECTED_OPTION_IDS
    assert all(option["selected_now"] is False for option in options)
    assert nonselection["all_options_unselected"] is True
    assert nonselection["operator_decision_option_selected_now"] is False
    assert nonselection["selected_option_id"] is None
    assert nonselection["explicit_pause_selected_now"] is False


def test_stage5da_explicit_pause_path_does_not_activate_anything() -> None:
    ensure_stage5da_built()
    pause = load_yaml("data/token-block/stage5da-explicit-pause-nonactivation-proof.yaml")

    assert pause["explicit_pause_available_as_future_operator_outcome"] is True
    assert pause["explicit_pause_selected_now"] is False
    assert pause["explicit_pause_provided_now"] is False
    assert pause["explicit_pause_authorizes_approval"] is False
    assert pause["explicit_pause_authorizes_activation"] is False
    assert pause["explicit_pause_authorizes_active_input"] is False
    assert pause["explicit_pause_authorizes_byte_stream_generation"] is False
    assert pause["explicit_pause_authorizes_execution"] is False
