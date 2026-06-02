from libreprimus.token_block.stage5cu import (
    NEGATIVE_FIXTURE_IDS,
    validate_stage5cu_decision_option_negative_fixtures,
)

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_decision_option_negative_fixtures_are_exact_and_gate_closed() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-decision-option-negative-fixture-pack.yaml")
    assert payload["negative_fixture_count"] == 41
    assert set(payload["negative_fixture_ids"]) == set(NEGATIVE_FIXTURE_IDS)
    assert payload["operator_decision_option_selected_now"] is False
    for fixture in payload["fixtures"]:
        assert fixture["fixture_only"] is True
        assert fixture["synthetic_negative_fixture"] is True
        assert fixture["may_satisfy_real_gate"] is False
        assert fixture["may_authorize_execution"] is False
        assert fixture["selected_option_id"] is None
    counts, errors = validate_stage5cu_decision_option_negative_fixtures()
    assert not errors
    assert counts["stage5cu_decision_option_negative_fixtures_valid"] is True
