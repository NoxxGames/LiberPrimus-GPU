from __future__ import annotations

import subprocess


def test_stage4k_generated_cache_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/source-lock-snapshots/stage4k/fetch_report.json",
        "third_party/SourceSnapshots/example.html",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
