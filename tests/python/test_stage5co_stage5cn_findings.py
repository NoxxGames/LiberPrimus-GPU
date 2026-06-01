from libreprimus.token_block.stage5co import STAGE5CN_FINDINGS, validate_stage5co_stage5cn_findings

from test_stage5co_common import load_yaml


def test_stage5co_stage5cn_findings_are_integrated() -> None:
    payload = load_yaml("data/project-state/stage5co-stage5cn-findings-integration.yaml")
    assert payload["stage5cn_findings_integrated"] is True
    assert payload["stage5cn_verdict"] == "accept_with_warnings"
    assert set(STAGE5CN_FINDINGS).issubset(payload["findings"])

    counts, errors = validate_stage5co_stage5cn_findings()
    assert errors == []
    assert counts["stage5co_stage5cn_findings_valid"] is True
