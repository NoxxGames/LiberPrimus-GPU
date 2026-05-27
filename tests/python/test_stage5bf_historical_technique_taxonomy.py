from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_historical_technique_taxonomy_is_blocked_or_control_only() -> None:
    payload = load_yaml("data/historical-route/stage5bf-historical-technique-taxonomy.yaml")
    techniques = {record["technique"]: record for record in payload["techniques"]}

    assert "stego" in payload["technique_categories"]
    assert techniques["outguess_source_image_candidate"]["historical_source_count"] == 55
    assert techniques["mp3stego_candidate"]["execution_status"] == "blocked_or_positive_control_only"
    assert all(record["execution_status"] == "blocked_or_positive_control_only" for record in payload["techniques"])
