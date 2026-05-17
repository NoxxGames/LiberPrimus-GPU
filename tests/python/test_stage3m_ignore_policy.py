from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _is_ignored(path: str) -> bool:
    return (
        subprocess.run(
            ["git", "check-ignore", "-q", "--", path],
            cwd=REPO,
            check=False,
        ).returncode
        == 0
    )


def test_image_analysis_generated_outputs_are_ignored() -> None:
    assert _is_ignored("experiments/results/image-analysis/stage3m/image_analysis_records.jsonl")
    assert _is_ignored("experiments/results/image-analysis/stage3m/visual_feature_candidates.jsonl")
    assert _is_ignored("experiments/results/image-analysis/stage3m/summary.json")


def test_liber_primus_raw_images_remain_ignored() -> None:
    assert _is_ignored("third_party/LiberPrimusPages/example.jpg")
    assert _is_ignored("third_party/LiberPrimusPages/example.jpeg")
    assert _is_ignored("third_party/LiberPrimusPages/example.png")
