from __future__ import annotations

from pathlib import Path

from libreprimus.doc_staleness.stage_ledger import stage_ledger_findings_for_text


def test_stage5ah_readme_ledger_does_not_stop_at_stage5n() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert stage_ledger_findings_for_text(text, expected_latest_stage="Stage 5AH") == []
    assert "Stage 5AH" in text
    assert "Stage 5AI" in text
