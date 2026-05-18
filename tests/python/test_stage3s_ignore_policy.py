from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=REPO,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def test_stage3s_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/post-discord/stage3s/candidate_records.jsonl")
    assert _ignored("experiments/results/post-discord/stage3s/top_candidates.jsonl")
    assert _ignored("experiments/results/post-discord/stage3s/summary.json")


def test_stage3s_raw_dirs_remain_ignored() -> None:
    assert _ignored("third_party/LiberPrimusDiscordChats/example.html")
    assert _ignored("third_party/LiberPrimusPages/example.jpg")
