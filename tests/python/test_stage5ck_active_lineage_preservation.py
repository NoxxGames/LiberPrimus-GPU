from libreprimus.token_block.stage5ca import CORRECT_STAGE5AW_PATH, INCORRECT_STAGE5AW_PATH

from test_stage5ck_common import load_yaml


def test_active_lineage_preserves_eight_current_records() -> None:
    payload = load_yaml("data/token-block/stage5ck-active-lineage-preservation.yaml")
    paths = [record["path"] for record in payload["lineage_records"]]
    assert payload["active_lineage_record_count"] == 8
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["deprecated_stage5aw_path_absent"] is True
    assert CORRECT_STAGE5AW_PATH in paths
    assert INCORRECT_STAGE5AW_PATH not in paths
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
