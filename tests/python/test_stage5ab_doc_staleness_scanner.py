from __future__ import annotations

from libreprimus.doc_staleness.models import SourceOfTruth
from libreprimus.doc_staleness.scanner import scan_text


def _source() -> SourceOfTruth:
    return SourceOfTruth(
        stage_id="stage-5ab",
        latest_completed_stage_after_this_stage=(
            "Stage 5AB - markdown staleness detection hardening and stale-doc repair"
        ),
        next_stage_after_this_stage="Stage 5AC - selected from Stage 5AA outcome after stale-doc repair",
        latest_previous_stage="Stage 5AA - prime-minus-one CUDA synthetic kernel implementation and parity",
        user_override_reason="stale operational Markdown repair",
        website_expansion_status="deferred_future_unnumbered_project",
        scored_experiments_status="deferred_manifest_gate_required",
        unsolved_page_cuda_status="blocked",
        canonical_corpus_status="inactive",
        page_boundaries_status="reviewable",
        expected_next_stage_prefix="Stage 5AC",
        latest_completed_stage_prefix="Stage 5AB",
    )


def test_stage5ab_scanner_fails_stage6_website_deferral() -> None:
    findings = scan_text("Website expansion is deferred to Stage 6.\n", "README.md", _source())

    assert [finding.rule_id for finding in findings] == ["website_stage6_deferral"]


def test_stage5ab_scanner_allows_future_unnumbered_website_deferral() -> None:
    findings = scan_text(
        "Website expansion is deferred to a future unnumbered project.\n",
        "README.md",
        _source(),
    )

    assert findings == []


def test_stage5ab_scanner_fails_stale_next_stage() -> None:
    findings = scan_text("Next: Stage 5Z - old plan\n", "README.md", _source())

    assert [finding.rule_id for finding in findings] == ["stale_next_stage_claim"]


def test_stage5ab_scanner_allows_expected_next_stage_with_historical_context() -> None:
    text = "Next: Stage 5AC - selected from Stage 5AA outcome after stale-doc repair\n"

    assert scan_text(text, "README.md", _source()) == []


def test_stage5ab_scanner_allows_historical_line_and_path() -> None:
    source = _source()
    historical_line = "Historical note: Next: Stage 5Z was selected before Stage 5AA completed.\n"
    historical_path = "Next: Stage 5Z was selected before repair.\n"

    assert scan_text(historical_line, "README.md", source) == []
    assert scan_text(historical_path, "docs/development-logs/old.md", source) == []


def test_stage5ab_scanner_fails_stale_cuda_cap() -> None:
    text = "Existing CUDA code includes scaffold metadata only through Stage 5M.\n"
    findings = scan_text(text, "AGENTS.md", _source())

    assert [finding.rule_id for finding in findings] == ["stale_existing_cuda_code_cap"]


def test_stage5ab_scanner_allows_non_brittle_cuda_summary() -> None:
    text = (
        "Existing CUDA code and metadata are summarized by the latest staged-plan and CUDA notes; "
        "broad CUDA remains blocked.\n"
    )

    assert scan_text(text, "AGENTS.md", _source()) == []
