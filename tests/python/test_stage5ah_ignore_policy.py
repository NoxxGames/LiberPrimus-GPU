from __future__ import annotations

import subprocess


def _is_ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5ah_generated_doc_staleness_reports_are_ignored() -> None:
    assert _is_ignored("experiments/results/doc-staleness/stage5ah/stale_stage_ledger_report.json")
    assert _is_ignored("experiments/results/doc-staleness/stage5ah/doc_staleness_summary.json")


def test_stage5ah_codex_output_is_ignored() -> None:
    assert _is_ignored("codex-output/stage5ah-codex-completion.md")
