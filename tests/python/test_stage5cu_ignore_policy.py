from pathlib import Path

from test_stage5cu_common import ROOT, git_check_ignore


def test_stage5cu_generated_and_codex_outputs_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5cu/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5cu/decision_options_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cu/negative_fixture_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cu/handoff_continuity_report.json")
    assert git_check_ignore("codex-output/stage5cu-codex-completion.md")
    assert git_check_ignore("data/raw/example-stage5cu.txt")


def test_stage5cu_generated_outputs_are_not_tracked() -> None:
    assert not (ROOT / "experiments/results/token-block/stage5cu/summary.json").is_file() or git_check_ignore(
        "experiments/results/token-block/stage5cu/summary.json"
    )
    assert Path("codex-output/stage5cu-codex-completion.md").as_posix().startswith(
        "codex-output/"
    )
    assert not (ROOT / "codex_output").exists()
