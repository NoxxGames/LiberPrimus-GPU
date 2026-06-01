from pathlib import Path

from test_stage5cs_common import ROOT, git_check_ignore


def test_stage5cs_generated_and_codex_outputs_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5cs/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5cs/operator_decision_readiness_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cs/decision_options_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cs/handoff_continuity_report.json")
    assert git_check_ignore("codex-output/stage5cs-codex-completion.md")
    assert git_check_ignore("data/raw/example-stage5cs.txt")


def test_stage5cs_generated_outputs_are_not_tracked() -> None:
    assert not (ROOT / "experiments/results/token-block/stage5cs/summary.json").is_file() or git_check_ignore(
        "experiments/results/token-block/stage5cs/summary.json"
    )
    assert Path("codex-output/stage5cs-codex-completion.md").as_posix().startswith(
        "codex-output/"
    )
