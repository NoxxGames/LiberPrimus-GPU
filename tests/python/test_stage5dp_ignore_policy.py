from __future__ import annotations

import subprocess

from test_stage5dp_common import ROOT, ensure_stage5dp_built, git_check_ignore


def test_stage5dp_raw_and_generated_paths_are_ignored() -> None:
    ensure_stage5dp_built()

    assert git_check_ignore("third_party/RedditStuff/MayFlyInvestigation/The Mayfly.docx")
    assert git_check_ignore("third_party/RedditStuff/MayFlyInvestigation/57.jpg Mayfly data.xlsx")
    assert git_check_ignore("third_party/RedditStuff/Page_33_ThreeDotsObservations/page_33.webp")
    assert git_check_ignore("experiments/results/token-block/stage5dp/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dp/candidate_report.json")
    assert git_check_ignore("codex-output/stage5dp-codex-completion.md")


def test_stage5dp_no_raw_third_party_files_tracked() -> None:
    ensure_stage5dp_built()

    result = subprocess.run(
        ["git", "ls-files", "--", "third_party/RedditStuff"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == ""
