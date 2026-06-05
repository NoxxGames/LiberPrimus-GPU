from __future__ import annotations

from libreprimus.token_block.stage5dj import build_stage5dj_records, validate_stage5dj_music_source_lock

from test_stage5dj_common import ensure_stage5dj_built, load_yaml, write_temp_yaml


def test_stage5dj_source_lock_records_metadata_only_files() -> None:
    ensure_stage5dj_built()

    counts, errors = validate_stage5dj_music_source_lock()
    assert errors == []
    payload = load_yaml("data/project-state/stage5dj-music-source-lock-register.yaml")
    assert payload["raw_music_files_committed"] is False
    assert payload["source_root"] == "third_party/CicadaMusic"
    assert counts["music_source_file_count"] == payload["music_source_file_count"]
    for row in payload["source_records"]:
        assert row["sha256"]
        assert row["raw_music_file_committed"] is False


def test_stage5dj_absent_music_root_is_explicit(tmp_path) -> None:
    records = build_stage5dj_records(music_root=tmp_path / "missing-cicadamusic")
    register = records["music_source_lock_register"]
    assert register["source_presence_status"] == "local_ignored_cache_absent"
    assert register["music_source_file_count"] == 0
    assert register["source_records"] == []


def test_stage5dj_source_lock_validator_rejects_raw_commit_flag(tmp_path) -> None:
    ensure_stage5dj_built()
    payload = load_yaml("data/project-state/stage5dj-music-source-lock-register.yaml")
    payload["raw_music_files_committed"] = True
    temp = write_temp_yaml(tmp_path / "bad.yaml", payload)

    _, errors = validate_stage5dj_music_source_lock(record=temp)
    assert any("raw_music_files" in error for error in errors)
