from libreprimus.token_block.stage5ca import CORRECT_STAGE5AW_PATH, INCORRECT_STAGE5AW_PATH
from libreprimus.token_block.stage5co import validate_stage5co_actual_record_rejection

from test_stage5co_common import load_yaml


def test_stage5co_active_lineage_preserves_correct_stage5aw_path() -> None:
    payload = load_yaml("data/token-block/stage5co-active-lineage-preservation.yaml")
    assert payload["active_lineage_record_count"] == 8
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["deprecated_stage5aw_path_absent"] is True
    paths = {record["path"] for record in payload["active_lineage_records"]}
    assert CORRECT_STAGE5AW_PATH in paths
    assert INCORRECT_STAGE5AW_PATH not in paths


def test_stage5co_rejects_deprecated_stage5aw_path() -> None:
    errors = validate_stage5co_actual_record_rejection({"path": INCORRECT_STAGE5AW_PATH})
    assert errors
