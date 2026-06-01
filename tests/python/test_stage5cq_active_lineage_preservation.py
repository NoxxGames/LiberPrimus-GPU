from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_active_lineage_preserves_correct_stage5aw_path() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/token-block/stage5cq-active-lineage-preservation.yaml")
    assert payload["active_lineage_record_count"] == 8
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["deprecated_stage5aw_path_absent"] is True
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
