from __future__ import annotations

from pathlib import Path

from libreprimus.doc_staleness.stage_ids import parse_stage_id
from libreprimus.doc_staleness.stale_current_claims import audit_repository, scan_text
from libreprimus.stage_state.current import current_latest_stage_label, current_next_stage_label
from test_stage5ei_common import stage5ei_data


LATEST = parse_stage_id("Stage 5EI")
NEXT = parse_stage_id("Stage 6")


def _findings(text: str, path: str = "STATUS.md"):
    return scan_text(text, path, LATEST, NEXT)


def test_stage5ei_routes_to_stage6_and_supersedes_batch006() -> None:
    summary = stage5ei_data("summary")

    assert summary["recommended_next_stage_id"] == "stage-6"
    assert summary["operator_superseded_number_fact_review_batch_006_now"] is True
    assert summary["number_fact_review_batch_006_performed_now"] is False
    assert summary["normal_source_lock_enrichment_paused_now"] is True


def test_stage5ei_scanner_flags_known_post_stage5eh_drift_patterns() -> None:
    samples = [
        "Stage 5EG doc-staleness guardians is complete",
        "Stage 5EE current boundary",
        "after Stage 5EE",
        "Current next prompt: Stage 5EI - Source-lock number-fact review batch 006",
        "Next recommended prompt: Stage 5EI - Source-lock number-fact review batch 006",
    ]

    for sample in samples:
        findings = _findings(sample)
        assert findings, sample
        assert any(finding.severity == "error" for finding in findings)


def test_stage5ei_scanner_accepts_historical_writing() -> None:
    assert not _findings("At the time of Stage 5EG, Stage 5EG was complete and Stage 5EH was next.")
    assert not _findings("## Historical Stage 5EG Boundary")


def test_stage5ei_repository_strict_scanner_has_no_errors() -> None:
    report = audit_repository()

    assert report.error_count == 0
    assert all(not finding.path.startswith("experiments/results/") for finding in report.findings)
    assert all(not finding.path.startswith("third_party/") for finding in report.findings)
    assert all(not finding.path.startswith("data/raw/") for finding in report.findings)


def test_start_here_current_state_is_repaired() -> None:
    text = Path("docs/onboarding/start-here.md").read_text(encoding="utf-8")

    latest = parse_stage_id(current_latest_stage_label())
    next_stage = parse_stage_id(current_next_stage_label())
    findings = scan_text(text, "docs/onboarding/start-here.md", latest, next_stage)
    assert not [finding for finding in findings if finding.severity == "error"]
