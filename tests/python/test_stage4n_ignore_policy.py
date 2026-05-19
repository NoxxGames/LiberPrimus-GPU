from __future__ import annotations

import subprocess


def test_stage4n_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/stego-positive-controls/stage4n/readiness_report.json",
        "experiments/results/stego-positive-controls/stage4n/cache_report.json",
        "third_party/StegoPositiveControls/example.mp3",
        "third_party/StegoPositiveControls/example.jpg",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
