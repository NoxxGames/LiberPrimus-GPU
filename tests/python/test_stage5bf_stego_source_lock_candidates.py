from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_stego_candidates_remain_blocked_metadata_only() -> None:
    payload = load_yaml("data/historical-route/stage5bf-stego-source-lock-candidates.yaml")

    assert payload["candidate_count"] == 80
    assert payload["ready_positive_control_count"] == 0
    assert payload["blocked_candidate_count"] == 80
    assert payload["stego_tool_execution_performed"] is False
    assert payload["outguess_execution_performed"] is False
    assert payload["openpuff_execution_performed"] is False
    assert payload["mp3stego_execution_performed"] is False
