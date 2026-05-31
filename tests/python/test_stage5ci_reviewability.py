from test_stage5ci_common import load_yaml


def test_stage5ci_reviewability_gaps_are_non_gate_opening() -> None:
    payload = load_yaml("data/project-state/stage5ci-reviewability-gap-register.yaml")
    gaps = {gap["gap_id"]: gap for gap in payload["gaps"]}
    assert gaps["public_github_issue_ci_external_or_unavailable"]["gate_opener"] is False
    assert gaps["attached_zip_not_pristine_checkout"]["gate_opener"] is False
    assert gaps["active_planning_input_scaffold_minimalist"]["disposition"] == (
        "closed_by_stage5ci_template_hardening"
    )
    assert gaps["final_commit_self_embedding"]["severity"] == "expected_external_evidence"


def test_stage5ci_next_stage_is_deep_research_review_without_execution() -> None:
    payload = load_yaml("data/project-state/stage5ci-next-stage-decision.yaml")
    assert payload["selected_next_stage_id"] == "stage-5cj"
    assert payload["selected_next_prompt_type"] == "deep_research_review"
    assert payload["selected_next_stage_authorizes_execution"] is False
