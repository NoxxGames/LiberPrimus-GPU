from __future__ import annotations

import subprocess

from libreprimus.paths import repo_root


def test_stage5am_generated_exports_and_handoffs_are_ignored() -> None:
    paths = [
        "website-export/stage5am/research-index/index.html",
        "website-export/stage5am/research-index/data/source-cards.json",
        "website-export/stage5am/research-index.zip",
        "experiments/results/website-render/stage5am/summary.json",
        "codex-output/stage5am-codex-completion.md",
        "research-inputs/stage5al/deep_research_master_context.md",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], cwd=repo_root(), check=False)
        assert completed.returncode == 0, path


def test_stage5am_raw_third_party_and_private_roots_remain_ignored() -> None:
    paths = [
        "third_party/UsefulFilesAndIdeas/LP Excel.xlsx",
        "third_party/UsefulFilesAndIdeas/community-facts/community-facts-collection.txt",
        "data/raw/transcripts/example.txt",
        "deep-research-reports/stage5am.md",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], cwd=repo_root(), check=False)
        assert completed.returncode == 0, path
