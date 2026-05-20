from __future__ import annotations

import subprocess


def test_stage5d_generated_outputs_and_codex_handoff_are_ignored() -> None:
    paths = [
        "experiments/results/native-cpu/stage5d/native_backend_capabilities.json",
        "experiments/results/native-cpu/stage5d/threading_parity_report.json",
        "experiments/results/native-cpu/stage5d/native_python_parity_report.json",
        "experiments/results/native-cpu/stage5d/summary.json",
        "codex-output/stage5d-codex-completion.md",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert completed.returncode == 0, path


def test_stage5d_raw_data_not_staged() -> None:
    completed = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True)
    staged = completed.stdout.splitlines()
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
