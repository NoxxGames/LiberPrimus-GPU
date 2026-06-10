from __future__ import annotations

from pathlib import Path

from libreprimus.doc_staleness.current_context import build_current_next_stage_report


def test_stage5ah_current_next_stage_claims_are_consistent() -> None:
    report = build_current_next_stage_report(
        root=Path("."),
        source_of_truth=Path("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml"),
        expected_latest_stage="Stage 5DX",
        expected_next_stage="Stage 5DY",
    )

    assert report["finding_count"] == 0
    assert report["warning_count"] == 0
    assert report["scanned_path_count"] >= 36
