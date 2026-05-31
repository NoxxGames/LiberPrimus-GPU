from pathlib import Path

from test_stage5ci_common import git_check_ignore


def test_stage5ci_generated_and_codex_outputs_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5ci/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5ci/approval_template_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5ci/combined_gate_validation.json")
    assert git_check_ignore("codex-output/stage5ci-codex-completion.md")


def test_stage5ci_deprecated_codex_output_not_used() -> None:
    assert not Path("codex_output").exists()
