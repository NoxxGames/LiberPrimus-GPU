from __future__ import annotations

import subprocess
from pathlib import Path


def _ignored(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
    return result.returncode == 0


def test_stage5aa_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/prime-minus-one-cuda-synthetic/stage5aa/summary.json")
    assert _ignored("experiments/results/prime-minus-one-cuda-synthetic/stage5aa/cuda_run_report.json")
    assert _ignored("experiments/results/prime-minus-one-cuda-synthetic/stage5aa/parity_report.json")


def test_stage5aa_raw_and_codex_output_are_ignored() -> None:
    assert _ignored("data/raw/example-stage5aa.txt")
    assert _ignored("codex-output/stage5aa-codex-completion.md")
    assert not Path("codex-output/stage5aa-codex-completion.md").is_file() or _ignored(
        "codex-output/stage5aa-codex-completion.md"
    )
