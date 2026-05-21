from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5s_generated_raw_codex_and_sqlite_paths_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/parity_report.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/result_store_integration_report.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/score_summary_integration_report.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/method_status_impact_report.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/generated_body_policy_report.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/boundary_review_report.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/controlled_next_step_decision.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/summary.json",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/warnings.jsonl",
        "experiments/results/gematria-expanded-cuda-result-store/stage5s/results.sqlite3",
        "codex-output/stage5s-codex-completion.md",
        "data/raw/stage5s-example.txt",
    ]
    for path in paths:
        assert _ignored(path), path


def test_stage5s_raw_generated_codex_and_sqlite_not_staged() -> None:
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
