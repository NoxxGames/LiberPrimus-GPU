from test_stage5bn_common import load_yaml


def test_stage5bn_summary_records_counts_and_guardrails() -> None:
    payload = load_yaml("data/project-state/stage5bn-summary.yaml")

    assert payload["status"] == "complete"
    assert payload["target_token_index_0_based"] == 199
    assert payload["unsupported_position_closure_status"] == "closed_spreadsheet_support_found"
    assert payload["spreadsheet_supports_0l"] is True
    assert payload["human_review_pack_generated"] is False
    assert payload["human_review_required"] is False
    assert payload["proposed_option_addendum_status"] == "proposed_inactive_review_only"
    assert payload["stage5bn_proposes_inactive_0l_addendum"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["codex_output_directory_used"] is False
