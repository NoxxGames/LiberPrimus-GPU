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
    allowed_stage5f_changes = {
        "cuda/CMakeLists.txt",
        "cuda/include/libreprimus/shift_score_kernel.cuh",
        "cuda/kernels/shift_score_kernel.cu",
        "cuda/tests/CMakeLists.txt",
        "cuda/tests/shift_score_kernel_test.cpp",
    }
    assert changed <= allowed_stage5f_changes
