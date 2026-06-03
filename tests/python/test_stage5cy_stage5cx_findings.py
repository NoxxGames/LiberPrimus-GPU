from test_stage5cy_common import ensure_stage5cy_built, load_yaml


def test_stage5cy_integrates_stage5cx_verdict_and_findings() -> None:
    ensure_stage5cy_built()
    findings = load_yaml("data/project-state/stage5cy-stage5cx-findings-integration.yaml")

    assert findings["stage5cx_verdict"] == "accept_with_warnings"
    assert findings["stage5cx_findings_integrated"] is True
    assert findings["finding_count"] == 26
    assert "stage5cw_pytest_count_reviewability_warning_2446_vs_2466" in findings["findings"]
    assert findings["stage5cx_did_not_recommend_execution"] is True
    assert findings["stage5cx_did_not_recommend_option_selection"] is True
