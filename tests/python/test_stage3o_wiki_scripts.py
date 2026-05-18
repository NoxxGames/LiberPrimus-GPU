from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def _run_script(*args: str) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        return subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", *args],
            cwd=REPO,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    return subprocess.run(
        ["bash", *args],
        cwd=REPO,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_stage3o_validate_wiki_source_script_passes() -> None:
    script = "scripts/github/validate-wiki-source.ps1" if os.name == "nt" else "scripts/github/validate-wiki-source.sh"
    result = _run_script(script)
    assert result.returncode == 0, result.stderr
    assert "wiki_source_valid=true" in result.stdout


def test_stage3o_sync_tutorials_dry_run_passes() -> None:
    if os.name == "nt":
        result = _run_script("scripts/github/sync-tutorials-to-wiki.ps1", "--DryRun")
    else:
        result = _run_script("scripts/github/sync-tutorials-to-wiki.sh", "--dry-run")
    assert result.returncode == 0, result.stderr
    assert "dry_run=true" in result.stdout


def test_stage3o_raw_and_generated_paths_are_ignored() -> None:
    for path in [
        "third_party/LiberPrimusDiscordChats/example.html",
        "experiments/results/discord-promotion/stage3o/promotion_candidates.jsonl",
        "experiments/results/wiki-sync/stage3o/wiki-sync-report.json",
    ]:
        result = subprocess.run(
            ["git", "check-ignore", "-q", "--", path],
            cwd=REPO,
            check=False,
        )
        assert result.returncode == 0, path
