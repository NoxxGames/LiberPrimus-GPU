from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5af_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/source-harvester/stage5af/harvest_plan.json")
    assert _ignored("experiments/results/source-harvester/stage5af/summary.json")
    assert _ignored("experiments/results/source-harvester/stage5af/research_bundles_preview/a.txt")


def test_stage5af_raw_roots_and_codex_output_are_ignored() -> None:
    assert _ignored("source-harvester-output/example.txt")
    assert _ignored("harvest-output/example.txt")
    assert _ignored("research-inputs/example.txt")
    assert _ignored("data/raw/stage5af-example.txt")
    assert _ignored("codex-output/stage5af-codex-completion.md")
