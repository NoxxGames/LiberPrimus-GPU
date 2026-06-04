from __future__ import annotations

from test_stage5dg_common import ensure_stage5dg_built, git_check_ignore


def test_stage5dg_generated_outputs_and_raw_roots_are_ignored() -> None:
    ensure_stage5dg_built()

    assert git_check_ignore("experiments/results/token-block/stage5dg/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dg/approval_record_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5dg/boundary_report.json")
    assert git_check_ignore("codex-output/stage5dg-codex-completion.md")
    assert git_check_ignore("data/raw/example.txt")
    assert git_check_ignore("data/normalized/alignment/example.txt")
