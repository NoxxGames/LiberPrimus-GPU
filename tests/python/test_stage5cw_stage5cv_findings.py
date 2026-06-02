from libreprimus.token_block.stage5cw import STAGE5CV_FINDINGS

from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_integrates_stage5cv_accept_with_warnings() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/project-state/stage5cw-stage5cv-findings-integration.yaml")

    assert payload["stage5cv_verdict"] == "accept_with_warnings"
    assert payload["stage5cv_findings_integrated"] is True
    assert set(payload["findings"]) == set(STAGE5CV_FINDINGS)
    assert payload["stage5cv_did_not_recommend_execution"] is True
    assert payload["execution_allowed"] is False
