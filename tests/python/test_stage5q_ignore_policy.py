from __future__ import annotations

from pathlib import Path
import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5q_generated_raw_and_codex_paths_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/candidate_inventory_report.json",
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/token_mapping_report.json",
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/native_parity_report.json",
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/result_store_preflight_report.json",
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/controlled_expansion_gate_report.json",
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/summary.json",
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/warnings.jsonl",
        "experiments/results/gematria-expansion-candidate-mapping/stage5q/results.sqlite3",
        "codex-output/stage5q-codex-completion.md",
        "data/raw/stage5q-example.txt",
    ]
    for path in paths:
        assert _ignored(path), path


def test_stage5q_raw_generated_codex_and_sqlite_not_staged() -> None:
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


def test_stage5q_docs_make_no_speedup_or_unsolved_claims() -> None:
    docs = [
        Path("docs/architecture/gematria-expansion-candidate-mapping.md"),
        Path("docs/architecture/gematria-expansion-native-parity-fixtures.md"),
        Path("docs/experiments/stage-5q-expansion-candidate-mapping.md"),
        Path("docs/research/stage-5q-expansion-candidate-mapping.md"),
    ]
    forbidden = ("speedup achieved", "solve claimed", "unsolved page cuda enabled")
    for doc in docs:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text, f"{doc}: {phrase}"
