from test_stage5bf_local_archive_location import assert_stage5bf_metadata_only, load_yaml


def test_stage5bf_magic_square_artifacts_are_source_lock_only() -> None:
    payload = load_yaml("data/historical-route/stage5bf-magic-square-artifacts.yaml")

    assert payload["candidate_count"] == 7
    assert payload["source_lock_only"] is True
    assert any("magic_square" in artifact["artifact_families"] for artifact in payload["artifacts"])
    assert_stage5bf_metadata_only(payload)
