from __future__ import annotations

import subprocess
from pathlib import Path


def test_stage5b_generated_raw_and_codex_output_paths_ignored() -> None:
    paths = [
        "experiments/results/cuda-parity/stage5b/harness_plan_report.json",
        "experiments/results/cuda-parity/stage5b/parity_fixtures_report.json",
        "experiments/results/cuda-parity/stage5b/backend_capability_report.json",
        "experiments/results/cuda-parity/stage5b/future_kernel_parity_matrix_report.json",
        "experiments/results/cuda-parity/stage5b/summary.json",
        "experiments/results/cuda-parity/stage5b/warnings.jsonl",
        "codex-output/stage5b-codex-completion.md",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path


def test_stage5b_no_transform_cuda_kernels_added() -> None:
    forbidden_name_parts = ("shift", "affine", "vigenere", "prime", "ngram", "topk", "dispatch")
    cuda_files = [
        path
        for path in Path("cuda").rglob("*")
        if path.suffix.lower() in {".cu", ".cuh"} and ".git" not in path.parts
    ]
    assert cuda_files
    explicitly_scoped_stage5_cuda_files = {
        "cuda_smoke",
        "shift_score_kernel",
        "gematria_shift_score_kernel",
    }
    unexpected = [
        path
        for path in cuda_files
        if path.stem not in explicitly_scoped_stage5_cuda_files
        and any(part in path.stem.lower() for part in forbidden_name_parts)
    ]
    assert unexpected == []
