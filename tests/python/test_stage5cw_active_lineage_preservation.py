from libreprimus.token_block.stage5ca import CORRECT_STAGE5AW_PATH, INCORRECT_STAGE5AW_PATH

from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_preserves_active_lineage_and_correct_stage5aw_path() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-active-lineage-preservation.yaml")
    paths = {record["path"] for record in payload["active_lineage_records"]}

    assert payload["active_lineage_record_count"] == 8
    assert payload["all_lineage_paths_resolve"] is True
    assert CORRECT_STAGE5AW_PATH in paths
    assert INCORRECT_STAGE5AW_PATH not in paths
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
