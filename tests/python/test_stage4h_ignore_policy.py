from __future__ import annotations

import subprocess


def test_stage4h_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/cpu-batch/stage4h/summary.json",
        "experiments/results/cpu-batch/stage4h/result_records.jsonl",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
