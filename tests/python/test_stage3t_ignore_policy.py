from __future__ import annotations

import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_stage3t_generated_outputs_ignored() -> None:
    for path in [
        "experiments/results/post-discord/stage3t/gp_rune_claim_verification_records.jsonl",
        "experiments/results/post-discord/stage3t/summary.json",
    ]:
        assert _ignored(path), path


def test_stage3t_raw_inputs_ignored() -> None:
    assert _ignored("third_party/LiberPrimusDiscordChats/example.html")
    assert _ignored("third_party/LiberPrimusPages/example.jpg")


def _ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=REPO,
        check=False,
    )
    return result.returncode == 0
