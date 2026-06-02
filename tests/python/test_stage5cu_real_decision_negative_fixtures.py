from libreprimus.token_block.stage5cu import (
    FUTURE_REAL_RECORD_CLASSES,
    validate_stage5cu_real_decision_negative_fixtures,
)

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_real_decision_negative_fixtures_cover_all_future_real_classes() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-real-decision-record-negative-fixture-pack.yaml")
    assert payload["real_decision_negative_fixture_count"] == len(FUTURE_REAL_RECORD_CLASSES)
    assert {fixture["target_real_record_class"] for fixture in payload["fixtures"]} == set(
        FUTURE_REAL_RECORD_CLASSES
    )
    for fixture in payload["fixtures"]:
        assert fixture["fixture_only"] is True
        assert fixture["created_now"] is False
        assert fixture["present_now"] is False
        assert fixture["satisfied_now"] is False
        assert fixture["may_satisfy_real_gate"] is False
    counts, errors = validate_stage5cu_real_decision_negative_fixtures()
    assert not errors
    assert counts["stage5cu_real_decision_negative_fixtures_valid"] is True
