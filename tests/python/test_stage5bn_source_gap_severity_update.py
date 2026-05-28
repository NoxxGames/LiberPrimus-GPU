from test_stage5bn_common import load_yaml


def test_stage5bn_source_gap_severity_records_closed_metadata_status() -> None:
    payload = load_yaml("data/historical-route/stage5bn-source-gap-severity-update.yaml")

    assert payload["string4_unsupported_position_gap_status"] == "closed"
    record = payload["records"][0]
    assert record["target_token_index_0_based"] == 199
    assert record["closure_status"] == "closed_spreadsheet_support_found"
    assert record["severity"] == "medium"
    assert record["blocks_execution"] is True
    assert record["blocks_future_token_block_execution"] is True
