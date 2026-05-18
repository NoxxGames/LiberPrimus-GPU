from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _is_ignored(path: str) -> bool:
    return (
        subprocess.run(
            ["git", "check-ignore", "-q", "--", path],
            cwd=REPO,
            check=False,
        ).returncode
        == 0
    )


def test_stage3r_generated_outputs_are_ignored() -> None:
    assert _is_ignored("experiments/results/discord-lead-promotion/stage3r/promotion_audit_records.jsonl")
    assert _is_ignored("experiments/results/discord-lead-promotion/stage3r/rejected_or_quarantined_records.jsonl")
    assert _is_ignored("experiments/results/discord-lead-promotion/stage3r/promotion_summary.json")


def test_raw_discord_logs_and_images_remain_ignored() -> None:
    assert _is_ignored("third_party/LiberPrimusDiscordChats/example.html")
    assert _is_ignored("third_party/LiberPrimusPages/example.jpg")
