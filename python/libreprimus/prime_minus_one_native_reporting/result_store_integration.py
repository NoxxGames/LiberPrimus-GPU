"""Build Stage 4P-compatible Stage 5Y result-store integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, OUTPUT_DIR, PARITY_REPORT_PATH, REPORT_FILES, RESULT_STORE_INTEGRATION_PATH


def build_result_store_integration(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    result_store_integration_out: Path = RESULT_STORE_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = []
    for report in read_records(parity_report):
        mapping_id = str(report.get("mapping_id"))
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "prime_minus_one_native_result_store_integration_record",
                "schema": "schemas/cuda/prime-minus-one-native-result-store-integration-record-v0.schema.json",
                "integration_record_id": f"stage5y-result-store-{mapping_id}",
                "mapping_id": mapping_id,
                "fixture_id": report.get("fixture_id"),
                "candidate_id": report.get("candidate_id"),
                "result_source_kind": "prime_minus_one_no_gpu_native_parity",
                "allowed_committed_record_type": "compact_summary_metadata_only",
                "generated_body_publication_allowed": False,
                "output_token_hash_required": True,
                "output_text_hash_policy": "blocked_pending_transliteration_policy",
                "result_store_contract": "stage4p",
                "score_summary_contract": "stage4i",
                "stage4p_compatibility": "compatible",
                "source_presence_status": "committed_summary_present",
                "method_status": "infrastructure",
                "method_status_upgrade_allowed": False,
                "performance_claim_allowed": False,
                "speedup_claim_allowed": False,
                "solve_claim": False,
                "hash_available": bool(report.get("computed_output_token_hash")),
                "hash_match": report.get("hash_match"),
                "compact_summary_only": True,
            }
        )
    write_records(result_store_integration_out, records)
    write_json_report(out_dir, REPORT_FILES["result_store"], {"records": records})
    return records
