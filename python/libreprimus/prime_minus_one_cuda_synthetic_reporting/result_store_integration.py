"""Build Stage 4P-compatible result-store integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import OUTPUT_DIR, PARITY_REPORT_PATH, REPORT_FILES, RESULT_STORE_INTEGRATION_PATH, base_record


def build_result_store_integration(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    result_store_integration_out: Path = RESULT_STORE_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    report = read_records(parity_report)[0]
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_result_store_integration_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-result-store-integration-record-v0.schema.json",
            integration_record_id="stage5ac-result-store-synthetic-parity-v0",
            source_report_record_id=report.get("report_record_id"),
            result_source_kind="prime_minus_one_cuda_synthetic_parity_metadata",
            result_store_contract="stage4p",
            score_summary_contract="stage4i",
            stage4p_compatibility="compatible",
            allowed_committed_record_type="compact_summary_metadata_only",
            source_presence_status="committed_summary_present",
            output_token_hash_required=True,
            output_token_hash=report.get("computed_output_token_hash"),
            output_text_hash_policy="not_applicable_numeric_token_parity",
            generated_body_publication_allowed=False,
            method_status="infrastructure",
            performance_claim_allowed=False,
            speedup_claim_allowed=False,
            hash_available=bool(report.get("computed_output_token_hash")),
            hash_match=report.get("stage5aa_hash_match"),
        )
    ]
    write_records(result_store_integration_out, records)
    write_json_report(out_dir, REPORT_FILES["result_store"], {"records": records})
    return records
