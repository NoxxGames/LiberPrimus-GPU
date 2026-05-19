from __future__ import annotations

import subprocess


def test_stage4l_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/observation-promotion/stage4l/promotion_ledger_report.json",
        "experiments/results/observation-promotion/stage4l/manifest_readiness_report.json",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
