"""Build Stage 5M CUDA/native parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda.models import OUTPUT_DIR, PARITY_RECORDS_PATH, PARITY_REPORT, RUN_RECORDS_PATH


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
    if record["cuda_run_status"] == "passed" and record["cuda_native_hash_match"] is True:
        parity_status = "passed"
    elif record["cuda_run_status"] == "passed":
        parity_status = "failed_hash_mismatch"
    elif str(record["cuda_run_status"]).startswith("skipped"):
        parity_status = record["cuda_run_status"]
    elif str(record["cuda_build_status"]).startswith("failed"):
        parity_status = "skipped_build_not_passed"
    else:
        parity_status = "failed_cuda_run"
    return {
        "record_type": "gematria_solved_fixture_cuda_parity_record",
        "parity_record_id": record["run_record_id"].replace("cuda-run", "cuda-parity"),
        "run_record_id": record["run_record_id"],
        "mapping_id": record["mapping_id"],
        "native_fixture_id": record["native_fixture_id"],
        "fixture_id": record["fixture_id"],
        "candidate_id": record["candidate_id"],
        "source_input_stream_id": record["source_input_stream_id"],
        "source_transform_family": record["source_transform_family"],
        "executed_kernel": record["executed_kernel"],
        "executed_semantics": record["executed_semantics"],
        "original_transform_family_semantics_exercised": record["original_transform_family_semantics_exercised"],
        "expected_native_output_token_hash": record["expected_native_output_token_hash"],
        "cuda_output_token_hash": record["cuda_output_token_hash"],
        "cuda_native_hash_match": record["cuda_native_hash_match"],
        "parity_status": parity_status,
        "cuda_run_status": record["cuda_run_status"],
        "cuda_build_status": record["cuda_build_status"],
        "failure_reason": record.get("failure_reason", ""),
        "stage5n_ready": parity_status == "passed",
        **{key: record[key] for key in _POLICY_KEYS if key in record},
    }


_POLICY_KEYS = (
    "stage_id",
    "implemented_kernel_name",
    "source_contract_id",
    "token_domain",
    "arithmetic_direction",
    "arithmetic_formula",
    "separator_policy",
    "solved_fixture_cuda_execution_allowed",
    "solved_fixture_cuda_execution_scope",
    "cuda_execution_performed",
    "solved_fixture_cuda_used",
    "unsolved_page_cuda_used",
    "real_liber_primus_cuda_data_used",
    "real_liber_primus_data_used",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "performance_or_speedup_claims",
    "broad_experiment_executed",
    "raw_data_processed",
    "generated_outputs_committed",
    "codex_output_committed",
    "website_expansion",
    "canonical_corpus_active",
    "page_boundaries_final",
    "ci_gpu_required",
    "no_gpu_ci_safe",
    "new_cuda_kernel_added",
    "new_cuda_kernels_added",
    "cuda_source_modified",
    "device_kernel_arithmetic_modified",
    "cxx_launches_python_workers",
    "no_solve_claim",
    "solve_claim",
)
