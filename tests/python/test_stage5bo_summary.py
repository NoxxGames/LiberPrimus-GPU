from test_stage5bo_common import load_yaml


def test_stage5bo_summary_records_counts_and_next_stage() -> None:
    payload = load_yaml("data/project-state/stage5bo-summary.yaml")

    assert payload["status"] == "complete"
    assert payload["token_case_errata_record_count"] == 8
    assert payload["case_199_operator_errata_found"] is True
    assert payload["case_198_operator_errata_found"] is True
    assert payload["case_199_original_possible_tokens"] == ["0I", "0j", "OI", "Oj"]
    assert payload["case_199_corrected_possible_tokens"] == ["0I", "0l", "OI", "Ol"]
    assert payload["string4_branch_membership_status_after_errata"] == "full_branch_match"
    assert payload["stage5bn_addendum_integrated_as_inactive"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["recommended_next_prompt_type"] == "deep_research_review"
