from __future__ import annotations

from test_stage5dc_common import ensure_stage5dc_built, git_check_ignore, load_yaml


def test_stage5dc_handoff_uses_codex_output_dash_root() -> None:
    ensure_stage5dc_built()
    handoff = load_yaml("data/source-harvester/stage5dc-codex-handoff-policy.yaml")

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["deprecated_handoff_root"] == "codex_output"
    assert handoff["codex_output_used"] is False
    assert handoff["codex_output_exists_locally"] is False
    assert handoff["stage5dc_completion_summary_finalized_not_pending"] is True
    assert git_check_ignore("codex-output/stage5dc-codex-completion.md")


def test_stage5dc_generated_reports_are_ignored() -> None:
    ensure_stage5dc_built()

    assert git_check_ignore("experiments/results/token-block/stage5dc/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dc/choice_decision_report.json")
