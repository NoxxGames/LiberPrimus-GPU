from test_stage5bf_local_archive_location import assert_stage5bf_metadata_only, load_yaml


def test_stage5bf_liber_primus_artifacts_are_historical_not_canonical() -> None:
    payload = load_yaml("data/historical-route/stage5bf-liber-primus-historical-artifacts.yaml")
    families = {family for artifact in payload["artifacts"] for family in artifact["artifact_families"]}

    assert payload["candidate_count"] == 257
    assert "liber_primus_page_image" in families
    assert "liber_primus_rune_text" in families
    assert_stage5bf_metadata_only(payload)
