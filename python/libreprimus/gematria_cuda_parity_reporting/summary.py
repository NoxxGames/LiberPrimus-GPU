"""Aggregate Stage 5K Gematria CUDA parity-reporting summary."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_cuda_parity_reporting.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_parity_reporting.models import (
    DEVICE_AUDIT_PATH,
    NEXT_STAGE_EXECUTION,
    NEXT_STAGE_WITH_BLOCKERS,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    PREFLIGHT_PATH,
    SCORE_PREFLIGHT_PATH,
    SUMMARY_JSON,
    SUMMARY_PATH,
)


def build_summary(
    *,
    parity_report_path: Path = PARITY_REPORT_PATH,
    device_code_audit_path: Path = DEVICE_AUDIT_PATH,
    preflight_path: Path = PREFLIGHT_PATH,
    score_preflight_path: Path = SCORE_PREFLIGHT_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    parity_records = read_record_set(parity_report_path)
    audit_records = read_record_set(device_code_audit_path)
    preflight_records = read_record_set(preflight_path)
    score_preflight_records = read_record_set(score_preflight_path)
    parity = parity_records[0] if parity_records else {}
    audit = audit_records[0] if audit_records else {}
    unique_blockers = sorted({str(blocker) for record in preflight_records for blocker in record.get("blockers", [])})
    readiness_counts = dict(sorted(Counter(str(record.get("readiness_status")) for record in preflight_records).items()))
    blocker_count = len(unique_blockers)
    next_stage = NEXT_STAGE_WITH_BLOCKERS if blocker_count else NEXT_STAGE_EXECUTION
    next_reason = (
        "Solved-fixture-safe blockers remain for token mapping, native fixture output hashes, "
        "score-summary parity, no-unsolved guardrails, and future-stage approval."
        if blocker_count
        else "All blockers except explicit execution approval are clear."
    )
    summary: dict[str, Any] = {
        "record_type": "stage5k_gematria_cuda_parity_reporting_summary",
        "stage_id": "stage-5k",
        "status": "complete",
        "parity_report_records": len(parity_records),
        "device_code_audit_records": len(audit_records),
        "solved_fixture_safe_preflight_records": len(preflight_records),
        "score_summary_preflight_records": len(score_preflight_records),
        "implemented_kernel_name": parity.get("implemented_kernel_name"),
        "source_contract_id": parity.get("source_contract_id"),
        "native_fixture_hash": parity.get("native_fixture_hash"),
        "cuda_output_hash": parity.get("cuda_output_hash"),
        "cuda_native_hash_match": parity.get("cuda_native_hash_match"),
        "gematria_cuda_synthetic_parity_verified": parity.get("gematria_cuda_synthetic_parity_verified"),
        "device_code_subset_compliant": audit.get("device_code_subset_compliant"),
        "stl_used_in_cuda_device_path": audit.get("stl_used_in_cuda_device_path"),
        "std_array_used_in_cuda_device_path": audit.get("std_array_used_in_cuda_device_path"),
        "std_vector_used_in_cuda_device_path": audit.get("std_vector_used_in_cuda_device_path"),
        "std_string_used_in_cuda_device_path": audit.get("std_string_used_in_cuda_device_path"),
        "cxx_exceptions_in_cuda_device_path": audit.get("cxx_exceptions_in_cuda_device_path"),
        "throw_used_in_cuda_device_path": audit.get("throw_used_in_cuda_device_path"),
        "dynamic_allocation_in_device_code": audit.get("dynamic_allocation_in_device_code"),
        "lambdas_in_cuda_device_path": audit.get("lambdas_in_cuda_device_path"),
        "cxx_ownership_types_cross_kernel_boundary": audit.get("cxx_ownership_types_cross_kernel_boundary"),
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "cuda_source_modified": False,
        "cuda_execution_performed": False,
        "optional_local_cuda_revalidation_performed": False,
        "synthetic_only": True,
        "solved_fixture_cuda_execution_allowed": False,
        "production_gematria_mod29_cuda_ready": False,
        "real_liber_primus_data_used": False,
        "solved_fixture_cuda_used": False,
        "unsolved_page_cuda_used": False,
        "gpu_benchmark_performed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "performance_or_speedup_claims": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "raw_data_processed": False,
        "website_expansion": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "local_16gb_profile_required": False,
        "ci_gpu_required": False,
        "no_gpu_ci_safe": True,
        "python_semantic_reference_preserved": True,
        "cxx_launches_python_workers": False,
        "no_solve_claim": True,
        "solve_claim": False,
        "score_summary_contract": "stage4i",
        "score_interpretation": "triage_only",
        "blockers": unique_blockers,
        "blocker_count": blocker_count,
        "readiness_status_counts": readiness_counts,
        "selected_next_stage": next_stage,
        "next_stage": next_stage,
        "next_stage_reason": next_reason,
        "recommended_next_prompt": next_stage,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_JSON, summary)
    write_warnings(out_dir, [])
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload
