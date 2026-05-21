from __future__ import annotations

from pathlib import Path
import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5o_generated_raw_and_codex_paths_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/repeat_run_report.json",
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/repeat_parity_report.json",
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/result_store_preflight.json",
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/score_summary_preflight.json",
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/expansion_decision.json",
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/summary.json",
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/warnings.jsonl",
        "experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/results.sqlite3",
        "codex-output/stage5o-codex-completion.md",
        "data/raw/stage5o-example.txt",
    ]
    for path in paths:
        assert _ignored(path), path


def test_stage5o_raw_generated_codex_and_sqlite_not_staged() -> None:
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


def test_stage5o_docs_make_no_positive_speedup_or_performance_claims() -> None:
    docs = [
        Path("docs/architecture/solved-fixture-cuda-repeat-verification.md"),
        Path("docs/architecture/solved-fixture-cuda-result-store-preflight.md"),
        Path("docs/experiments/stage-5o-repeat-verification-result-store-preflight.md"),
        Path("docs/research/stage-5o-repeat-verification-result-store-preflight.md"),
    ]
    forbidden_positive_claims = (
        "speedup achieved",
        "performance improved",
        "benchmark passed",
        "throughput",
    )
    for doc in docs:
        text = doc.read_text(encoding="utf-8").lower()
        for phrase in forbidden_positive_claims:
            assert phrase not in text, f"{doc}: {phrase}"
