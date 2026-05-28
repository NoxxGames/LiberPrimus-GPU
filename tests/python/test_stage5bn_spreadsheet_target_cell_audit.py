from test_stage5bn_common import load_yaml


def test_stage5bn_spreadsheet_target_cell_audit_is_target_only() -> None:
    payload = load_yaml("data/token-block/stage5bn-local-spreadsheet-target-cell-audit.yaml")

    assert payload["spreadsheet_found"] is True
    assert payload["target_token_index_0_based"] == 199
    assert payload["target_cell_or_row_identified"] is True
    assert payload["target_excel_row_one_based"] == 203
    assert payload["target_possible_tokens_from_spreadsheet"] == ["0l"]
    assert payload["spreadsheet_supports_0l"] is True
    assert payload["spreadsheet_body_committed"] is False
    assert payload["spreadsheet_file_committed"] is False
    assert payload["full_cell_dump_committed"] is False
