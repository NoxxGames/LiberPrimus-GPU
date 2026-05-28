from test_stage5bm_common import load_yaml


def test_stage5bm_next_stage_decision_selects_gap_closure_not_execution() -> None:
    record = load_yaml("data/project-state/stage5bm-next-stage-decision.yaml")

    assert record["selected_next_stage_id"] == "stage-5bn"
    assert "String 4 unsupported-position source-gap closure" in record["selected_next_stage_title"]
    assert record["token_block_execution_selected"] is False
    assert record["byte_stream_generation_selected"] is False
    assert record["cuda_selected"] is False
    assert record["solve_claim"] is False
