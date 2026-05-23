from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5ad_fix_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-mismatch/stage5ad-fix/summary.json")
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-mismatch/stage5ad-fix/hash_lineage_report.json")
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-mismatch/stage5ad-fix/warnings.jsonl")


def test_stage5ad_fix_raw_and_codex_output_are_ignored() -> None:
    assert _ignored("data/raw/stage5ad-fix-example.txt")
    assert _ignored("codex-output/stage5ad-fix-codex-completion.md")
