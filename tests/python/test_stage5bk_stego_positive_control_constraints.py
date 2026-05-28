from test_stage5bk_common import load_yaml


def test_stage5bk_stego_constraints_are_positive_control_only() -> None:
    payload = load_yaml("data/historical-route/stage5bk-stego-positive-control-constraint-integration.yaml")
    assert "outguess_positive_control_only" in payload["constraints"]
    assert payload["stego_tool_execution_performed"] is False
    assert payload["execution_allowed"] is False
