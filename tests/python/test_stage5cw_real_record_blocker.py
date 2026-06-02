from libreprimus.token_block.stage5cu import FUTURE_REAL_RECORD_CLASSES

from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_real_record_blocker_blocks_all_real_record_classes() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-real-record-creation-blocker.yaml")

    assert payload["real_record_creation_blocker_status"] == "active"
    assert set(payload["blocked_current_stage_real_records"]) == set(FUTURE_REAL_RECORD_CLASSES)
    assert payload["future_real_records_created_now"] is False
    assert payload["real_operator_decision_record_created_now"] is False
    assert payload["real_operator_approval_record_created_now"] is False
