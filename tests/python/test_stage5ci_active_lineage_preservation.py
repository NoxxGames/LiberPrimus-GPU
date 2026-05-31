from libreprimus.token_block.stage5ci import validate_stage5ci
from test_stage5ci_common import load_yaml, write_yaml


def test_stage5ci_active_lineage_has_exactly_eight_records() -> None:
    payload = load_yaml("data/token-block/stage5ci-active-lineage-preservation.yaml")
    assert payload["active_lineage_record_count"] == 8
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["deprecated_stage5aw_path_absent"] is True
    assert len(payload["lineage_records"]) == 8
    assert all(record["present"] for record in payload["lineage_records"])


def test_stage5ci_deprecated_stage5aw_path_fails(tmp_path) -> None:
    payload = load_yaml("data/token-block/stage5ci-active-lineage-preservation.yaml")
    payload["lineage_records"][0]["path"] = "data/token-block/stage5aw-repaired-branch-manifest.yaml"
    bad = tmp_path / "lineage.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci(active_lineage=bad)
    assert bad_errors
