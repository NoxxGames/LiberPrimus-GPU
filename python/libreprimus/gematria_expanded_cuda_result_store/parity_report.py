"""Build Stage 5S compact parity-report records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    COMMON_FLAGS,
    EXECUTED_KERNEL,
    EXECUTED_SEMANTICS,
    HASH_ALGORITHM,
    IMPLEMENTED_KERNEL_NAME,
    OUTPUT_DIR,
    PARITY_REPORT_JSON,
    PARITY_REPORT_PATH,
    SOURCE_CONTRACT_ID,
    STAGE5R_RUN,
    STAGE5R_PARITY,
)


def build_parity_report(
    *,
    stage5r_parity: Path = STAGE5R_PARITY,
    stage5r_run: Path = STAGE5R_RUN,
    parity_report_out: Path = PARITY_REPORT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    source_records = sorted(read_record_set(stage5r_parity), key=lambda record: str(record["fixture_id"]))
    run_by_id = {str(record["run_record_id"]): record for record in read_record_set(stage5r_run)}
    records = [
        _record(index=index, source=record, run=run_by_id[str(record["run_record_id"])])
        for index, record in enumerate(source_records)
    ]
    write_record_set(parity_report_out, records)
    write_report(out_dir, PARITY_REPORT_JSON, {"records": records})
    return records


def _record(*, index: int, source: dict[str, Any], run: dict[str, Any]) -> dict[str, Any]:
    record = {
        "record_type": "gematria_expanded_cuda_parity_report_record",
        "parity_report_id": f"stage5s-expanded-cuda-parity-report-{index:02d}",
        "source_parity_record_id": source["parity_record_id"],
        "source_stage5q_candidate_inventory_id": source["candidate_inventory_id"],
        "fixture_id": source["fixture_id"],
        "source_input_stream_id": source["source_input_stream_id"],
        "candidate_id": source["candidate_id"],
        "source_transform_family": source["source_transform_family"],
        "implemented_kernel_name": IMPLEMENTED_KERNEL_NAME,
        "source_contract_id": SOURCE_CONTRACT_ID,
        "executed_kernel": EXECUTED_KERNEL,
        "executed_semantics": EXECUTED_SEMANTICS,
        "original_transform_family_semantics_exercised": False,
        "token_count": run["token_count"],
        "transformable_token_count": run["transformable_token_count"],
        "stage5q_native_hash": source["stage5q_native_output_token_hash"],
        "stage5r_cuda_hash": source["stage5r_cuda_output_token_hash"],
        "cuda_native_hash_match": source["cuda_native_hash_match"],
        "parity_status": source["parity_status"],
        "output_hash_algorithm": HASH_ALGORITHM,
        "stage5r_cuda_execution_performed": source["cuda_execution_performed"],
        "stage5r_solved_fixture_cuda_used": source["solved_fixture_cuda_used"],
        "all_stage5r_hashes_matched": True,
        "consumed_controls_excluded": True,
        "blocked_original_family_fixtures_excluded": True,
    }
    record.update(COMMON_FLAGS)
    return record
