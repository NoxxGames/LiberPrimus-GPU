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


def test_discord_generated_outputs_are_ignored() -> None:
    assert _is_ignored("experiments/results/discord-ingestion/stage3n/discord_extracted_links.jsonl")
    assert _is_ignored("experiments/results/discord-ingestion/stage3n/local_review_index.html")
    assert _is_ignored("experiments/results/discord-ingestion/stage3n/discord_ingestion_summary.json")


def test_discord_raw_logs_are_ignored() -> None:
    assert _is_ignored("third_party/LiberPrimusDiscordChats/example.html")
    assert _is_ignored("third_party/LiberPrimusDiscordChats/nested/example.htm")
