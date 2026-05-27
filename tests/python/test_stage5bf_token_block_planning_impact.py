from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_token_block_planning_impact_keeps_execution_blocked() -> None:
    payload = load_yaml("data/historical-route/stage5bf-token-block-planning-impact.yaml")

    assert payload["historical_corpus_source_locked"] == "partial"
    assert payload["token_block_planning_should_pause_for_historical_review"] is True
    assert payload["do_not_change_current_token_block_records"] is True
    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
