from libreprimus.token_block.stage5cq import FUTURE_REAL_RECORD_CLASSES, validate_stage5cq_real_record_blocker

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_real_record_creation_blocker_is_active() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/token-block/stage5cq-real-record-creation-blocker.yaml")
    assert payload["real_record_creation_blocker_status"] == "active"
    assert set(payload["blocked_current_stage_real_records"]) == set(FUTURE_REAL_RECORD_CLASSES)
    assert payload["operator_decision_record_created_now"] is False
    assert payload["real_operator_approval_record_created_now"] is False
    counts, errors = validate_stage5cq_real_record_blocker()
    assert not errors
    assert counts["stage5cq_real_record_blocker_valid"] is True
