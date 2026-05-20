from __future__ import annotations

import subprocess
from pathlib import Path


def test_stage5g_generated_outputs_and_codex_handoff_are_ignored() -> None:
    paths = [
        "experiments/results/cuda-parity-reporting/stage5g/shift_score_parity_report.json",
        "experiments/results/cuda-parity-reporting/stage5g/device_code_subset_audit.json",
        "experiments/results/cuda-parity-reporting/stage5g/solved_fixture_safe_preflight.json",
        "experiments/results/cuda-parity-reporting/stage5g/summary.json",
        "experiments/results/cuda-parity-reporting/stage5g/warnings.jsonl",
        "codex-output/stage5g-codex-completion.md",
        "data/raw/example.bin",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert completed.returncode == 0, path


def test_stage5g_raw_generated_codex_and_sqlite_not_staged() -> None:
    completed = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True)
    staged = completed.stdout.splitlines()
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("experiments/results/") and not path.endswith((".gitkeep", "README.md")) for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
    assert not any(path.endswith((".sqlite", ".sqlite3", ".db")) for path in staged)


def test_stage5g_docs_do_not_make_performance_claims() -> None:
    docs = [
        Path("docs/architecture/shift-score-cuda-parity-reporting.md"),
        Path("docs/architecture/cuda-device-code-subset-policy.md"),
        Path("docs/experiments/stage-5g-shift-score-cuda-parity-reporting.md"),
        Path("docs/research/stage-5g-shift-score-cuda-parity-reporting.md"),
        Path("docs/reference/cuda-parity-reporting-cli.md"),
    ]
    for path in docs:
        if path.is_file():
            text = path.read_text(encoding="utf-8").lower()
            assert "speedup claim" not in text
            assert "performance claim" not in text


def test_stage5g_manifests_do_not_reference_real_lp_data() -> None:
    manifest_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in Path("experiments/manifests/cuda").glob("stage5g-*.yaml"))
    assert "third_party/liberprimuspages" not in manifest_text
    assert "data/raw/transcripts" not in manifest_text
    assert "unsolved_page_cuda_used: true" not in manifest_text


def test_stage5g_cxx_does_not_launch_python_workers() -> None:
    cxx_paths = [*Path("cuda").rglob("*.cu"), *Path("cuda").rglob("*.cuh"), *Path("src").rglob("*.cpp"), *Path("src").rglob("*.hpp")]
    worker_refs = [
        path
        for path in cxx_paths
        if "python" in path.read_text(encoding="utf-8", errors="ignore").lower()
        and "worker" in path.read_text(encoding="utf-8", errors="ignore").lower()
    ]
    assert worker_refs == []
