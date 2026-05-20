from __future__ import annotations

import subprocess


def test_stage5f_generated_outputs_and_codex_handoff_are_ignored() -> None:
    paths = [
        "experiments/results/cuda-kernel/stage5f/kernel_implementation_report.json",
        "experiments/results/cuda-kernel/stage5f/kernel_build_report.json",
        "experiments/results/cuda-kernel/stage5f/synthetic_parity_report.json",
        "experiments/results/cuda-kernel/stage5f/summary.json",
        "experiments/results/cuda-kernel/stage5f/warnings.jsonl",
        "codex-output/stage5f-codex-completion.md",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert completed.returncode == 0, path


def test_stage5f_raw_generated_and_codex_output_not_staged() -> None:
    completed = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True)
    staged = completed.stdout.splitlines()
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("experiments/results/") for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
