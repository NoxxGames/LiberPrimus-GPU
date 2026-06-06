from __future__ import annotations

from pathlib import Path

from test_stage5dm_common import ROOT, ensure_stage5dm_built, git_check_ignore


def test_stage5dm_generated_outputs_and_handoff_are_ignored() -> None:
    ensure_stage5dm_built()

    assert git_check_ignore("experiments/results/token-block/stage5dm/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dm/source_lock_addendum_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5dm/pivot_readiness_report.json")
    assert git_check_ignore("codex-output/stage5dm-codex-completion.md")


def test_stage5dm_raw_third_party_sources_remain_ignored() -> None:
    ensure_stage5dm_built()

    assert git_check_ignore("third_party/koan_page.png")
    assert git_check_ignore("third_party/LiberPrimusPages/32.jpg")
    assert git_check_ignore(
        "third_party/The-Complete-Cicada3301-Archive-main/2014/Liber Primus/"
        "LP Sacred Book Edition/english text on top of pages/Page6-book.jpg"
    )


def test_stage5dm_deprecated_codex_output_absent() -> None:
    ensure_stage5dm_built()

    assert not (ROOT / "codex_output").exists()
    assert Path("codex-output").as_posix() == "codex-output"
