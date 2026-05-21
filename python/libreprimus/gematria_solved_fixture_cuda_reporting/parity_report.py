"""Build Stage 5N parity report records from Stage 5M outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_solved_fixture_cuda_reporting.export import (
    common_policy_fields,
    read_record_set,
    write_record_set,
    write_report,
)
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    HASH_ALGORITHM,
    OUTPUT_DIR,
    PARITY_REPORT_JSON,
    PARITY_REPORT_PATH,
    STAGE5M_PARITY_RECORDS,
    STAGE5M_RUN_RECORDS,
    STAGE5M_SUMMARY,
)


def build_parity_report(
    *,
    stage5m_run_records: Path = STAGE5M_RUN_RECORDS,
    stage5m_parity_records: Path = STAGE5M_PARITY_RECORDS,
    stage5m_summary: Path = STAGE5M_SUMMARY,
    parity_report_out: Path = PARITY_REPORT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    runs = {record["run_record_id"]: record for record in read_record_set(stage5m_run_records)}
    parity_records = read_record_set(stage5m_parity_records)
    stage5m = read_yaml(stage5m_summary)
    records: list[dict[str, Any]] = []
    for index, parity in enumerate(parity_records):
        run = runs[str(parity["run_record_id"])]
        records.append(
            {
                "record_type": "gematria_solved_fixture_cuda_report_record",
                "report_record_id": f"stage5n-parity-report-{index:02d}",
                "source_stage_id": "stage-5m",
                "source_parity_record_id": parity["parity_record_id"],
                "source_run_record_id": parity["run_record_id"],
                "mapping_id": parity["mapping_id"],
                "fixture_id": parity["fixture_id"],
                "source_input_stream_id": parity["source_input_stream_id"],
                "candidate_id": parity["candidate_id"],
                "original_transform_family": parity["source_transform_family"],
                "executed_kernel": parity["executed_kernel"],
                "executed_semantics": parity["executed_semantics"],
                "original_transform_family_semantics_exercised": bool(
                    parity["original_transform_family_semantics_exercised"]
                ),
                "native_hash": parity["expected_native_output_token_hash"],
                "cuda_hash": parity["cuda_output_token_hash"],
                "parity_status": parity["parity_status"],
                "token_count": len(run.get("token_values", [])),
                "candidate_shifts": list(run.get("candidate_shifts", [])),
                "output_hash_algorithm": HASH_ALGORITHM,
                "solved_fixture_cuda_execution_scope": parity["solved_fixture_cuda_execution_scope"],
                "stage5m_run_records": int(stage5m["run_records"]),
                "stage5m_parity_records": int(stage5m["parity_records"]),
                "stage5m_parity_pass_count": int(stage5m["parity_pass_count"]),
                "stage5m_parity_fail_count": int(stage5m["parity_fail_count"]),
                "stage5m_parity_skip_count": int(stage5m["parity_skip_count"]),
                "not_production_broad_cuda_readiness": True,
                **common_policy_fields(),
            }
        )
    write_record_set(parity_report_out, records)
    write_report(out_dir, PARITY_REPORT_JSON, {"records": records})
    return records
