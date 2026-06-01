from libreprimus.token_block.stage5co import (
    FUTURE_REAL_RECORD_CLASSES,
    validate_stage5co_real_record_blocker,
)

from test_stage5co_common import load_yaml


def test_stage5co_real_record_creation_blocker_is_active() -> None:
    payload = load_yaml("data/token-block/stage5co-real-record-creation-blocker.yaml")
    assert payload["real_record_creation_blocker_status"] == "active"
    assert set(payload["blocked_current_stage_real_records"]) == set(FUTURE_REAL_RECORD_CLASSES)
    assert payload["future_real_records_created_now"] is False

    counts, errors = validate_stage5co_real_record_blocker()
    assert errors == []
    assert counts["stage5co_real_record_blocker_valid"] is True
