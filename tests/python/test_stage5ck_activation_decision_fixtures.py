from libreprimus.token_block.stage5ck import ACTIVATION_DECISION_FIXTURE_CASES

from test_stage5ck_common import load_yaml


def test_activation_decision_fixtures_are_invalid_now() -> None:
    payload = load_yaml("data/token-block/stage5ck-activation-decision-fixture-pack.yaml")
    assert payload["activation_decision_fixture_records_created"] is True
    assert payload["actual_activation_decision_records_created"] is False
    assert payload["activation_decision_fixture_records_valid_now"] is False
    assert set(ACTIVATION_DECISION_FIXTURE_CASES) <= set(payload["fixture_cases"])
    for fixture in payload["fixture_records"]:
        assert fixture["fixture_only"] is True
        assert fixture["actual_activation_decision_record"] is False
        assert fixture["may_authorize_active_input"] is False
