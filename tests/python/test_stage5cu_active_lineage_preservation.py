from libreprimus.token_block.stage5ca import CORRECT_STAGE5AW_PATH, INCORRECT_STAGE5AW_PATH

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_preserves_correct_active_lineage() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-active-lineage-preservation.yaml")
    paths = {record["path"] for record in payload["active_lineage_records"]}
    assert payload["active_lineage_record_count"] == 8
    assert CORRECT_STAGE5AW_PATH in paths
    assert INCORRECT_STAGE5AW_PATH not in paths
    assert payload["active_token_block_manifest_changed"] is False
