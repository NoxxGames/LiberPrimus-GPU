from test_stage5bk_common import load_yaml


def test_stage5bk_next_stage_is_review_not_execution() -> None:
    payload = load_yaml("data/project-state/stage5bk-next-stage-decision.yaml")
    assert payload["selected_next_stage_id"] == "stage-5bl"
    assert payload["selected_next_prompt_type"] == "deep_research_review"
    assert payload["token_block_execution_selected"] is False
    assert payload["byte_stream_generation_selected"] is False
    assert payload["cuda_selected"] is False
    assert payload["solve_claim"] is False
