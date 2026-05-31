from test_stage5ck_common import load_yaml


def test_stage5cj_findings_and_gaps_are_reviewable() -> None:
    findings = load_yaml("data/project-state/stage5ck-stage5cj-findings-integration.yaml")
    gaps = load_yaml("data/project-state/stage5ck-reviewability-gap-register.yaml")
    assert findings["stage5cj_findings_integrated"] is True
    assert findings["stage5cj_verdict"] == "accept_with_warnings"
    assert findings["warnings_gate_opening"] is False
    gap_ids = {gap["gap_id"] for gap in gaps["gaps"]}
    assert "attached_zip_not_pristine_checkout" in gap_ids
    assert "public_github_corroboration_unreliable" in gap_ids
    assert gaps["gate_opening_gap_count"] == 0


def test_stage5ck_next_stage_is_deep_research_review() -> None:
    payload = load_yaml("data/project-state/stage5ck-next-stage-decision.yaml")
    assert payload["selected_next_stage_id"] == "stage-5cl"
    assert payload["selected_next_prompt_type"] == "deep_research_review"
    assert payload["selected_next_stage_authorizes_execution"] is False
