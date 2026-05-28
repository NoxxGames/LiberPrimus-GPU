from test_stage5bm_common import load_yaml


def test_stage5bm_integrates_stage5bl_accept_with_warnings() -> None:
    record = load_yaml("data/project-state/stage5bm-stage5bl-findings-integration.yaml")

    assert record["stage5bl_verdict"] == "accept_with_warnings"
    assert record["stage5bl_primary_warning"] == "string4_stage5aw_branch_membership_unreconciled"
    assert "source_gap_severity_missing_string4_row" in record["stage5bl_findings_integrated"]
    assert record["execution_selected"] is False
