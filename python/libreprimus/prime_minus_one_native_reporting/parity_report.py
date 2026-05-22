"""Build Stage 5Y compact native parity report records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, read_yaml, write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import (
    COMMON_RECORD_FLAGS,
    FULL_P56_MAPPING_ID,
    HASH_ALGORITHM,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    REPORT_FILES,
    STAGE5W_MAPPING_PATH,
    STAGE5W_SUMMARY_PATH,
    STAGE5X_PARITY_PATH,
    STAGE5X_SUMMARY_PATH,
)


def build_parity_report(
    *,
    stage5x_parity: Path = STAGE5X_PARITY_PATH,
    stage5x_summary: Path = STAGE5X_SUMMARY_PATH,
    stage5w_summary: Path = STAGE5W_SUMMARY_PATH,
    stage5w_mapping: Path = STAGE5W_MAPPING_PATH,
    parity_report_out: Path = PARITY_REPORT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    source_parity = sorted(read_records(stage5x_parity), key=lambda record: str(record.get("mapping_id")))
    stage5x_summary_payload = read_yaml(stage5x_summary)
    stage5w_summary_payload = read_yaml(stage5w_summary)
    stage5w_mappings = {record["mapping_id"]: record for record in read_records(stage5w_mapping)}
    records = []
    for source in source_parity:
        mapping_id = str(source.get("mapping_id"))
        status = str(source.get("parity_status"))
        blocked = mapping_id == FULL_P56_MAPPING_ID or status == "blocked_not_executed"
        expected_hash = source.get("expected_output_token_hash")
        computed_hash = source.get("computed_output_token_hash")
        hash_match = bool(expected_hash and computed_hash and expected_hash == computed_hash)
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "prime_minus_one_native_parity_report_record",
                "schema": "schemas/cuda/prime-minus-one-native-parity-report-record-v0.schema.json",
                "report_record_id": f"stage5y-parity-report-{mapping_id}",
                "mapping_id": mapping_id,
                "fixture_id": source.get("fixture_id"),
                "candidate_id": source.get("candidate_id"),
                "native_parity_status": status,
                "expected_output_token_hash": expected_hash,
                "computed_output_token_hash": computed_hash,
                "hash_match": hash_match,
                "output_hash_algorithm": HASH_ALGORITHM,
                "executed_in_stage5x": source.get("native_execution_performed") is True,
                "blocked_in_stage5x": blocked,
                "compact_summary_only": True,
                "source_stage5w_mapping_status": stage5w_mappings.get(mapping_id, {}).get("mapping_status", "unknown"),
                "source_stage5x_summary_status": stage5x_summary_payload.get("status"),
                "source_stage5w_summary_status": stage5w_summary_payload.get("status"),
            }
        )
    write_records(parity_report_out, records)
    write_json_report(out_dir, REPORT_FILES["parity_report"], {"records": records})
    return records
