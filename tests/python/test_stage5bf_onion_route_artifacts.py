from test_stage5bf_local_archive_location import assert_stage5bf_metadata_only, load_yaml


def test_stage5bf_onion_route_artifacts_are_not_live_route_fetches() -> None:
    payload = load_yaml("data/historical-route/stage5bf-onion-route-artifacts.yaml")

    assert payload["candidate_count"] == 293
    assert payload["source_lock_only"] is True
    assert any(artifact["text_metadata"]["onion_url_count"] > 0 for artifact in payload["artifacts"])
    assert_stage5bf_metadata_only(payload)
