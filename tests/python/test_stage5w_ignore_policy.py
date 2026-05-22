from __future__ import annotations

import subprocess


def test_stage5w_generated_outputs_and_codex_output_are_ignored() -> None:
    for path in (
        "experiments/results/prime-minus-one-native-contract/stage5w/summary.json",
        "experiments/results/prime-minus-one-native-contract/stage5w/source_inventory_report.json",
        "codex-output/stage5w-codex-completion.md",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0


def test_stage5w_raw_data_remains_ignored() -> None:
    result = subprocess.run(["git", "check-ignore", "-q", "data/raw/stage5w-example.txt"], check=False)
    assert result.returncode == 0
