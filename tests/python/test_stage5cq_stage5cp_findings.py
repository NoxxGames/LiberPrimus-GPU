from libreprimus.token_block.stage5cq import STAGE5CP_FINDINGS, validate_stage5cq_stage5cp_findings

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_stage5cp_findings_are_integrated() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/project-state/stage5cq-stage5cp-findings-integration.yaml")
    assert payload["stage5cp_verdict"] == "accept_with_warnings"
    assert set(STAGE5CP_FINDINGS).issubset(set(payload["findings"]))
    counts, errors = validate_stage5cq_stage5cp_findings()
    assert not errors
    assert counts["stage5cq_stage5cp_findings_valid"] is True
