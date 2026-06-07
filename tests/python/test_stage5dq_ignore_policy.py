from __future__ import annotations

import subprocess

from test_stage5dq_common import ROOT, git_check_ignore


def test_stage5dq_generated_caches_and_handoffs_are_ignored() -> None:
    assert git_check_ignore(".cache/operator-console/index.json")
    assert git_check_ignore(".cache/operator-console/operator-console.log")
    assert git_check_ignore(".cache/operator-console/thumbnails/example.png")
    assert git_check_ignore("codex-output/stage5dq-codex-completion.md")


def test_stage5dq_deprecated_codex_output_absent_and_cache_untracked() -> None:
    assert not (ROOT / "codex_output").exists()
    result = subprocess.run(
        ["git", "ls-files", "--", ".cache/operator-console"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == ""
