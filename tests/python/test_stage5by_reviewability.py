from test_stage5by_common import load_yaml


def test_stage5by_reviewability_records_exist_and_route_to_stage5bz() -> None:
    findings = load_yaml("data/project-state/stage5by-stage5bx-findings-integration.yaml")
    evidence = load_yaml("data/project-state/stage5by-reviewable-validation-evidence.yaml")
    decision = load_yaml("data/project-state/stage5by-next-stage-decision.yaml")
    assert findings["stage5bx_verdict"] == "accept_with_warnings"
    assert findings["stage5bx_warning_count"] == 3
    assert evidence["stage5ax_parallel_validation_used"] is True
    assert evidence["codex_completion_summary_path"] == "codex-output/stage5by-codex-completion.md"
    assert decision["selected_next_stage_id"] == "stage-5bz"
