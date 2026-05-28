from test_stage5bj_crosswalk_closure import load_yaml


def test_media_equivalence_records_keep_fandom_media_secondary() -> None:
    payload = load_yaml("data/historical-route/stage5bj-media-equivalence-closure.yaml")

    assert payload["media_equivalence_record_count"] == len(payload["records"]) == 8
    assert payload["media_original_archive_equivalent_found_count"] == 8
    assert payload["fandom_media_is_original_source_truth"] is False
    for record in payload["records"]:
        assert record["archive_equivalent_status"] == "original_archive_equivalent_found"
        assert record["fandom_media_is_original_source_truth"] is False
        assert record["raw_media_committed"] is False
        assert record["execution_allowed"] is False
        assert record["stego_execution_allowed"] is False
        assert record["image_forensics_allowed"] is False
        assert record["audio_analysis_allowed"] is False
        assert record["solve_claim"] is False
