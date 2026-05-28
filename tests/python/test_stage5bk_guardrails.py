from test_stage5bk_common import assert_no_forbidden_true, load_yaml


def test_stage5bk_guardrails_reject_forbidden_work() -> None:
    payload = load_yaml("data/historical-route/stage5bk-guardrail.yaml")
    assert payload["planning_constraint_integration_only"] is True
    assert payload["metadata_only"] is True
    assert_no_forbidden_true(payload)
