from libreprimus.token_block.stage5cs import FUTURE_REAL_RECORD_CLASSES, validate_stage5cs_real_record_blocker

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_real_record_creation_blocker_covers_six_classes() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-real-record-creation-blocker.yaml")
    assert payload["real_record_creation_blocker_status"] == "active"
    assert set(payload["blocked_current_stage_real_records"]) == set(FUTURE_REAL_RECORD_CLASSES)
    assert payload["blocked_current_stage_real_record_count"] == 6
    counts, errors = validate_stage5cs_real_record_blocker()
    assert not errors
    assert counts["stage5cs_real_record_blocker_valid"] is True
