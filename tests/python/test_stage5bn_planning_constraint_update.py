from test_stage5bn_common import load_yaml


def test_stage5bn_planning_constraint_update_does_not_enable_ingestion() -> None:
    payload = load_yaml("data/token-block/stage5bn-string4-planning-constraint-update.yaml")

    assert payload["planning_effect"] == "source_gap_closed_metadata_only"
    assert payload["string4_active_input_allowed"] is False
    assert payload["string4_execution_input_allowed"] is False
    assert payload["string4_byte_stream_generation_allowed"] is False
    assert payload["string4_dry_run_ingestion_allowed_now"] is False
    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
