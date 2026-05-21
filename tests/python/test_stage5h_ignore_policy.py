from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_stage5h_generated_and_codex_outputs_are_ignored() -> None:
    paths = [
        "experiments/results/gematria-shift-contract/stage5h/contract_report.json",
        "experiments/results/gematria-shift-contract/stage5h/native_fixture_report.json",
        "experiments/results/gematria-shift-contract/stage5h/solved_fixture_mapping_report.json",
        "experiments/results/gematria-shift-contract/stage5h/summary.json",
        "codex-output/stage5h-codex-completion.md",
        "data/raw/stage5h-example.txt",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path


def test_stage5h_docs_make_no_performance_or_speedup_claims() -> None:
    docs = [
        Path("docs/architecture/gematria-mod29-shift-score-contract.md"),
        Path("docs/architecture/gematria-native-parity-fixtures.md"),
        Path("docs/experiments/stage-5h-gematria-shift-contract.md"),
        Path("docs/research/stage-5h-gematria-shift-contract.md"),
        Path("docs/reference/gematria-shift-contract-cli.md"),
    ]
    for path in docs:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        assert "speedup claim" not in text
        assert "performance claim" not in text


def test_cuda_source_changes_remain_stage5m_host_runner_scope() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "cuda/**/*.cu", "cuda/**/*.cuh"],
        check=True,
        capture_output=True,
        text=True,
    )
    changed = set(result.stdout.splitlines())
    assert changed <= {
        "cuda/include/libreprimus/gematria_shift_score_kernel.cuh",
        "cuda/kernels/gematria_shift_score_kernel.cu",
    }


def test_stage5h_device_code_subset_audit_still_passes() -> None:
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
