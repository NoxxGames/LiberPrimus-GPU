from pathlib import Path

from test_stage5cq_common import ROOT, git_check_ignore


def test_stage5cq_generated_and_codex_outputs_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5cq/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5cq/operator_decision_package_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cq/handoff_restoration_report.json")
    assert git_check_ignore("codex-output/stage5cq-codex-completion.md")
    assert git_check_ignore("data/raw/example-stage5cq.txt")


def test_stage5cq_generated_outputs_are_not_tracked() -> None:
    assert not (ROOT / "experiments/results/token-block/stage5cq/summary.json").is_file() or git_check_ignore(
        "experiments/results/token-block/stage5cq/summary.json"
    )
    assert Path("codex-output/stage5cq-codex-completion.md").as_posix().startswith(
        "codex-output/"
    )
