from __future__ import annotations

from pathlib import Path

from libreprimus.doc_staleness.stage_ledger import scan_stage_ledgers, stage_ledger_findings_for_text


def test_stage5ah_stage_ledger_flags_truncated_current_ledger() -> None:
    text = """# README

## Already implemented since Stage 0A

- Stage 5J complete
- Stage 5K complete
- Stage 5L complete
- Stage 5M complete
- Stage 5N complete
"""

    findings = stage_ledger_findings_for_text(text, expected_latest_stage="Stage 5AH")

    assert len(findings) == 1
    assert findings[0].max_stage == "Stage 5N"


def test_stage5ah_stage_ledger_allows_historical_snapshot() -> None:
    text = """# README

## Historical snapshot: early current status

- Stage 5J complete
- Stage 5K complete
- Stage 5L complete
- Stage 5M complete
- Stage 5N complete
"""

    assert stage_ledger_findings_for_text(text, expected_latest_stage="Stage 5AH") == []


def test_stage5ah_current_operational_stage_ledgers_are_clean() -> None:
    report = scan_stage_ledgers(
        paths=("README.md", "STATUS.md", "ROADMAP.md", "AGENTS.md", "docs/roadmap/staged-plan.md"),
        root=Path("."),
        expected_latest_stage="Stage 5AH",
    )

    assert report["finding_count"] == 0
    assert report["warning_count"] == 0
