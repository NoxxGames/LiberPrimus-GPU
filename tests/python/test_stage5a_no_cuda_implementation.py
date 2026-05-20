from __future__ import annotations

import subprocess


def test_stage5a_does_not_modify_cuda_sources() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "*.cu", "*.cuh", "cuda"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == ""
