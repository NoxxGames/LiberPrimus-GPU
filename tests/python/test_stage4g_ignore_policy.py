from __future__ import annotations

import subprocess


def test_stage4g_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/cookie-refresh/stage4g/summary.json",
        "experiments/results/cookie-refresh/stage4g/candidate_records.jsonl",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
