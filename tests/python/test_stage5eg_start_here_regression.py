from __future__ import annotations

from pathlib import Path

from libreprimus.doc_staleness.stale_current_claims import audit_repository
from test_stage5eg_common import ensure_stage5eg_built


def test_start_here_known_stale_current_patterns_are_repaired() -> None:
    ensure_stage5eg_built()

    text = Path("docs/onboarding/start-here.md").read_text(encoding="utf-8")

    assert "## Stage 5EC Current Boundary" not in text
    assert "## Historical Stage 5EC Boundary" in text
    assert "Stage 5EC is the latest completed stage." not in text
    assert "Current state: Stage 5DQ is complete" not in text
    assert "Stage 5CM is the latest completed stage." not in text


def test_start_here_has_no_unsuppressed_stale_current_errors() -> None:
    ensure_stage5eg_built()

    report = audit_repository()
    findings = [finding for finding in report.findings if finding.path == "docs/onboarding/start-here.md"]

    assert not [finding for finding in findings if finding.severity == "error"]
