from __future__ import annotations

import subprocess


def test_stage5x_generated_outputs_and_codex_output_are_ignored() -> None:
    for path in (
        "experiments/results/prime-minus-one-native-parity/stage5x/summary.json",
        "experiments/results/prime-minus-one-native-parity/stage5x/native_run_report.json",
        "experiments/results/prime-minus-one-native-parity/stage5x/native_parity_report.json",
        "codex-output/stage5x-codex-completion.md",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0


def test_stage5x_raw_data_and_sqlite_remain_ignored() -> None:
    for path in (
        "data/raw/stage5x-example.txt",
        "experiments/results/prime-minus-one-native-parity/stage5x/results.sqlite3",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0
