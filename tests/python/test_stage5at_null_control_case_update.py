from pathlib import Path

import yaml


def test_stage5at_null_control_case_update_adds_controls() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-null-control-case-update.yaml").read_text())
    assert payload["case_decision_controls_added"] is True
    assert payload["review_bias_controls_added"] is True
    assert payload["value_sensitivity_controls_added"] is True
    assert payload["execution_enabled"] is False
    assert payload["no_decode"] is True
