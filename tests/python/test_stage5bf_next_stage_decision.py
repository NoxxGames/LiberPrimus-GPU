from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_next_stage_decision_selects_deep_research_review() -> None:
    payload = load_yaml("data/project-state/stage5bf-next-stage-decision.yaml")

    assert payload["selected_next_prompt_type"] == "deep_research_review"
    assert payload["selected_next_stage_id"] == "stage-5bg"
    assert payload["token_block_preflight_execution_selected"] is False
    assert payload["dwh_hash_search_selected"] is False
    assert payload["unsolved_page_cuda_selected"] is False
