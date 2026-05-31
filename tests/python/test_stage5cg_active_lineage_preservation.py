from libreprimus.token_block.stage5ca import CORRECT_STAGE5AW_PATH, INCORRECT_STAGE5AW_PATH
from test_stage5cg_common import load_yaml


def test_stage5cg_preserves_active_lineage_paths() -> None:
    payload = load_yaml("data/token-block/stage5cg-active-lineage-preservation.yaml")
    paths = {record["path"] for record in payload["lineage_records"]}
    assert payload["active_lineage_record_count"] == 8
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["deprecated_stage5aw_path_absent"] is True
    assert CORRECT_STAGE5AW_PATH in paths
    assert INCORRECT_STAGE5AW_PATH not in paths
