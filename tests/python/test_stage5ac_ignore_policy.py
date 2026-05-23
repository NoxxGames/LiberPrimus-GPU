from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
    return result.returncode == 0


def test_stage5ac_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/prime-minus-one-cuda-synthetic-reporting/stage5ac/synthetic_parity_report.json")
    assert _ignored("experiments/results/prime-minus-one-cuda-synthetic-reporting/stage5ac/summary.json")
    assert _ignored("experiments/results/prime-minus-one-cuda-synthetic-reporting/stage5ac/warnings.jsonl")


def test_stage5ac_raw_and_codex_output_are_ignored() -> None:
    assert _ignored("data/raw/stage5ac-example.txt")
    assert _ignored("codex-output/stage5ac-codex-completion.md")
