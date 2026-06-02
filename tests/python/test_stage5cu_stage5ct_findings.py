from libreprimus.token_block.stage5cu import STAGE5CT_FINDINGS, validate_stage5cu_stage5ct_findings

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_integrates_stage5ct_accept_with_warnings() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/project-state/stage5cu-stage5ct-findings-integration.yaml")
    assert payload["stage5ct_verdict"] == "accept_with_warnings"
    assert set(payload["findings"]) == set(STAGE5CT_FINDINGS)
    counts, errors = validate_stage5cu_stage5ct_findings()
    assert not errors
    assert counts["stage5cu_stage5ct_findings_valid"] is True
