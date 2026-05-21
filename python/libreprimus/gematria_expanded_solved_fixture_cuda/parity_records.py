"""Build Stage 5R CUDA/native parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_solved_fixture_cuda.models import COMMON_POLICY_FLAGS, OUTPUT_DIR, PARITY_RECORDS_PATH, PARITY_REPORT, RUN_RECORDS_PATH


def build_parity_records(
    *,
    run_records: Path = RUN_RECORDS_PATH,
    parity_records_out: Path = PARITY_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_record_from_run(record) for record in read_record_set(run_records)]
    write_record_set(parity_records_out, records)
    write_report(out_dir, PARITY_REPORT, {"records": records})
    return records


def _record_from_run(record: dict[str, Any]) -> dict[str, Any]:
    status = _parity_status(record)
    parity = {
        "record_type": "gematria_expanded_solved_fixture_cuda_parity_record",
        "parity_record_id": record["run_record_id"].replace("run", "parity"),
        "run_record_id": record["run_record_id"],
        "candidate_inventory_id": record["candidate_inventory_id"],
        "token_mapping_record_id": record["token_mapping_record_id"],
        "native_parity_record_id": record["native_parity_record_id"],
        "fixture_id": record["fixture_id"],
        "candidate_id": record["candidate_id"],
        "source_input_stream_id": record["source_input_stream_id"],
        "source_transform_family": record["source_transform_family"],
        "expected_native_output_token_hash": record["expected_native_output_token_hash"],
        "stage5q_native_output_token_hash": record["stage5q_native_output_token_hash"],
        "stage5r_cuda_output_token_hash": record.get("stage5r_cuda_output_token_hash"),
        "cuda_output_token_hash": record.get("cuda_output_token_hash"),
        "cuda_native_hash_match": record.get("cuda_native_hash_match"),
        "parity_status": status,
        "cuda_run_status": record["cuda_run_status"],
        "cuda_build_status": record["cuda_build_status"],
        "cuda_run_attempted": record["cuda_run_attempted"],
        "failure_reason": record.get("failure_reason", ""),
        "stage5s_ready": status == "passed",
        "cuda_execution_performed": record["cuda_execution_performed"],
        "solved_fixture_cuda_used": record["solved_fixture_cuda_used"],
    }
    parity.update(COMMON_POLICY_FLAGS)
    return parity


def _parity_status(record: dict[str, Any]) -> str:
    if record["cuda_run_status"] == "passed" and record.get("cuda_native_hash_match") is True:
        return "passed"
    if str(record["cuda_run_status"]).startswith("skipped"):
        return record["cuda_run_status"]
    if record.get("cuda_native_hash_match") is False:
        return "failed_hash_mismatch"
    if str(record["cuda_build_status"]).startswith("failed"):
        return "skipped_build_not_passed"
    return "failed_cuda_run"
