"""Build Stage 5O repeat parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_repeat.models import COMMON_POLICY_FLAGS, OUTPUT_DIR, REPEAT_PARITY_PATH, REPEAT_PARITY_REPORT, REPEAT_RUN_PATH


def build_repeat_parity_records(
    *,
    repeat_run_records: Path = REPEAT_RUN_PATH,
    repeat_parity_out: Path = REPEAT_PARITY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_record_from_run(record) for record in read_record_set(repeat_run_records)]
    write_record_set(repeat_parity_out, records)
    write_report(out_dir, REPEAT_PARITY_REPORT, {"records": records})
    return records


def _record_from_run(record: dict[str, Any]) -> dict[str, Any]:
    status = _parity_status(record)
    parity = {
        "record_type": "gematria_solved_fixture_cuda_repeat_parity_record",
        "repeat_parity_record_id": record["repeat_run_record_id"].replace("repeat-run", "repeat-parity"),
        "repeat_run_record_id": record["repeat_run_record_id"],
        "stage5m_run_record_id": record["stage5m_run_record_id"],
        "stage5m_parity_record_id": record.get("stage5m_parity_record_id"),
        "mapping_id": record["mapping_id"],
        "native_fixture_id": record["native_fixture_id"],
        "fixture_id": record["fixture_id"],
        "candidate_id": record["candidate_id"],
        "source_input_stream_id": record["source_input_stream_id"],
        "source_transform_family": record["source_transform_family"],
        "expected_native_output_token_hash": record["stage5l_native_output_token_hash"],
        "stage5m_cuda_output_token_hash": record["stage5m_cuda_output_token_hash"],
        "stage5o_repeat_cuda_output_token_hash": record["repeat_cuda_output_token_hash"],
        "stage5l_native_hash_match": record["repeat_cuda_native_hash_match"],
        "stage5m_cuda_hash_match": record["repeat_cuda_stage5m_hash_match"],
        "repeat_parity_status": status,
        "repeat_cuda_status": record["repeat_cuda_status"],
        "cuda_build_status": record["cuda_build_status"],
        "failure_reason": record.get("failure_reason", ""),
        "stage5p_result_store_preflight_ready": status == "passed",
        "cuda_execution_performed": record["cuda_execution_performed"],
        "solved_fixture_cuda_used": record["solved_fixture_cuda_used"],
        "additional_cuda_execution_performed": record["additional_cuda_execution_performed"],
    }
    parity.update(COMMON_POLICY_FLAGS)
    return parity


def _parity_status(record: dict[str, Any]) -> str:
    if record["repeat_cuda_status"] == "passed" and record["repeat_cuda_native_hash_match"] is True and record["repeat_cuda_stage5m_hash_match"] is True:
        return "passed"
    if str(record["repeat_cuda_status"]).startswith("skipped"):
        return record["repeat_cuda_status"]
    if record["repeat_cuda_native_hash_match"] is False or record["repeat_cuda_stage5m_hash_match"] is False:
        return "failed_hash_mismatch"
    if str(record["cuda_build_status"]).startswith("failed"):
        return "skipped_build_not_passed"
    return "failed_cuda_run"
