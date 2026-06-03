from __future__ import annotations

from test_stage5da_common import ensure_stage5da_built, git_check_ignore, load_yaml


def test_stage5da_generated_outputs_and_codex_completion_are_ignored() -> None:
    ensure_stage5da_built()

    assert git_check_ignore("experiments/results/token-block/stage5da/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5da/choice_pause_scaffold_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5da/preservation_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5da/warnings.jsonl")
    assert git_check_ignore("codex-output/stage5da-codex-completion.md")


def test_stage5da_handoff_uses_codex_output_and_preserves_worker_cap() -> None:
    ensure_stage5da_built()
    handoff = load_yaml("data/source-harvester/stage5da-codex-handoff-policy.yaml")
    validation = load_yaml("data/project-state/stage5da-reviewable-validation-evidence.yaml")
    summary = load_yaml("data/project-state/stage5da-summary.yaml")

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["deprecated_handoff_root"] == "codex_output"
    assert handoff["codex_output_used"] is False
    assert handoff["codex_output_exists_locally"] is False
    assert handoff["stage5da_codex_completion_summary_written_locally_before_final_response"] is True
    assert validation["parallel_worker_cap"] == 8
    assert validation["parallel_worker_cap_for_stage5da_and_later"] == 8
    assert validation["old_16_worker_default_reintroduced"] is False
    assert summary["recommended_next_stage_id"] == "stage-5db"
