from __future__ import annotations

import subprocess


def test_stage5a_generated_outputs_and_codex_output_ignored() -> None:
    paths = [
        "experiments/results/cuda-planning/stage5a/target_plan_report.json",
        "experiments/results/cuda-planning/stage5a/parity_scaffold_report.json",
        "experiments/results/cuda-planning/stage5a/implementation_gates_report.json",
        "experiments/results/cuda-planning/stage5a/non_targets_report.json",
        "experiments/results/cuda-planning/stage5a/summary.json",
        "experiments/results/cuda-planning/stage5a/warnings.jsonl",
        "codex-output/stage5a-codex-completion.md",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
