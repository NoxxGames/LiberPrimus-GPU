from __future__ import annotations

from pathlib import Path
import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5p_generated_raw_and_codex_paths_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-cuda-result-store/stage5p/result_store_integration_report.json",
        "experiments/results/gematria-cuda-result-store/stage5p/score_summary_integration_report.json",
        "experiments/results/gematria-cuda-result-store/stage5p/method_status_impact_report.json",
        "experiments/results/gematria-cuda-result-store/stage5p/generated_body_policy_report.json",
        "experiments/results/gematria-cuda-result-store/stage5p/controlled_expansion_candidate_report.json",
        "experiments/results/gematria-cuda-result-store/stage5p/summary.json",
        "experiments/results/gematria-cuda-result-store/stage5p/warnings.jsonl",
        "experiments/results/gematria-cuda-result-store/stage5p/results.sqlite3",
        "codex-output/stage5p-codex-completion.md",
        "data/raw/stage5p-example.txt",
    ]
    for path in paths:
        assert _ignored(path), path


def test_stage5p_raw_generated_codex_and_sqlite_not_staged() -> None:
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


def test_stage5p_docs_make_no_speedup_or_solve_claims() -> None:
    docs = [
        Path("docs/architecture/gematria-cuda-result-store-integration.md"),
        Path("docs/architecture/gematria-cuda-score-summary-integration.md"),
        Path("docs/experiments/stage-5p-cuda-result-store-integration.md"),
        Path("docs/research/stage-5p-cuda-result-store-integration.md"),
    ]
    forbidden = ("speedup achieved", "solve claimed", "unsolved page cuda enabled")
    for doc in docs:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text, f"{doc}: {phrase}"
