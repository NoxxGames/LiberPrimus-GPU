from libreprimus.token_block.stage5cu import FUTURE_REAL_RECORD_CLASSES, validate_stage5cu_real_record_blocker

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_real_record_blocker_covers_future_real_record_classes() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-real-record-creation-blocker.yaml")
    assert payload["real_record_creation_blocker_status"] == "active"
    assert set(payload["blocked_current_stage_real_records"]) == set(FUTURE_REAL_RECORD_CLASSES)
    assert payload["real_operator_decision_record_created_now"] is False
    assert payload["future_real_records_created_now"] is False
    counts, errors = validate_stage5cu_real_record_blocker()
    assert not errors
    assert counts["stage5cu_real_record_blocker_valid"] is True
