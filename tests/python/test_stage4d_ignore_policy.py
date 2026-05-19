from __future__ import annotations

import subprocess


def test_stage4d_generated_outputs_are_ignored() -> None:
    for path in (
        "experiments/results/bounded-numeric/stage4d/summary.json",
        "experiments/results/bounded-numeric/stage4d/result_records.jsonl",
    ):
        result = subprocess.run(["git", "check-ignore", path], check=False, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr


def test_stage4d_raw_discord_and_lp_images_are_ignored() -> None:
    for path in (
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ):
        result = subprocess.run(["git", "check-ignore", path], check=False, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
