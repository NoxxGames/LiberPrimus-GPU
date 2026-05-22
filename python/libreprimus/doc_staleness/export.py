"""Export generated doc-staleness reports."""

from __future__ import annotations

import json
from pathlib import Path

from libreprimus.doc_staleness.models import ScanResult


def write_report_bundle(scan: ScanResult, findings_path: Path) -> None:
    """Write generated JSON/JSONL reports next to ``findings_path``."""

    findings_path.parent.mkdir(parents=True, exist_ok=True)
    findings = [finding.to_dict() for finding in scan.findings]
    findings_path.write_text(
        json.dumps(
            {
                "record_type": "doc_staleness_findings_report",
                "summary": scan.summary_dict(),
                "findings": findings,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (findings_path.parent / "staleness_findings.jsonl").write_text(
        "".join(json.dumps(finding, sort_keys=True) + "\n" for finding in findings),
        encoding="utf-8",
    )
    (findings_path.parent / "summary.json").write_text(
        json.dumps(scan.summary_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (findings_path.parent / "source_of_truth_comparison.json").write_text(
        json.dumps(
            {
                "record_type": "doc_staleness_source_of_truth_comparison",
                "source_of_truth": scan.source_of_truth.to_dict(),
                "strict_passed": scan.finding_count == 0,
                "finding_count": scan.finding_count,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (findings_path.parent / "repair_summary.json").write_text(
        json.dumps(
            {
                "record_type": "doc_staleness_repair_summary",
                "finding_count_after_scan": scan.finding_count,
                "files_with_findings_after_scan": list(scan.files_with_findings),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (findings_path.parent / "warnings.jsonl").write_text(
        "".join(json.dumps({"warning": warning}, sort_keys=True) + "\n" for warning in scan.warnings),
        encoding="utf-8",
    )
