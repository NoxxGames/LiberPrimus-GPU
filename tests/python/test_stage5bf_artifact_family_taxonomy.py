from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_artifact_family_taxonomy_records_expected_families() -> None:
    payload = load_yaml("data/historical-route/stage5bf-artifact-family-taxonomy.yaml")

    assert "outguess_source_image_candidate" in payload["known_artifact_families"]
    assert "openpuff_source_audio_candidate" in payload["known_artifact_families"]
    assert "hex_to_jpeg_extraction" in payload["known_artifact_families"]
    assert payload["family_counts"]["onion_url"] == 293
    assert payload["family_counts"]["jpeg_sequence"] == 586
    assert payload["historical_source_lock_only"] is True
    assert payload["execution_performed"] is False
