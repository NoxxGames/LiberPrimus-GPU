from __future__ import annotations

import subprocess


def test_stage5z_generated_outputs_and_codex_output_are_ignored() -> None:
    paths = [
        "experiments/results/prime-minus-one-cuda-contract/stage5z/summary.json",
        "experiments/results/prime-minus-one-cuda-contract/stage5z/cuda_contract_report.json",
        "experiments/results/prime-minus-one-cuda-contract/stage5z/validation_vector_report.json",
        "codex-output/stage5z-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
