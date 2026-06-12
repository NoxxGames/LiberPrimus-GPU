from __future__ import annotations

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_drift_audit_is_report_only() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_drift_audit_policy()
    policy = load_yaml("data/project-state/stage5ef-drift-audit-policy.yaml")
    report = stage5ef.build_doc_drift_audit_report()

    assert result.validation_error_count == 0
    assert policy["audit_default_mode"] == "report_only_no_fix"
    assert policy["generated_audit_outputs_committed"] is False
    assert report["fixes_applied"] is False
    assert report["generated_outputs_committed"] is False
