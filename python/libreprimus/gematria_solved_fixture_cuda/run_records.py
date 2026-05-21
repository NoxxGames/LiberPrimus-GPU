"""Build Stage 5M solved-fixture CUDA run records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda.models import (
    COMMON_POLICY_FLAGS,
    EXECUTED_SEMANTICS,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    RUN_RECORDS_PATH,
    RUN_REPORT,
    TOKEN_MAPPING_PATH,
)


def build_run_records(
    *,
    token_mapping: Path = TOKEN_MAPPING_PATH,
    native_parity: Path = NATIVE_PARITY_PATH,
    run_records_out: Path = RUN_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    mappings = read_record_set(token_mapping)
    native_by_mapping = {record["mapping_id"]: record for record in read_record_set(native_parity)}
    records = [
        _build_record(index=index, mapping=mapping, native=native_by_mapping.get(str(mapping["mapping_id"])))
        for index, mapping in enumerate(mappings)
    ]
    write_record_set(run_records_out, records)
    write_report(out_dir, RUN_REPORT, {"records": records})
    return records


def _build_record(*, index: int, mapping: dict[str, Any], native: dict[str, Any] | None) -> dict[str, Any]:
    native_hash = native.get("output_token_hash") if native else None
    native_fixture_id = native.get("native_fixture_id") if native else None
    return {
        "record_type": "gematria_solved_fixture_cuda_run_record",
        "run_record_id": f"stage5m-cuda-run-{index:02d}",
        "mapping_id": mapping["mapping_id"],
        "native_fixture_id": native_fixture_id,
        "source_input_stream_id": mapping["source_input_stream_id"],
        "fixture_id": mapping["fixture_id"],
        "candidate_id": mapping["candidate_id"],
        "source_transform_family": mapping["transform_family"],
        "executed_semantics": EXECUTED_SEMANTICS,
        "original_transform_family_semantics_exercised": False,
        "token_values": mapping["token_values"],
        "transformable_mask": mapping["transformable_mask"],
        "token_kinds": mapping["token_kinds"],
        "token_records": mapping["token_records"],
        "candidate_shifts": native.get("candidate_shifts", []) if native else [],
        "expected_native_output_token_hash": native_hash,
        "cuda_build_status": "pending",
        "cuda_run_status": "pending",
        "cuda_run_attempted": False,
        "cuda_output_token_hash": None,
        "cuda_native_hash_match": None,
        "cuda_status_codes": [],
        "cuda_output_token_values": [],
        "failure_reason": "",
        "warnings": [],
        "cuda_source_modified": True,
        "cuda_source_modification_scope": "stage5m_host_runner_only_no_device_arithmetic_change",
        "solved_fixture_cuda_used": False,
        "stage5n_ready": False,
        **COMMON_POLICY_FLAGS,
    }
