from test_stage5bo_common import load_yaml


def test_stage5bo_source_gap_closes_for_metadata_planning_only() -> None:
    payload = load_yaml("data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml")
    severity = load_yaml("data/historical-route/stage5bo-source-gap-severity-update.yaml")

    assert payload["closure_status_after_errata"] == "closed_operator_errata_supported_full_branch_match"
    assert payload["blocks_metadata_planning"] is False
    assert payload["blocks_string4_ingestion_or_active_use"] is True
    assert payload["blocks_future_token_block_execution"] is True
    assert payload["string4_active_input_allowed"] is False
    assert severity["string4_gap_status_after_errata"] == payload["closure_status_after_errata"]
