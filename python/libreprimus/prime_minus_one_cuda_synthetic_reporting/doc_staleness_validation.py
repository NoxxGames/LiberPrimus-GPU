"""Build Stage 5AB document-staleness validation records for Stage 5AC."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.doc_staleness.scanner import scan_repository
from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_yaml, resolve, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import (
    DOC_STALENESS_VALIDATION_PATH,
    OPERATIONAL_FILE_MAP_PATH,
    OUTPUT_DIR,
    REPORT_FILES,
    STAGE5AB_SOURCE_OF_TRUTH_PATH,
    STAGE5AB_SUMMARY_PATH,
    base_record,
)


def build_doc_staleness_validation(
    *,
    stage5ab_summary: Path = STAGE5AB_SUMMARY_PATH,
    doc_staleness_source_of_truth: Path = STAGE5AB_SOURCE_OF_TRUTH_PATH,
    operational_file_map: Path = OPERATIONAL_FILE_MAP_PATH,
    doc_staleness_validation_out: Path = DOC_STALENESS_VALIDATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    summary = read_yaml(stage5ab_summary)
    scan = scan_repository(
        root=resolve(Path(".")),
        source_of_truth_path=doc_staleness_source_of_truth,
        operational_file_map=operational_file_map,
    )
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_doc_staleness_validation_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-doc-staleness-validation-record-v0.schema.json",
            validation_record_id="stage5ac-doc-staleness-validation-v0",
            source_stage_id="stage-5ab",
            doc_staleness_source_of_truth=str(doc_staleness_source_of_truth).replace("\\", "/"),
            operational_file_map=str(operational_file_map).replace("\\", "/"),
            doc_staleness_strict_check_passed=scan.finding_count == 0,
            stale_findings_after_repair=int(summary.get("stale_findings_after_repair", 0)),
            current_doc_staleness_findings=scan.finding_count,
            current_doc_staleness_warnings=len(scan.warnings),
            operational_files_scanned=len(scan.scanned_paths),
            website_expansion_status="deferred_future_unnumbered_project",
            next_stage_expected_prefix="Stage 5AD",
            operational_docs_expected_latest="Stage 5AC - prime-minus-one CUDA synthetic parity reporting and bounded-p56 CUDA parity preflight",
            operational_docs_expected_next="Stage 5AD - bounded p56 CUDA parity run",
        )
    ]
    write_records(doc_staleness_validation_out, records)
    write_json_report(out_dir, REPORT_FILES["doc_staleness"], {"records": records, "findings": [finding.to_dict() for finding in scan.findings]})
    return records
