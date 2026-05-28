from test_stage5bm_common import load_yaml


def test_stage5bm_string4_planning_constraint_blocks_ingestion() -> None:
    record = load_yaml("data/token-block/stage5bm-string4-planning-constraint.yaml")

    assert record["planning_effect"] == "source_gap"
    assert record["string4_active_input_allowed"] is False
    assert record["string4_byte_stream_generation_allowed"] is False
    assert record["string4_dry_run_ingestion_allowed_now"] is False
    assert record["requires_gap_closure_before_any_ingestion"] is True
