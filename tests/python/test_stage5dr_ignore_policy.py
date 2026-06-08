from __future__ import annotations

from test_stage5dr_common import git_check_ignore


def test_stage5dr_handoff_and_generated_outputs_ignored() -> None:
    assert git_check_ignore("codex-output/stage5dr-codex-completion.md")
    assert git_check_ignore("experiments/results/source-browser/stage5dr/example.json")
    assert git_check_ignore("experiments/results/token-block/stage5dr/example.json")
