from __future__ import annotations

import subprocess


def test_stage4j_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/observation-review/stage4j/review_decision_report.json",
        "experiments/results/observation-review/stage4j/path_sanitisation_report.json",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
