from pathlib import Path

import yaml


def test_stage5ay_null_control_families_defined_not_executed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-null-control-family-manifest.yaml").read_text(encoding="utf-8"))

    assert payload["null_controls_defined_before_execution"] is True
    assert payload["controls_executed"] is False
    assert {record["family_id"] for record in payload["families"]} >= {"case_policy_control", "random_shuffled_control"}
