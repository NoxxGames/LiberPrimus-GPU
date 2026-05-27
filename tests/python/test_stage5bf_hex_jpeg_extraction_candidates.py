from test_stage5bf_local_archive_location import assert_stage5bf_metadata_only, load_yaml


def test_stage5bf_hex_jpeg_candidates_are_not_extracted_or_decoded() -> None:
    payload = load_yaml("data/historical-route/stage5bf-hex-jpeg-extraction-candidates.yaml")

    assert payload["candidate_count"] == 595
    assert payload["source_lock_only"] is True
    assert any("jpeg_sequence" in artifact["artifact_families"] for artifact in payload["artifacts"])
    assert_stage5bf_metadata_only(payload)
