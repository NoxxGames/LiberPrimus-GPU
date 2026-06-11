from __future__ import annotations

import subprocess

from test_stage5eb_common import ROOT, ensure_stage5eb_built


def test_stage5eb_generated_and_handoff_outputs_are_ignored() -> None:
    ensure_stage5eb_built()

    for path in (
        "codex-output/stage5eb-codex-completion.md",
        "experiments/results/ci/parallel-validation/stage5eb/example.json",
        "experiments/results/ci/parallel-validation/stage5eb/summary.json",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
        assert result.returncode == 0


def test_stage5eb_raw_roots_remain_ignored() -> None:
    ensure_stage5eb_built()

    for path in (
        "data/raw/stage5eb-example.txt",
        "third_party/LiberPrimusDiscordChats/stage5eb-example.txt",
        "third_party/LiberPrimusPages/stage5eb-example.png",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
        assert result.returncode == 0
