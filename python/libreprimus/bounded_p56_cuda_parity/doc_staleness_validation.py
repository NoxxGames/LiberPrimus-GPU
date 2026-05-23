"""Document-staleness validation records for Stage 5AD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.doc_staleness.models import DEFAULT_SOURCE_OF_TRUTH
from libreprimus.doc_staleness.scanner import scan_repository

from .export import resolve, write_json_report, write_records
from .models import DOC_STALENESS_VALIDATION_PATH, OPERATIONAL_FILE_MAP_PATH, OUTPUT_DIR, REPORT_FILES, STAGE5AB_SOURCE_OF_TRUTH_PATH, base_record

ACTIVE_SOURCE_OF_TRUTH_PATH = Path(DEFAULT_SOURCE_OF_TRUTH)


def build_doc_staleness_validation(
    *, doc_staleness_validation_out: Path = DOC_STALENESS_VALIDATION_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    result = scan_repository(
        root=resolve(Path(".")),
        source_of_truth_path=ACTIVE_SOURCE_OF_TRUTH_PATH,
        operational_file_map=OPERATIONAL_FILE_MAP_PATH,
    )
    current_findings = list(result.findings)
    record = base_record(
        "bounded_p56_cuda_doc_staleness_validation_record",
        "schemas/cuda/bounded-p56-cuda-doc-staleness-validation-record-v0.schema.json",
        doc_staleness_validation_id="stage5ad-doc-staleness-validation-v0",
        latest_stage_context="stage-5ad",
        doc_staleness_source_of_truth=str(ACTIVE_SOURCE_OF_TRUTH_PATH),
        historical_doc_staleness_source_of_truth=str(STAGE5AB_SOURCE_OF_TRUTH_PATH),
        operational_file_map=str(OPERATIONAL_FILE_MAP_PATH),
        stage5ab_source_of_truth_consumed=resolve(STAGE5AB_SOURCE_OF_TRUTH_PATH).exists(),
        active_source_of_truth_consumed=resolve(ACTIVE_SOURCE_OF_TRUTH_PATH).exists(),
        operational_file_map_consumed=resolve(OPERATIONAL_FILE_MAP_PATH).exists(),
        doc_staleness_strict_check_passed=len(current_findings) == 0,
        stale_findings_after_repair=len(current_findings),
        website_expansion_status="deferred_future_unnumbered_project",
        operational_docs_expected_latest="Stage 5AD - bounded p56 CUDA parity run",
        operational_docs_expected_next="dynamic_from_parity_status",
    )
    records = [record]
    write_records(doc_staleness_validation_out, records)
    write_json_report(out_dir, REPORT_FILES["doc_staleness"], {"records": records, "findings": [finding.to_dict() for finding in current_findings]})
    return records
