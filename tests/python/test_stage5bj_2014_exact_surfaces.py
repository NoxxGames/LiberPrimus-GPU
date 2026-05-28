from test_stage5bj_crosswalk_closure import load_yaml


def test_three_2014_surfaces_are_locked_exactly_once() -> None:
    payload = load_yaml("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml")
    records = payload["records"]

    assert payload["surface_lock_target_count"] == 3
    assert payload["exact_512_hex_surface_locked_count"] == 3
    assert len({record["surface_id"] for record in records}) == 3
    for record in records:
        assert record["surface_source_lock_status"] == "exact_512_hex_surface_locked_by_archive_path_and_hash"
        assert record["exact_512_hex_count"] == 1
        assert record["exact_surface_hex_length"] == 512
        assert record["exact_surface_sha256"]
        assert record["full_surface_body_committed"] is False
        assert record["combination_with_page49_51_allowed"] is False
        assert record["hash_search_performed"] is False
        assert record["decode_attempt_performed"] is False
        assert record["solve_claim"] is False


def test_1033_and_3301_surfaces_are_not_closed_by_media_files() -> None:
    payload = load_yaml("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml")
    by_id = {record["surface_id"]: record for record in payload["records"]}

    assert not by_id["stage5bi-c02-2014-1033-hex-surface"]["archive_path"].endswith("1033.jpg")
    assert not by_id["stage5bi-c03-2014-3301-hex-surface"]["archive_path"].lower().endswith(".mp3")
