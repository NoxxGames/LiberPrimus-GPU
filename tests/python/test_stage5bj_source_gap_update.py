from test_stage5bj_crosswalk_closure import load_yaml


def test_all_stage5bi_source_gaps_are_mapped() -> None:
    stage5bi = load_yaml("data/historical-route/stage5bi-source-gap-register.yaml")
    stage5bj = load_yaml("data/historical-route/stage5bj-source-gap-update.yaml")

    original_gap_ids = {record["gap_id"] for record in stage5bi["gaps"]}
    updated_origin_ids = {
        record["gap_id"] for record in stage5bj["records"] if record["source_gap_origin"] == "stage-5bi"
    }

    assert updated_origin_ids == original_gap_ids
    assert stage5bj["source_gap_origin_count"] == 5
    assert stage5bj["source_gap_closed_count"] == 4
    assert stage5bj["new_source_gap_count"] == 2


def test_spreadsheet_remains_reference_only() -> None:
    payload = load_yaml("data/historical-route/stage5bj-source-gap-update.yaml")
    spreadsheet = next(record for record in payload["records"] if record["gap_id"] == "stage5bi-spreadsheet-not-canonical")

    assert spreadsheet["closure_status"] == "downgraded_to_reference_only"
    assert spreadsheet["carried_forward"] is False
    assert spreadsheet["execution_allowed"] is False
    assert spreadsheet["solve_claim"] is False
