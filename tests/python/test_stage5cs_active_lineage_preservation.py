from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_preserves_correct_active_lineage() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-active-lineage-preservation.yaml")
    assert payload["active_lineage_record_count"] == 8
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["deprecated_stage5aw_path_absent"] is True
