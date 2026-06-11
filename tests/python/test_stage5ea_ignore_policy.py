from __future__ import annotations

import subprocess

from test_stage5ea_common import ROOT, ensure_stage5ea_built


def test_stage5ea_generated_outputs_are_ignored() -> None:
    ensure_stage5ea_built()

    for path in (
        "codex-output/stage5ea-codex-completion.md",
        "experiments/results/ci/parallel-validation/stage5ea/example.json",
    ):
        result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
        assert result.returncode == 0
