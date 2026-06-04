from __future__ import annotations

from test_stage5de_common import ensure_stage5de_built, load_yaml


def test_stage5de_integrates_stage5dd_accept_with_warnings() -> None:
    ensure_stage5de_built()
    findings = load_yaml("data/project-state/stage5de-stage5dd-findings-integration.yaml")

    assert findings["stage5dd_findings_integrated"] is True
    assert findings["stage5dd_verdict"] == "accept_with_warnings"
    assert findings["stage5dc_commit_verified"] == "95d295e77864755900a4b909f0d660ac2b42a809"
    assert findings["stage5dc_selected_option_verified"] == "prepare_real_operator_approval_record"
    assert findings["stage5dc_real_approval_absent_verified"] is True


def test_stage5de_records_label_anomaly_as_non_gate_opening() -> None:
    ensure_stage5de_built()
    anomaly = load_yaml("data/project-state/stage5de-review-label-anomaly.yaml")

    assert anomaly["review_label_anomaly_record_created"] is True
    assert anomaly["expected_review_subject"] == "stage-5dc"
    assert anomaly["gate_opening"] is False
    assert anomaly["activation_defect"] is False
    assert anomaly["requires_generic_preflight_layer"] is False
