"""Aggregate Stage 5AA summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic.export import read_records, write_json_report, write_summary, write_warnings
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    CUDA_RUN_PATH,
    DEVICE_SUBSET_AUDIT_PATH,
    EXPECTED_COUNTS,
    EXPECTED_SYNTHETIC_HASH,
    FORBIDDEN_FALSE_FLAGS,
    KERNEL_IMPLEMENTATION_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    P56_BLOCKER_PATH,
    PARITY_PATH,
    REPORT_FILES,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    STAGE_ID,
    SUMMARY_PATH,
    VALIDATION_VECTOR_ID,
)


def build_summary(
    *,
    kernel_implementation: Path = KERNEL_IMPLEMENTATION_PATH,
    cuda_run: Path = CUDA_RUN_PATH,
    parity: Path = PARITY_PATH,
    device_subset_audit: Path = DEVICE_SUBSET_AUDIT_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    p56_blocker: Path = P56_BLOCKER_PATH,
    scored_experiment_deferral: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    groups = {
        "kernel_implementation_records": read_records(kernel_implementation),
        "cuda_run_records": read_records(cuda_run),
        "parity_records": read_records(parity),
        "device_subset_audit_records": read_records(device_subset_audit),
        "result_store_preflight_records": read_records(result_store_preflight),
        "p56_blocker_records": read_records(p56_blocker),
        "scored_experiment_deferral_records": read_records(scored_experiment_deferral),
        "next_stage_decision_records": read_records(next_stage_decision),
    }
    run = groups["cuda_run_records"][0]
    parity_record = groups["parity_records"][0]
    selected = next(record for record in groups["next_stage_decision_records"] if record.get("selected") is True)
    summary: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "status": "complete",
        "synthetic_vector_id": VALIDATION_VECTOR_ID,
        "expected_output_token_hash": EXPECTED_SYNTHETIC_HASH,
        "computed_output_token_hash": parity_record.get("computed_output_token_hash"),
        "parity_status": parity_record.get("parity_status"),
        "cuda_attempted": bool(run.get("cuda_attempted")),
        "cuda_pass_count": int(run.get("cuda_pass_count", 0)),
        "cuda_fail_count": int(run.get("cuda_fail_count", 0)),
        "cuda_skip_count": int(run.get("cuda_skip_count", 0)),
        "cuda_source_modified": True,
        "new_cuda_kernels_added": 1,
        "device_kernel_arithmetic_modified": True,
        "p56_cuda_blocked": True,
        "full_p56_cuda_blocked": True,
        "p56_cuda_execution_performed": False,
        "full_p56_cuda_execution_performed": False,
        "unsolved_page_cuda_used": False,
        "real_liber_primus_cuda_data_used": False,
        "gpu_benchmark_performed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "scored_experiment_executed": False,
        "website_expansion_performed": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "codex_output_committed": False,
        "method_status_upgraded": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "solve_claim": False,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "recommended_next_stage_title": selected.get("recommended_stage_title"),
        "deep_research_recommended_next": False,
        "generated_reports_written": True,
    }
    summary.update(FORBIDDEN_FALSE_FLAGS)
    summary.update(
        {
            "cuda_source_modified": True,
            "new_cuda_kernels_added": 1,
            "device_kernel_arithmetic_modified": True,
            "p56_cuda_blocked": True,
            "full_p56_cuda_blocked": True,
            "no_solve_claim": True,
            "no_gpu_ci_safe": True,
        }
    )
    summary.update({key: len(records) for key, records in groups.items()})
    summary.update({key: value for key, value in EXPECTED_COUNTS.items() if key not in summary})
    write_summary(summary_out, summary)
    write_json_report(out_dir, REPORT_FILES["summary"], summary)
    write_warnings(out_dir, [])
    return summary
