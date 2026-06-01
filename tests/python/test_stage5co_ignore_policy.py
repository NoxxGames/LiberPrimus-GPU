from pathlib import Path

from test_stage5co_common import ROOT, git_check_ignore


def test_stage5co_generated_and_codex_outputs_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5co/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5co/readiness_package_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5co/transition_plan_report.json")
    assert git_check_ignore("codex-output/stage5co-codex-completion.md")
    assert git_check_ignore("data/raw/example-stage5co.txt")
    assert not (ROOT / "codex_output").exists()


def test_stage5co_generated_outputs_are_not_tracked() -> None:
    assert not (ROOT / "experiments/results/token-block/stage5co/summary.json").is_file() or git_check_ignore(
        "experiments/results/token-block/stage5co/summary.json"
    )
    assert Path("codex-output/stage5co-codex-completion.md").as_posix().startswith(
        "codex-output/"
    )
