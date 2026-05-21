"""Build Stage 5O repeat run records from Stage 5M/5L committed records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_repeat.models import (
    COMMON_POLICY_FLAGS,
    OUTPUT_DIR,
    REPEAT_RUN_PATH,
    REPEAT_RUN_REPORT,
    STAGE5L_NATIVE_PARITY,
    STAGE5M_PARITY_RECORDS,
    STAGE5M_RUN_RECORDS,
)


def build_repeat_run_records(
    *,
    stage5m_run_records: Path = STAGE5M_RUN_RECORDS,
    stage5m_parity_records: Path = STAGE5M_PARITY_RECORDS,
    stage5l_native_parity: Path = STAGE5L_NATIVE_PARITY,
    repeat_run_out: Path = REPEAT_RUN_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    runs = read_record_set(stage5m_run_records)
    parity_by_run = {str(record["run_record_id"]): record for record in read_record_set(stage5m_parity_records)}
    native_by_mapping = {str(record["mapping_id"]): record for record in read_record_set(stage5l_native_parity)}
    records = [
        _build_record(index=index, stage5m_run=run, stage5m_parity=parity_by_run.get(str(run["run_record_id"])), native=native_by_mapping.get(str(run["mapping_id"])))
        for index, run in enumerate(runs)
    ]
    write_record_set(repeat_run_out, records)
    write_report(out_dir, REPEAT_RUN_REPORT, {"records": records})
    return records


def _build_record(
    *,
    index: int,
    stage5m_run: dict[str, Any],
    stage5m_parity: dict[str, Any] | None,
    native: dict[str, Any] | None,
) -> dict[str, Any]:
    stage5m_hash = (stage5m_parity or stage5m_run).get("cuda_output_token_hash")
    native_hash = (native or stage5m_run).get("output_token_hash") or stage5m_run.get("expected_native_output_token_hash")
    record = {
        "record_type": "gematria_solved_fixture_cuda_repeat_run_record",
        "repeat_run_record_id": f"stage5o-repeat-run-{index:02d}",
        "run_record_id": f"stage5o-repeat-run-{index:02d}",
        "stage5m_run_record_id": stage5m_run["run_record_id"],
        "stage5m_parity_record_id": (stage5m_parity or {}).get("parity_record_id"),
        "mapping_id": stage5m_run["mapping_id"],
        "native_fixture_id": stage5m_run.get("native_fixture_id"),
        "source_input_stream_id": stage5m_run["source_input_stream_id"],
        "fixture_id": stage5m_run["fixture_id"],
        "candidate_id": stage5m_run["candidate_id"],
        "source_transform_family": stage5m_run["source_transform_family"],
        "original_transform_family_semantics_exercised": False,
        "token_values": stage5m_run["token_values"],
        "transformable_mask": stage5m_run["transformable_mask"],
        "token_kinds": stage5m_run["token_kinds"],
        "token_records": stage5m_run["token_records"],
        "candidate_shifts": stage5m_run["candidate_shifts"],
        "expected_native_output_token_hash": native_hash,
        "stage5l_native_output_token_hash": native_hash,
        "stage5m_cuda_output_token_hash": stage5m_hash,
        "stage5m_cuda_run_status": stage5m_run.get("cuda_run_status"),
        "stage5m_parity_status": (stage5m_parity or {}).get("parity_status"),
        "cuda_build_status": "pending",
        "cuda_run_status": "pending",
        "cuda_run_attempted": False,
        "cuda_output_token_hash": None,
        "cuda_native_hash_match": None,
        "cuda_status_codes": [],
        "cuda_output_token_values": [],
        "failure_reason": "",
        "warnings": [],
        "repeat_cuda_status": "pending",
        "repeat_cuda_attempted": False,
        "repeat_cuda_execution_performed": False,
        "repeat_cuda_output_token_hash": None,
        "repeat_cuda_native_hash_match": None,
        "repeat_cuda_stage5m_hash_match": None,
        "stage5p_ready": False,
        "cuda_execution_performed": False,
        "solved_fixture_cuda_used": False,
        "additional_cuda_execution_performed": False,
    }
    record.update(COMMON_POLICY_FLAGS)
    return record
