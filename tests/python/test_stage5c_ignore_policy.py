from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    completed = subprocess.run(["git", "check-ignore", "-q", path], check=False)
    return completed.returncode == 0


def test_stage5c_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert _ignored("experiments/results/cuda-build/stage5c/summary.json")
    assert _ignored("experiments/results/cuda-build/stage5c/toolchain_detection_report.json")
    assert _ignored("experiments/results/cuda-build/stage5c/smoke_build_report.json")
    assert _ignored("experiments/results/cuda-build/stage5c/cmake-smoke-build/CMakeCache.txt")
    assert _ignored("codex-output/stage5c-codex-completion.md")
