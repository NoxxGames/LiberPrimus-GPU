from libreprimus.token_block.stage5cs import STAGE5CR_FINDINGS, validate_stage5cs_stage5cr_findings

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_integrates_stage5cr_accept_with_warnings() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/project-state/stage5cs-stage5cr-findings-integration.yaml")
    assert payload["stage5cr_verdict"] == "accept_with_warnings"
    assert set(STAGE5CR_FINDINGS) <= set(payload["findings"])
    counts, errors = validate_stage5cs_stage5cr_findings()
    assert not errors
    assert counts["stage5cs_stage5cr_findings_valid"] is True
