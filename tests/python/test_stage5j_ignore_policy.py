from __future__ import annotations

import subprocess


def test_stage5j_generated_codex_and_raw_paths_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-cuda-kernel/stage5j/kernel_implementation_report.json",
        "experiments/results/gematria-cuda-kernel/stage5j/kernel_build_report.json",
        "experiments/results/gematria-cuda-kernel/stage5j/synthetic_parity_report.json",
        "experiments/results/gematria-cuda-kernel/stage5j/summary.json",
        "experiments/results/gematria-cuda-kernel/stage5j/warnings.jsonl",
        "codex-output/stage5j-codex-completion.md",
        "data/raw/example.bin",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert completed.returncode == 0, path


def test_stage5j_raw_generated_codex_and_sqlite_not_staged() -> None:
    completed = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True)
    staged = completed.stdout.splitlines()
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("experiments/results/") and not path.endswith((".gitkeep", "README.md")) for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
    assert not any(path.endswith((".sqlite", ".sqlite3", ".db")) for path in staged)
