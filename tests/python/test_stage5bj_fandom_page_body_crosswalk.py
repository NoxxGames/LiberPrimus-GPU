from test_stage5bj_crosswalk_closure import load_yaml


def test_fandom_page_body_crosswalk_preserves_secondary_status() -> None:
    payload = load_yaml("data/historical-route/stage5bj-fandom-page-body-crosswalk.yaml")
    records = payload["records"]

    assert payload["fandom_page_body_crosswalk_count"] == len(records)
    assert payload["local_page_snapshot_found_count"] == 0
    assert payload["page_body_not_found_count"] >= 1
    for record in records:
        assert record["fandom_page_body_committed"] is False
        assert record["execution_allowed"] is False
        assert record["solve_claim"] is False


def test_fandom_2014_page_body_gap_is_partially_closed_not_silently_promoted() -> None:
    gaps = load_yaml("data/historical-route/stage5bj-source-gap-update.yaml")
    gap = next(
        record
        for record in gaps["records"]
        if record["gap_id"] == "stage5bi-fandom-2014-page-body-not-hash-locked"
    )

    assert gap["closure_status"] == "partially_closed_more_specific_gap_remains"
    assert gap["carried_forward"] is True
    assert gap["blocks_future_token_block_execution"] is True
