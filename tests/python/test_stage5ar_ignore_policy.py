from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5ar_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/token-block/stage5ar/token_pixel_coordinate_records.jsonl")
    assert _ignored("experiments/results/token-block/stage5ar/token_coordinate_validation.json")
    assert _ignored("experiments/results/token-block/stage5ar/review-overlays/example.png")
    assert _ignored("codex-output/stage5ar-codex-completion.md")


def test_stage5ar_raw_page_images_remain_ignored() -> None:
    assert _ignored("third_party/LiberPrimusPages/49.jpg")
