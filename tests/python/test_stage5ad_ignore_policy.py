from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
    return result.returncode == 0


def test_stage5ad_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/summary.json")
    assert _ignored(
        "experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/cuda_run_report.json"
    )
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/warnings.jsonl")


def test_stage5ad_raw_and_codex_output_are_ignored() -> None:
    assert _ignored("data/raw/stage5ad-example.txt")
    assert _ignored("codex-output/stage5ad-codex-completion.md")
