from __future__ import annotations

import subprocess


def test_stage5e_generated_outputs_and_codex_handoff_are_ignored() -> None:
    paths = [
        "experiments/results/cuda-kernel-contract/stage5e/first_kernel_contract_report.json",
        "experiments/results/cuda-kernel-contract/stage5e/adapter_selection_report.json",
        "experiments/results/cuda-kernel-contract/stage5e/native_parity_adapter_report.json",
        "experiments/results/cuda-kernel-contract/stage5e/implementation_readiness_report.json",
        "experiments/results/cuda-kernel-contract/stage5e/summary.json",
        "codex-output/stage5e-codex-completion.md",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert completed.returncode == 0, path


def test_stage5e_raw_data_and_codex_output_not_staged() -> None:
    completed = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True)
    staged = completed.stdout.splitlines()
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
