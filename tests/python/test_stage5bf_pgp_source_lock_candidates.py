from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_pgp_candidates_are_not_verified_or_keyserver_fetched() -> None:
    payload = load_yaml("data/historical-route/stage5bf-pgp-source-lock-candidates.yaml")

    assert payload["pgp_candidate_count"] == 96
    assert payload["pgp_block_present_count"] == 80
    assert payload["verification_performed"] is False
    assert payload["network_keyserver_fetch_performed"] is False
    assert {candidate["verification_status"] for candidate in payload["candidates"]} == {"not_verified_by_stage5bf"}
