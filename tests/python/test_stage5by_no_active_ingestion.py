from test_stage5by_common import load_yaml


def test_stage5by_no_active_ingestion_remains_closed() -> None:
    proof = load_yaml("data/token-block/stage5by-no-active-ingestion-proof.yaml")
    assert proof["string4_active_input_allowed"] is False
    assert proof["string4_dry_run_ingestion_allowed_now"] is False
    assert proof["string4_execution_input_allowed"] is False
    assert proof["string4_added_to_active_dry_run_inputs"] is False
    assert proof["string4_added_to_stage5bd_run_plan_ids"] is False
