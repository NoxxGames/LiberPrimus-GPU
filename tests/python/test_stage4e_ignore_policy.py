from __future__ import annotations

import subprocess


def test_stage4e_cache_and_outputs_ignored() -> None:
    paths = [
        "third_party/CicadaSolversIddqd/example.jpg",
        "experiments/results/source-delta/stage4e/source_delta_report.json",
        "third_party/LiberPrimusPages/example.jpg",
        "third_party/LiberPrimusDiscordChats/example.html",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
