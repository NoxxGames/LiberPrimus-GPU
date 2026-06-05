from __future__ import annotations

from libreprimus.token_block.stage5di import (
    SOURCE_FAMILY_IDS,
    WEB_SOURCES,
    validate_stage5di_local_archive_crosswalk,
    validate_stage5di_number_triangle_crosswalk,
    validate_stage5di_source_lock_register,
)

from test_stage5di_common import ensure_stage5di_built, load_yaml, write_temp_yaml


def test_stage5di_required_web_and_local_source_locks_exist() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di_source_lock_register()

    assert errors == []
    assert counts["source_family_count"] == len(SOURCE_FAMILY_IDS)
    assert counts["web_source_lock_count"] == len(WEB_SOURCES)
    assert counts["local_archive_source_lock_count"] == 11

    web = load_yaml("data/source-harvester/stage5di-web-source-lock-register.yaml")
    urls = {source["url"] for source in web["sources"]}
    assert "https://uncovering-cicada.fandom.com/wiki/2016_Message" in urls
    assert "https://github.com/tweqx/3301-hash-alarm" in urls
    assert all(source["raw_body_committed"] is False for source in web["sources"])


def test_stage5di_local_archive_crosswalk_records_provided_paths() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di_local_archive_crosswalk()

    assert errors == []
    assert counts["crosswalk_count"] == 5

    payload = load_yaml("data/source-harvester/stage5di-cicada-solvers-iddqd-v2-crosswalk.yaml")
    assert set(payload["local_archive_root_candidates"]) == {
        "third_party/CiadaSolversIddqd_v2",
        "third_party/CicadaSolversIddqd_v2",
    }
    assert payload["found_in_repo_path"] in {None, "third_party/CiadaSolversIddqd_v2"}
    assert payload["raw_archive_committed"] is False
    for row in payload["crosswalks"]:
        assert row["local_paths"]
        assert all(path_row["path"].startswith("third_party/") for path_row in row["local_paths"])
    assert counts["root_exists"] in {True, False}
    assert counts["alternate_root_exists"] in {True, False}


def test_stage5di_number_triangle_bundle_records_messages_and_images() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di_number_triangle_crosswalk()

    assert errors == []
    payload = load_yaml(
        "data/source-harvester/stage5di-number-triangle-theory-bundle-crosswalk.yaml"
    )
    expected_root = "third_party/UsefulFilesAndIdeas/number-triangle-theory"
    assert payload["operator_path"] == expected_root
    assert payload["bundle_root"] == expected_root
    assert payload["full_forum_text_committed_in_stage5di"] is False
    assert payload["cross_check_against_iddqd_transcription_status"]
    if counts["bundle_root_exists"] is True:
        assert counts["message_file_count"] >= 1
        assert counts["image_file_count"] >= 1
    else:
        assert counts["message_file_count"] == 0
        assert counts["image_file_count"] == 0


def test_stage5di_source_lock_register_rejects_missing_required_family(tmp_path) -> None:
    ensure_stage5di_built()
    payload = load_yaml("data/project-state/stage5di-recent-clue-source-lock-register.yaml")
    payload["source_family_ids"] = [
        family for family in payload["source_family_ids"] if family != SOURCE_FAMILY_IDS[0]
    ]
    temp = write_temp_yaml(tmp_path / "source-lock-register.yaml", payload)

    _, errors = validate_stage5di_source_lock_register(register=temp)

    assert errors
    assert any(error.startswith("missing_source_family:") for error in errors)
