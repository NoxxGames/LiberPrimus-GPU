from pathlib import Path

import yaml


def test_stage5bd_null_control_counters_are_plan_metadata() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-null-control-plan-counters.yaml").read_text())

    assert payload["null_control_family_count"] == 6
    assert payload["counter_mode"] == "metadata_only_plan_space"
    assert payload["controls_executed"] is False
