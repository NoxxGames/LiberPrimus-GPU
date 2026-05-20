from __future__ import annotations

import subprocess


def test_stage4q_generated_outputs_and_codex_output_ignored() -> None:
    paths = [
        "experiments/results/benchmarks/stage4q/benchmark_environment.json",
        "experiments/results/benchmarks/stage4q/cpu_benchmark_smoke_records.jsonl",
        "experiments/results/benchmarks/stage4q/cuda_parity_readiness.json",
        "experiments/results/benchmarks/stage4q/summary.json",
        "codex-output/stage4q-codex-completion.md",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
