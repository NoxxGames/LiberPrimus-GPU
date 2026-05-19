from __future__ import annotations

import subprocess


def test_stage4c_generated_outputs_are_ignored() -> None:
    for path in (
        "experiments/results/visual-annotation/stage4c/site/index.html",
        "experiments/results/visual-annotation/stage4c/site/templates/example.annotation.yaml",
    ):
        result = subprocess.run(["git", "check-ignore", path], check=False, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr


def test_stage4c_raw_page_and_discord_inputs_are_ignored() -> None:
    for path in (
        "third_party/LiberPrimusPages/example.jpg",
        "third_party/LiberPrimusDiscordChats/example.html",
    ):
        result = subprocess.run(["git", "check-ignore", path], check=False, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
