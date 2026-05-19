from __future__ import annotations

import subprocess


def test_stage4f_generated_and_raw_cache_paths_ignored() -> None:
    paths = [
        "experiments/results/stego-fixtures/stage4f/fixture_candidate_report.json",
        "third_party/CicadaSolversIddqd/example.mp3",
        "third_party/CicadaArchive/example.jpg",
        "third_party/CicadaOutGuess/example.jpg",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
