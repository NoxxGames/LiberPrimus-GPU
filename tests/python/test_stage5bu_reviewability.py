from test_stage5bu_common import load_yaml


def test_stage5bu_reviewability_records_stage5bt_and_external_gaps() -> None:
    findings = load_yaml("data/project-state/stage5bu-stage5bt-findings-integration.yaml")
    gaps = load_yaml("data/project-state/stage5bu-reviewability-gap-register.yaml")
    evidence = load_yaml("data/project-state/stage5bu-reviewable-validation-evidence.yaml")

    assert findings["stage5bt_verdict"] == "accept_with_warnings"
    assert gaps["lineage_path_gap_closed"] is True
    assert gaps["incorrect_stage5aw_path_gap_closed"] is True
    command_ids = {row["command_id"] for row in evidence["validation_commands"]}
    assert "stage5bu_validator" in command_ids
    assert "stage5bs_validator" in command_ids
