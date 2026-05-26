from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _ignored(path: str) -> bool:
    return subprocess.run(
        ["git", "check-ignore", "-q", path],
        cwd=ROOT,
        check=False,
    ).returncode == 0


def test_stage5av_generated_and_decision_paths_are_ignored() -> None:
    assert _ignored("experiments/results/token-block/stage5av/decision_file_ingest_report.json")
    assert _ignored("experiments/results/token-block/stage5av/token_variant_branch_manifest.json")
    assert _ignored("human-review-packs/stage5au/token-case-review-v2/decision-template.yaml")
    assert _ignored("codex-output/stage5av-codex-completion.md")
