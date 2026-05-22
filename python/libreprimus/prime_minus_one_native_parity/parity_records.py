"""Stage 5X native parity comparison records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_parity.models import COMMON_RECORD_FLAGS, NATIVE_PARITY_PATH, NATIVE_RUN_PATH, OUTPUT_DIR, REPORT_FILES


def build_parity_records(
    *,
    native_run: Path = NATIVE_RUN_PATH,
    native_parity_out: Path = NATIVE_PARITY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_parity_record(record) for record in read_records(native_run)]
    write_records(native_parity_out, records)
    write_json_report(out_dir, REPORT_FILES["native_parity"], {"records": records})
    return records


def _parity_record(run: dict[str, Any]) -> dict[str, Any]:
    if run["native_execution_status"] == "skipped_blocked_full_p56":
        status = "blocked_not_executed"
    elif run.get("computed_output_token_hash") == run.get("expected_output_token_hash"):
        status = "passed"
    else:
        status = "failed_hash_mismatch"
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_native_parity_record",
        "schema": "schemas/cuda/prime-minus-one-native-parity-record-v0.schema.json",
        "parity_record_id": f"stage5x-parity-{run['mapping_id']}",
        "mapping_id": run["mapping_id"],
        "fixture_id": run["fixture_id"],
        "candidate_id": run.get("candidate_id"),
        "expected_output_token_hash": run.get("expected_output_token_hash"),
        "computed_output_token_hash": run.get("computed_output_token_hash"),
        "formula_output_token_hash": run.get("formula_output_token_hash"),
        "output_hash_algorithm": run["output_hash_algorithm"],
        "parity_status": status,
        "native_execution_status": run["native_execution_status"],
        "python_reference_execution_performed": run.get("python_reference_execution_performed") is True,
        "native_execution_performed": run.get("native_execution_performed") is True,
        "blockers": list(run.get("blockers", [])),
    }
