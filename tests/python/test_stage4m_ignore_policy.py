from __future__ import annotations

import subprocess


def test_stage4m_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/image-preflight/stage4m/summary.json",
        "experiments/results/image-preflight/stage4m/compression_metrics.jsonl",
        "experiments/results/image-preflight/stage4m/image_metadata.jsonl",
        "third_party/LiberPrimusPages/example.jpg",
        "data/raw/images/Fib421.jpg",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
