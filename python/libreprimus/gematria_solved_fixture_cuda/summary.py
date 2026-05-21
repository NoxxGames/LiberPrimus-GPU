"""Build and print Stage 5M solved-fixture CUDA parity summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_solved_fixture_cuda.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_solved_fixture_cuda.models import (
    BOUNDARY_RECORDS_PATH,
    HASH_ALGORITHM,
    NEXT_STAGE_MISMATCH,
    NEXT_STAGE_PARTIAL,
    NEXT_STAGE_READY,
    NEXT_STAGE_TOOLCHAIN,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    RUN_RECORDS_PATH,
    SUMMARY_PATH,
    SUMMARY_REPORT,
)


def build_summary(
    *,
    run_records: Path = RUN_RECORDS_PATH,
    parity_records: Path = PARITY_RECORDS_PATH,
    boundaries: Path = BOUNDARY_RECORDS_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    runs = read_record_set(run_records)
    parity = read_record_set(parity_records)
    boundary_records = read_record_set(boundaries)
    pass_count = sum(1 for record in parity if record["parity_status"] == "passed")
    fail_count = sum(1 for record in parity if str(record["parity_status"]).startswith("failed"))
    skip_count = len(parity) - pass_count - fail_count
    attempted_count = sum(1 for record in runs if record.get("cuda_run_attempted") is True)
    stage5n_ready = pass_count == 5 and fail_count == 0 and skip_count == 0
    next_stage, reason = decide_next_stage(pass_count=pass_count, fail_count=fail_count, skip_count=skip_count)
    summary: dict[str, Any] = {
        "record_type": "stage5m_solved_fixture_cuda_parity_summary",
        "stage_id": "stage-5m",
        "status": "complete",
        "implemented_kernel_name": "gematria_mod29_shift_score_kernel",
        "executed_kernel": "gematria_mod29_shift_score_kernel",
        "source_contract_id": "gematria_mod29_shift_score_contract_v0",
        "executed_semantics": "gematria_shift_score_only",
        "input_mapping_records": len(runs),
        "run_records": len(runs),
        "cuda_attempted_count": attempted_count,
        "cuda_pass_count": pass_count,
        "cuda_fail_count": fail_count,
        "cuda_skip_count": skip_count,
        "parity_records": len(parity),
        "boundary_records": len(boundary_records),
        "parity_pass_count": pass_count,
        "parity_fail_count": fail_count,
        "parity_skip_count": skip_count,
        "stage5n_ready": stage5n_ready,
        "selected_next_stage": next_stage,
        "next_stage": next_stage,
        "selected_next_stage_reason": reason,
        "remaining_blockers": [] if stage5n_ready else ["stage5m_cuda_parity_not_fully_passed"],
        "newly_discovered_blockers": [] if fail_count == 0 else ["stage5m_cuda_native_hash_mismatch_or_run_failure"],
        "output_hash_algorithm": HASH_ALGORITHM,
        "per_fixture_parity": [
            {
                "mapping_id": record["mapping_id"],
                "fixture_id": record["fixture_id"],
                "native_hash": record["expected_native_output_token_hash"],
                "cuda_hash": record["cuda_output_token_hash"],
                "status": record["parity_status"],
            }
            for record in parity
        ],
        "solved_fixture_cuda_execution_allowed": True,
        "solved_fixture_cuda_execution_scope": "exact_stage5l_mapped_token_buffers_only",
        "no_gpu_ci_safe": True,
        "cuda_execution_performed": attempted_count > 0,
        "solved_fixture_cuda_used": attempted_count > 0,
        "unsolved_page_cuda_used": False,
        "real_liber_primus_cuda_data_used": False,
        "new_cuda_kernels_added": 0,
        "cuda_source_modified": True,
        "cuda_source_modification_scope": "stage5m_host_runner_only_no_device_arithmetic_change",
        "device_kernel_arithmetic_modified": False,
        "gpu_benchmark_performed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "performance_or_speedup_claims": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "codex_output_committed": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "cxx_launches_python_workers": False,
        "no_solve_claim": True,
        "solve_claim": False,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_REPORT, summary)
    write_warnings(out_dir, [])
    return summary


def decide_next_stage(*, pass_count: int, fail_count: int, skip_count: int) -> tuple[str, str]:
    if pass_count == 5 and fail_count == 0 and skip_count == 0:
        return NEXT_STAGE_READY, "All five solved-fixture-safe CUDA/native hashes matched."
    if fail_count > 0:
        return NEXT_STAGE_MISMATCH, "At least one solved-fixture-safe CUDA/native parity record failed."
    if pass_count == 0 and skip_count > 0:
        return NEXT_STAGE_TOOLCHAIN, "CUDA did not run for the bounded Stage 5M fixture set."
    return NEXT_STAGE_PARTIAL, "Only part of the bounded Stage 5M fixture set produced CUDA parity records."


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload
