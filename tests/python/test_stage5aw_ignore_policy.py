from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_generated_and_raw_paths_remain_ignored() -> None:
    paths = [
        "experiments/results/token-block/stage5aw/summary.json",
        "experiments/results/token-block/stage5aw/repaired_token_variant_branch_manifest.json",
        "human-review-packs/stage5au/token-case-review-v2/decision-template.yaml",
        "codex-output/stage5aw-codex-completion.md",
        "third_party/LiberPrimusPages/example.jpg",
    ]
    for path in paths:
        result = subprocess.run(
            ["git", "check-ignore", "-q", path],
            cwd=ROOT,
            check=False,
        )
        assert result.returncode == 0, path
