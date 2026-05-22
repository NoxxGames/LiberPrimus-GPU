from __future__ import annotations

import subprocess


def test_stage5z_no_cuda_source_files_changed() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "*.cu", "*.cuh"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
