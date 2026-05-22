from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5t_generated_raw_codex_and_sqlite_paths_are_ignored() -> None:
    paths = [
        "experiments/results/cuda-solved-family-readiness/stage5t/solved_family_inventory_report.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/cuda_parity_matrix_report.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/kernel_readiness_report.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/batch_abi_gap_report.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/benchmark_readiness_report.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/no_unsolved_guardrail_report.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/next_stage_decision.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/summary.json",
        "experiments/results/cuda-solved-family-readiness/stage5t/warnings.jsonl",
        "experiments/results/cuda-solved-family-readiness/stage5t/results.sqlite3",
        "codex-output/stage5t-codex-completion.md",
        "data/raw/stage5t-example.txt",
    ]
    for path in paths:
        assert _ignored(path), path


def test_stage5t_raw_generated_codex_and_sqlite_not_staged() -> None:
    completed = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True)
    staged = completed.stdout.splitlines()
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
    assert not any(path.endswith((".sqlite", ".sqlite3", ".db")) for path in staged)
    generated = [
        path
        for path in staged
        if path.startswith("experiments/results/") and not path.endswith((".gitkeep", "README.md"))
    ]
    assert generated == []
