from __future__ import annotations

from pathlib import Path
import subprocess


def test_stage5k_generated_codex_and_raw_paths_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-cuda-parity-reporting/stage5k/parity_report.json",
        "experiments/results/gematria-cuda-parity-reporting/stage5k/device_code_audit.json",
        "experiments/results/gematria-cuda-parity-reporting/stage5k/solved_fixture_safe_preflight.json",
        "experiments/results/gematria-cuda-parity-reporting/stage5k/score_summary_preflight.json",
        "experiments/results/gematria-cuda-parity-reporting/stage5k/summary.json",
        "experiments/results/gematria-cuda-parity-reporting/stage5k/warnings.jsonl",
        "codex-output/stage5k-codex-completion.md",
        "data/raw/example.bin",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert completed.returncode == 0, path


def test_stage5k_raw_generated_codex_and_sqlite_not_staged() -> None:
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
    assert not generated


def test_stage5k_docs_do_not_make_performance_claims() -> None:
    docs = [
        "CUDA_NOTES.md",
        "BENCHMARKS.md",
        "docs/architecture/gematria-cuda-parity-reporting.md",
        "docs/experiments/stage-5k-gematria-cuda-parity-reporting.md",
    ]
    for doc in docs:
        path = Path(doc)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        assert "speedup achieved" not in text
        assert "performance improvement" not in text


def test_stage5k_no_new_kernel_or_python_worker_policy() -> None:
    summary = Path("data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml").read_text(encoding="utf-8")
    assert "new_cuda_kernels_added: 0" in summary
    assert "cxx_launches_python_workers: false" in summary
