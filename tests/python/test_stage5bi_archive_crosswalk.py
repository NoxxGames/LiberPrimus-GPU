from test_stage5bi_fandom_page_triage import load_yaml


def test_stage5bi_archive_crosswalk_prefers_local_archive_metadata() -> None:
    payload = load_yaml("data/historical-route/stage5bi-original-archive-crosswalk-candidates.yaml")
    statuses = {record["archive_crosswalk_status"] for record in payload["records"]}

    assert payload["candidate_count"] == len(payload["records"])
    assert payload["verified_archive_crosswalk_count"] >= 1
    assert "original_archive_equivalent_found" in statuses
    assert "probable_archive_path_candidate" in statuses
    assert all(record["preferred_archive_root"] == "third_party/CicadaSolversIddqd" for record in payload["records"])
    assert all(record["raw_archive_files_committed"] is False for record in payload["records"])
    assert all(record["execution_allowed"] is False for record in payload["records"])
