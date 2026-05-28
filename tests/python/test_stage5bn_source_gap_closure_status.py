from test_stage5bn_common import load_yaml


def test_stage5bn_source_gap_closure_keeps_execution_blocked() -> None:
    payload = load_yaml("data/token-block/stage5bn-string4-source-gap-closure-status.yaml")

    assert payload["unsupported_position_closure_status"] == "closed_spreadsheet_support_found"
    assert payload["stage5aw_supports_0l_after_stage5bn"] is False
    assert payload["stage5bn_proposes_inactive_0l_addendum"] is True
    assert payload["blocks_string4_ingestion_or_active_use"] is True
    assert payload["blocks_future_token_block_execution"] is True
    assert payload["blocks_metadata_planning"] is False
    assert payload["execution_allowed"] is False
