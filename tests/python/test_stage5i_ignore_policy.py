from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_stage5i_generated_codex_and_raw_outputs_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-cuda-prep/stage5i/kernel_preparation_report.json",
        "experiments/results/gematria-cuda-prep/stage5i/abi_plan_report.json",
        "experiments/results/gematria-cuda-prep/stage5i/validation_vectors_report.json",
        "experiments/results/gematria-cuda-prep/stage5i/summary.json",
        "codex-output/stage5i-codex-completion.md",
        "data/raw/stage5i-example.txt",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path


def test_stage5i_docs_make_no_performance_or_speedup_claims() -> None:
    docs = [
        Path("docs/architecture/gematria-mod29-cuda-preparation.md"),
        Path("docs/architecture/gematria-shift-kernel-abi.md"),
        Path("docs/experiments/stage-5i-gematria-cuda-preparation.md"),
        Path("docs/research/stage-5i-gematria-cuda-preparation.md"),
        Path("docs/reference/gematria-cuda-prep-cli.md"),
    ]
    for path in docs:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        assert "speedup claim" not in text
        assert "performance claim" not in text


def test_stage5i_does_not_change_cuda_sources() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "cuda/**/*.cu", "cuda/**/*.cuh"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == ""


def test_stage5i_device_code_subset_audit_still_passes() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "libreprimus.cli",
            "cuda-parity-reporting",
            "validate-stage5g",
            "--parity-report",
            "data/cuda/stage5g-shift-score-parity-report.yaml",
            "--device-code-audit",
            "data/cuda/stage5g-cuda-device-code-subset-audit.yaml",
            "--preflight",
            "data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml",
            "--summary",
            "data/cuda/stage5g-cuda-parity-reporting-summary.yaml",
            "--results-dir",
            "experiments/results/cuda-parity-reporting/stage5g",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "device_code_subset_compliant=true" in result.stdout
