from __future__ import annotations

import subprocess


def test_stage5y_generated_outputs_and_codex_output_are_ignored() -> None:
    for path in (
        "experiments/results/prime-minus-one-native-reporting/stage5y/native_parity_report.json",
        "experiments/results/prime-minus-one-native-reporting/stage5y/cuda_contract_readiness_gate.json",
        "experiments/results/prime-minus-one-native-reporting/stage5y/summary.json",
        "codex-output/stage5y-codex-completion.md",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0


def test_stage5y_raw_data_and_sqlite_remain_ignored() -> None:
    for path in (
        "data/raw/stage5y-example.txt",
        "experiments/results/prime-minus-one-native-reporting/stage5y/results.sqlite3",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0
