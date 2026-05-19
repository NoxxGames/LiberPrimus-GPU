from __future__ import annotations

from libreprimus.stego_positive_controls.cache_policy import build_cache_record


def test_stage4n_cache_policy_rejects_committed_raw_defaults(tmp_path) -> None:
    record = {"fixture_id": "fixture", "source_path": "fixture.mp3", "local_availability": "source_only"}
    cache = build_cache_record(record, category="mp3_instar_candidate", cache_dir=tmp_path, source_kind="audio")
    assert cache["cache_policy"] == "cache_candidate"
    assert cache["audio_committed"] is False
    assert cache["image_committed"] is False
    assert cache["binary_committed"] is False
    assert cache["archive_committed"] is False
