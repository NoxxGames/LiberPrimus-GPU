"""Build and print Stage 5R expanded solved-fixture CUDA parity summaries."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_expanded_solved_fixture_cuda.models import (
    HASH_ALGORITHM,
    NEXT_STAGE_MISMATCH,
    NEXT_STAGE_PARTIAL,
    NEXT_STAGE_READY,
    NEXT_STAGE_TOOLCHAIN,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    RUN_RECORDS_PATH,
    SCORE_SUMMARY_CONTRACT,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    STAGE5Q_SUMMARY,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    BOUNDARY_RECORDS_PATH,
)


def build_summary(
    *,
    run_records: Path = RUN_RECORDS_PATH,
    parity_records: Path = PARITY_RECORDS_PATH,
    boundaries: Path = BOUNDARY_RECORDS_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    stage5q_summary: Path = STAGE5Q_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    runs = read_record_set(run_records)
    parity = read_record_set(parity_records)
    boundary_records = read_record_set(boundaries)
    result_store = read_record_set(result_store_preflight)
    score = read_record_set(score_summary_preflight)
    stage5q = read_yaml(stage5q_summary)
    pass_count = sum(1 for record in parity if record["parity_status"] == "passed")
    fail_count = sum(1 for record in parity if str(record["parity_status"]).startswith("failed"))
    skip_count = len(parity) - pass_count - fail_count
    attempted_count = sum(1 for record in runs if record.get("cuda_run_attempted") is True)
    stage5s_ready = pass_count == 3 and fail_count == 0 and skip_count == 0
    next_stage, reason = decide_next_stage(pass_count=pass_count, fail_count=fail_count, skip_count=skip_count)
    summary: dict[str, Any] = {
        "record_type": "stage5r_expanded_solved_fixture_cuda_parity_summary",
        "stage_id": "stage-5r",
        "status": "complete",
        "source_stage_id": "stage-5q",
        "implemented_kernel_name": "gematria_mod29_shift_score_kernel",
        "executed_kernel": "gematria_mod29_shift_score_kernel",
        "source_contract_id": "gematria_mod29_shift_score_contract_v0",
        "executed_semantics": "gematria_shift_score_only",
        "input_stage5q_mapped_candidates": int(stage5q["mapped_count"]),
        "run_records": len(runs),
        "cuda_attempted_count": attempted_count,
        "cuda_pass_count": pass_count,
        "cuda_fail_count": fail_count,
        "cuda_skip_count": skip_count,
        "parity_records": len(parity),
        "parity_pass_count": pass_count,
        "parity_fail_count": fail_count,
        "parity_skip_count": skip_count,
        "boundary_records": len(boundary_records),
        "result_store_preflight_records": len(result_store),
        "result_store_preflight_ready_count": sum(1 for record in result_store if record.get("stage5s_ready") is True),
        "score_summary_preflight_records": len(score),
        "score_summary_preflight_ready_count": sum(1 for record in score if record.get("stage5s_ready") is True),
        "stage4p_compatibility": all(record.get("stage4p_compatibility") is True for record in result_store),
        "stage4i_compatibility": all(record.get("score_interpretation") == "triage_only" for record in score),
        "stage5s_ready": stage5s_ready,
        "selected_next_stage": next_stage,
        "next_stage": next_stage,
        "selected_next_stage_reason": reason,
        "remaining_blockers": [] if stage5s_ready else ["stage5r_cuda_parity_not_fully_passed"],
        "newly_discovered_blockers": [] if fail_count == 0 else ["stage5r_cuda_native_hash_mismatch_or_run_failure"],
        "output_hash_algorithm": HASH_ALGORITHM,
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "parity_status_counts": dict(sorted(Counter(record["parity_status"] for record in parity).items())),
        "per_fixture_parity": [
            {
                "candidate_inventory_id": record["candidate_inventory_id"],
                "fixture_id": record["fixture_id"],
                "source_input_stream_id": record["source_input_stream_id"],
                "token_count": next(run["token_count"] for run in runs if run["run_record_id"] == record["run_record_id"]),
                "transformable_token_count": next(
                    run["transformable_token_count"] for run in runs if run["run_record_id"] == record["run_record_id"]
                ),
                "stage5q_native_hash": record["stage5q_native_output_token_hash"],
                "stage5r_cuda_hash": record["stage5r_cuda_output_token_hash"],
                "status": record["parity_status"],
            }
            for record in parity
        ],
        "solved_fixture_cuda_execution_allowed": True,
        "solved_fixture_cuda_execution_scope": "exact_three_stage5q_mapped_direct_translation_candidates_only",
        "approved_stage5r_scope": "exact_three_stage5q_mapped_direct_translation_candidates_only",
        "consumed_controls_excluded": True,
        "blocked_original_family_fixtures_excluded": True,
        "original_transform_family_semantics_exercised": False,
        "cuda_execution_performed": attempted_count > 0,
        "solved_fixture_cuda_used": attempted_count > 0,
        "unsolved_page_cuda_used": False,
        "real_liber_primus_cuda_data_used": False,
        "real_liber_primus_data_used": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "cuda_source_modified": False,
        "device_kernel_arithmetic_modified": False,
        "gpu_benchmark_performed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "performance_or_speedup_claims": False,
        "generated_body_publication_allowed": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "codex_output_committed": False,
        "method_status_upgrade_allowed": False,
        "method_status_upgraded": False,
        "deep_research_recommended": False,
        "website_expansion": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "ci_gpu_required": False,
        "no_gpu_ci_safe": True,
        "local_16gb_profile_required": False,
        "cxx_launches_python_workers": False,
        "no_solve_claim": True,
        "solve_claim": False,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_REPORT, summary)
    write_warnings(out_dir, [])
    return summary


def decide_next_stage(*, pass_count: int, fail_count: int, skip_count: int) -> tuple[str, str]:
    if pass_count == 3 and fail_count == 0 and skip_count == 0:
        return NEXT_STAGE_READY, "All three Stage 5Q expanded solved-fixture CUDA/native hashes matched."
    if fail_count > 0:
        return NEXT_STAGE_MISMATCH, "At least one expanded solved-fixture CUDA/native parity record failed."
    if pass_count == 0 and skip_count > 0:
        return NEXT_STAGE_TOOLCHAIN, "CUDA did not run for the bounded Stage 5R fixture set."
    return NEXT_STAGE_PARTIAL, "Only part of the bounded Stage 5R fixture set produced CUDA parity records."


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload
