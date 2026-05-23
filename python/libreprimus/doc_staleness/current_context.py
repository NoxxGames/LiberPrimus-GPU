"""Current/next-stage consistency report helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.doc_staleness.scanner import scan_repository


def build_current_next_stage_report(
    *,
    root: Path,
    source_of_truth: Path,
    expected_latest_stage: str,
    expected_next_stage: str,
) -> dict[str, Any]:
    """Build a deterministic current/next-stage consistency report."""

    scan = scan_repository(root=root, source_of_truth_path=source_of_truth)
    findings = [finding.to_dict() for finding in scan.findings]
    return {
        "record_type": "current_next_stage_consistency_report",
        "source_of_truth": str(source_of_truth).replace("\\", "/"),
        "expected_latest_stage": expected_latest_stage,
        "expected_next_stage": expected_next_stage,
        "scanned_path_count": len(scan.scanned_paths),
        "finding_count": len(findings),
        "findings": findings,
        "warning_count": len(scan.warnings),
        "warnings": list(scan.warnings),
    }
