from test_stage5bw_common import load_yaml


def test_stage5bw_sidecar_proposal_exists_but_inactive() -> None:
    proposal = load_yaml("data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml")

    assert proposal["string4_inactive_sidecar_planning_ingestion_proposal_created"] is True
    assert proposal["string4_inactive_sidecar_planning_ingestion_activated"] is False
    assert proposal["proposal_active"] is False
    assert proposal["proposal_ingests_bytes"] is False
    assert proposal["proposal_changes_current_plans"] is False
    assert proposal["level_2_future_active_planning_input"]["future_active_planning_input_authorized_now"] is False


def test_stage5bv_verdict_integrated() -> None:
    findings = load_yaml("data/project-state/stage5bw-stage5bv-findings-integration.yaml")
    assert findings["stage5bv_verdict"] == "accept_with_warnings"
    assert findings["stage5bu_repair_accepted"] is True
