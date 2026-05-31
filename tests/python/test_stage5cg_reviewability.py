from test_stage5cg_common import load_yaml


def test_stage5cg_reviewability_records_findings_and_gaps() -> None:
    findings = load_yaml("data/project-state/stage5cg-stage5cf-findings-integration.yaml")
    gaps = load_yaml("data/project-state/stage5cg-reviewability-gap-register.yaml")
    source_digest = load_yaml("data/project-state/stage5cg-reviewable-source-digest-index.yaml")
    next_stage = load_yaml("data/project-state/stage5cg-next-stage-decision.yaml")

    assert findings["stage5cf_verdict"] == "accept_with_warnings"
    assert findings["warnings_are_gate_openers"] is False
    assert gaps["reviewability_gap_status"] == "non_gate_opening_warnings_recorded"
    assert source_digest["source_digest_duplicate_path_count"] == 0
    assert next_stage["selected_next_stage_id"] == "stage-5ch"
    assert next_stage["selected_next_stage_authorizes_execution"] is False
