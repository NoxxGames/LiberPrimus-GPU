from __future__ import annotations

import subprocess
from pathlib import Path


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5ab_generated_staleness_reports_are_ignored() -> None:
    assert _ignored("experiments/results/doc-staleness/stage5ab/staleness_findings.json")
    assert _ignored("experiments/results/doc-staleness/stage5ab/summary.json")
    assert _ignored("experiments/results/doc-staleness/stage5ab/warnings.jsonl")


def test_stage5ab_raw_and_codex_outputs_are_ignored() -> None:
    assert _ignored("data/raw/stage5ab-example.txt")
    assert _ignored("data/normalized/alignment/stage5ab-example.txt")
    assert _ignored("codex-output/stage5ab-doc-staleness-codex-completion.md")
    assert not Path("codex-output/stage5ab-doc-staleness-codex-completion.md").is_file() or _ignored(
        "codex-output/stage5ab-doc-staleness-codex-completion.md"
    )
