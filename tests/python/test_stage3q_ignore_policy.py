from __future__ import annotations

import subprocess
from pathlib import Path


def test_stage3q_generated_shards_and_raw_discord_logs_are_ignored() -> None:
    repo = Path(__file__).resolve().parents[2]
    for path in [
        "experiments/results/discord-review-bundles/stage3q/topic_shards/source-links-and-datasets.md",
        "experiments/results/discord-review-bundles/stage3q/redacted_message_stream.jsonl",
        "third_party/LiberPrimusDiscordChats/example.html",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=repo, check=False)
        assert result.returncode == 0, path
