from libreprimus.token_block.stage5ck import validate_stage5ck_actual_record_rejection

from test_stage5ck_common import load_yaml


def test_fixture_isolation_policy_is_non_authorising() -> None:
    payload = load_yaml("data/token-block/stage5ck-fixture-isolation-policy.yaml")
    assert payload["fixture_pack_only"] is True
    assert payload["synthetic_negative_fixtures_only"] is True
    assert payload["real_approval_records_created"] is False
    assert payload["real_activation_decision_records_created"] is False
    assert payload["fixtures_may_satisfy_real_gate"] is False
    assert payload["fixtures_may_authorize_activation"] is False
    assert payload["fixtures_may_authorize_execution"] is False


def test_fixture_payload_is_rejected_as_actual_record() -> None:
    payload = load_yaml("data/token-block/stage5ck-operator-approval-fixture-pack.yaml")
    fixture = payload["fixture_records"][0]
    errors = validate_stage5ck_actual_record_rejection(fixture)
    assert errors
