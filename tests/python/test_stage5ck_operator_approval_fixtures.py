from libreprimus.token_block.stage5ck import OPERATOR_FIXTURE_CASES

from test_stage5ck_common import load_yaml


def test_operator_approval_fixtures_are_unsatisfied() -> None:
    payload = load_yaml("data/token-block/stage5ck-operator-approval-fixture-pack.yaml")
    assert payload["operator_approval_fixture_records_created"] is True
    assert payload["actual_operator_approval_records_created"] is False
    assert payload["operator_approval_fixture_records_satisfy_approval"] is False
    assert set(OPERATOR_FIXTURE_CASES) <= set(payload["fixture_cases"])
    for fixture in payload["fixture_records"]:
        assert fixture["fixture_only"] is True
        assert fixture["actual_operator_approval_record"] is False
        assert fixture["may_satisfy_real_gate"] is False
