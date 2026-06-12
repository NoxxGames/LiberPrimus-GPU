from __future__ import annotations

from libreprimus.doc_staleness.stage_ids import parse_stage_id
from libreprimus.doc_staleness.stale_current_claims import audit_repository, scan_text
from test_stage5eg_common import ensure_stage5eg_built


LATEST = parse_stage_id("Stage 5EG")
NEXT = parse_stage_id("Stage 5EH")


def _findings(text: str, path: str = "docs/onboarding/start-here.md"):
    return scan_text(text, path, LATEST, NEXT)


def test_scanner_flags_stale_latest_current_and_next_claims() -> None:
    samples = [
        "Stage 5EC is the latest completed stage.",
        "Current state: Stage 5DQ is complete and Stage 5DR is next.",
        "Latest completed stage: Stage 5CM",
        "Current planning focus: Stage 5EF - Source-lock number-fact review batch 006",
    ]

    for sample in samples:
        findings = _findings(sample)
        assert findings, sample
        assert any(finding.severity == "error" for finding in findings)


def test_scanner_ignores_plain_and_explicit_historical_statements() -> None:
    assert not _findings("Stage 5EC completed the third review batch.")
    assert not _findings("At the time of Stage 5EC, Stage 5EC was the latest completed stage.")
    assert not _findings("## Historical Stage 5EC Boundary")


def test_scanner_requires_suppression_reason() -> None:
    text = "<!-- doc-staleness: allow-historical-current-phrase -->\nStage 5EC is the latest completed stage."
    findings = _findings(text)

    assert any(finding.claim_type == "invalid_suppression" for finding in findings)


def test_scanner_accepts_reasoned_adjacent_suppression() -> None:
    text = (
        "<!-- doc-staleness: allow-historical-current-phrase; reason: quoted old closeout -->\n"
        "Stage 5EC is the latest completed stage."
    )

    assert not _findings(text)


def test_repository_audit_excludes_generated_and_raw_roots() -> None:
    ensure_stage5eg_built()

    report = audit_repository()

    assert report.error_count == 0
    assert all(not finding.path.startswith("experiments/results/") for finding in report.findings)
    assert all(not finding.path.startswith("third_party/") for finding in report.findings)
    assert all(not finding.path.startswith("data/raw/") for finding in report.findings)
