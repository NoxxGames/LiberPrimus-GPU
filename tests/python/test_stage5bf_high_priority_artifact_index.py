from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_high_priority_index_has_metadata_only_artifacts() -> None:
    payload = load_yaml("data/historical-route/stage5bf-high-priority-artifact-index.yaml")
    first = payload["artifacts"][0]
    families = {family for artifact in payload["artifacts"] for family in artifact["artifact_families"]}

    assert payload["artifact_count"] == 1043
    assert payload["raw_archive_files_committed"] is False
    assert first["sha256"]
    assert first["raw_commit_allowed"] is False
    assert "pgp_signed_message" in families
    assert "outguess_source_image_candidate" in families
    assert "liber_primus_page_image" in families
