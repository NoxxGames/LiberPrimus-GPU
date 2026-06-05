from __future__ import annotations

from pathlib import Path

from test_stage5di_common import ensure_stage5di_built, git_check_ignore


def test_stage5di_generated_outputs_raw_roots_and_handoff_are_ignored() -> None:
    ensure_stage5di_built()

    assert git_check_ignore("experiments/results/token-block/stage5di/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5di/source_lock_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5di/pivot_readiness_report.json")
    assert git_check_ignore("codex-output/stage5di-codex-completion.md")
    assert git_check_ignore("data/raw/example.txt")
    assert git_check_ignore("data/normalized/alignment/example.txt")
    assert git_check_ignore("third_party/CiadaSolversIddqd_v2/example.jpg")
    assert git_check_ignore("third_party/UsefulFilesAndIdeas/number-triangle-theory/example.png")


def test_stage5di_codex_output_underscore_root_absent() -> None:
    ensure_stage5di_built()

    assert not Path("codex_output").exists()
