from __future__ import annotations

from test_stage5eb_common import ensure_stage5eb_built, load_yaml


def test_stage5eb_current_stage_registry_uses_external_post_push_handoff_policy() -> None:
    ensure_stage5eb_built()

    current = load_yaml("data/project-state/current-stage-state.yaml")
    policy = load_yaml("data/project-state/stage5eb-current-stage-registry-finalization-policy.yaml")

    assert current["latest_completed_stage_id"] == "stage-5eb"
    assert current["recommended_next_stage_id"] == "stage-5ec"
    assert current["latest_completed_stage_commit_recording_policy"] == "external_post_push_handoff"
    assert current["latest_completed_stage_ci_status_recording_policy"] == "external_post_push_handoff"
    assert current["latest_completed_stage_commit_in_committed_registry"] == "not_applicable_self_referential"
    assert current["latest_completed_stage_ci_status_in_committed_registry"] == "not_applicable_pre_push"
    assert "latest_completed_stage_commit" not in current
    assert policy["final_commit_and_final_ci_recorded_in_ignored_codex_output_summary"] is True
    assert policy["final_commit_and_final_ci_recorded_in_github_issue_comment"] is True
