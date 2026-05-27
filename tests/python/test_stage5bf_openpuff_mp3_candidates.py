from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_openpuff_mp3_candidates_do_not_execute_tools() -> None:
    payload = load_yaml("data/historical-route/stage5bf-openpuff-mp3-candidates.yaml")
    families = {family for candidate in payload["candidates"] for family in candidate["artifact_families"]}

    assert payload["candidate_count"] == 7
    assert payload["interconnectedness_present"] is True
    assert "interconnectedness_mp3_candidate" in families
    assert payload["openpuff_execution_performed"] is False
    assert payload["mp3stego_execution_performed"] is False
