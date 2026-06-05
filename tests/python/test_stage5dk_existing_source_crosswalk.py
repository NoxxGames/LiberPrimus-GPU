from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, load_yaml, write_temp_yaml


def test_stage5dk_crosswalk_marks_stage5di_and_malformed_old_urls() -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/source-harvester/stage5dk-existing-source-index-crosswalk.yaml")
    rows = {row["source_key"]: row for row in record["crosswalk_records"]}

    for key in stage5dk.STAGE5DI_LOCKED_KEYS:
        assert (
            rows[key]["prior_source_index_status"]
            == "already_stage5di_source_locked_and_stage5dk_refreshed_or_cross_referenced"
        )
    for key in stage5dk.OLD_INDEX_TRUNCATED_KEYS:
        assert rows[key]["old_index_url_malformed_or_truncated"] is True
        assert rows[key]["stage5dk_canonical_url_corrected"] is True
        assert rows[key]["old_index_url"] != rows[key]["canonical_url"]
    assert all(row["stage5aj_index_only_was_sufficient"] is False for row in rows.values())


def test_stage5dk_crosswalk_validator_rejects_stage5aj_sufficient_flag(
    monkeypatch: object,
    tmp_path,
) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/source-harvester/stage5dk-existing-source-index-crosswalk.yaml")
    record["crosswalk_records"][0]["stage5aj_index_only_was_sufficient"] = True
    path = write_temp_yaml(tmp_path / "crosswalk.yaml", record)

    monkeypatch.setitem(stage5dk.DATA_PATHS, "existing_source_index_crosswalk", path)

    result = stage5dk.validate_stage5dk_existing_source_crosswalk()
    assert result.validation_error_count > 0
    assert any("stage5aj_index_only_must_not_be_sufficient" in error for error in result.errors)
