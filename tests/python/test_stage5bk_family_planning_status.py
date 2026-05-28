from test_stage5bk_common import load_yaml


def test_stage5bk_family_statuses_are_not_method_upgrades() -> None:
    payload = load_yaml("data/historical-route/stage5bk-historical-family-planning-status.yaml")
    assert payload["historical_family_planning_status_count"] == len(payload["records"]) == 9
    assert payload["method_status_upgraded"] is False
    assert all(record["method_status_upgrade_allowed"] is False for record in payload["records"])
    assert all(record["execution_allowed"] is False for record in payload["records"])
