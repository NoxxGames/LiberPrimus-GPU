from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_outguess_positive_controls_are_candidates_not_executions() -> None:
    payload = load_yaml("data/historical-route/stage5bf-outguess-positive-control-candidates.yaml")

    assert payload["candidate_count"] == 61
    assert payload["ready_positive_control_count"] == 0
    assert payload["execution_performed"] is False
    assert payload["outguess_execution_performed"] is False
    assert all(candidate["raw_commit_allowed"] is False for candidate in payload["candidates"])
