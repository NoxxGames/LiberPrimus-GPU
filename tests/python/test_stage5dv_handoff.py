from __future__ import annotations

import subprocess

from test_stage5dv_common import ROOT, ensure_stage5dv_built, load_yaml


def test_stage5dv_handoff_uses_codex_output_and_not_deprecated_root() -> None:
    ensure_stage5dv_built()
    handoff = load_yaml("data/source-harvester/stage5dv-codex-handoff-policy.yaml")
    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["completion_summary_committed"] is False
    assert handoff["deprecated_codex_output_root_used"] is False
    assert not (ROOT / "codex_output").exists()


def test_stage5dv_generated_and_codex_output_paths_are_ignored() -> None:
    ensure_stage5dv_built()
    paths = [
        "codex-output/stage5dv-codex-completion.md",
        "experiments/results/source-lock-triage/example.json",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
        assert result.returncode == 0
