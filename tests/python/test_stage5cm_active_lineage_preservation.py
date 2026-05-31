from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS

from test_stage5cm_common import load_yaml


def test_stage5cm_active_lineage_preservation_keeps_exact_path_set() -> None:
    payload = load_yaml("data/token-block/stage5cm-active-lineage-preservation.yaml")
    assert payload["active_lineage_record_count"] == 8
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["deprecated_stage5aw_path_absent"] is True
    assert payload["all_lineage_paths_resolve"] is True
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
    assert [record["path"] for record in payload["active_lineage_records"]] == ACTIVE_LINEAGE_PATHS
