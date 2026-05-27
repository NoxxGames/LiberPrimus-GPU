from test_stage5bf_local_archive_location import assert_stage5bf_metadata_only, load_yaml


def test_stage5bf_book_code_artifacts_require_review_before_token_planning() -> None:
    payload = load_yaml("data/historical-route/stage5bf-book-code-artifacts.yaml")

    assert payload["candidate_count"] == 14
    assert payload["source_lock_only"] is True
    assert any(
        artifact["token_block_planning_relevance"] == "review_required_before_future_token_block_planning"
        for artifact in payload["artifacts"]
    )
    assert_stage5bf_metadata_only(payload)
