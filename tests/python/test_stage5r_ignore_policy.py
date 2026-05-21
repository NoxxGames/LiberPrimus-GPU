from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5r_generated_raw_and_codex_paths_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/cuda_run_report.json",
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/parity_report.json",
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/boundary_report.json",
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/result_store_preflight.json",
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/score_summary_preflight.json",
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/summary.json",
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/warnings.jsonl",
        "experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/results.sqlite3",
        "codex-output/stage5r-codex-completion.md",
        "data/raw/stage5r-example.txt",
    ]
    for path in paths:
        assert _ignored(path), path


def test_stage5r_raw_generated_codex_and_sqlite_not_staged() -> None:
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
