from __future__ import annotations

import subprocess


def test_stage4i_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/scoring-consolidation/stage4i/scorer_inventory.json",
        "experiments/results/scoring-consolidation/stage4i/calibration_report_generated.json",
        "experiments/results/scoring-consolidation/stage4i/cpu_batch_score_compatibility.json",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
