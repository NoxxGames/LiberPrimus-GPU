from __future__ import annotations

import subprocess


def test_stage5a_does_not_modify_cuda_sources() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "*.cu", "*.cuh", "cuda"],
        check=True,
        capture_output=True,
        text=True,
    )
    changed = set(result.stdout.splitlines())
    allowed_stage5f_stage5m_changes = {
        "cuda/CMakeLists.txt",
        "cuda/include/libreprimus/gematria_shift_score_kernel.cuh",
        "cuda/include/libreprimus/shift_score_kernel.cuh",
        "cuda/kernels/cuda_smoke.cu",
        "cuda/kernels/gematria_shift_score_kernel.cu",
        "cuda/kernels/shift_score_kernel.cu",
        "cuda/tests/CMakeLists.txt",
        "cuda/tests/gematria_shift_score_stage5m_runner.cpp",
        "cuda/tests/shift_score_kernel_test.cpp",
    }
    assert changed <= allowed_stage5f_stage5m_changes
