"""Aggregate Stage 5B CUDA parity harness summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_json, write_yaml
from libreprimus.cuda_parity.loaders import load_records
from libreprimus.cuda_parity.models import (
    BACKEND_CAPABILITY_PATH,
    CUDA_PARITY_POLICY,
    FUTURE_KERNEL_MATRIX_PATH,
    HARNESS_PLAN_PATH,
    PARITY_FIXTURES_PATH,
    STAGE5A_TARGET_PLAN_PATH,
    STAGE5A_SUMMARY_PATH,
    STAGE5A_NON_TARGETS_PATH,
    STAGE5B_OUTPUT_DIR,
    SUMMARY_PATH,
    SUMMARY_REPORT,
)


def build_summary(
    *,
    harness_plan_path: Path = HARNESS_PLAN_PATH,
    parity_fixtures_path: Path = PARITY_FIXTURES_PATH,
    backend_capability_path: Path = BACKEND_CAPABILITY_PATH,
    future_kernel_matrix_path: Path = FUTURE_KERNEL_MATRIX_PATH,
    target_plan_path: Path = STAGE5A_TARGET_PLAN_PATH,
    stage5a_summary_path: Path = STAGE5A_SUMMARY_PATH,
    non_targets_path: Path = STAGE5A_NON_TARGETS_PATH,
    out_dir: Path = STAGE5B_OUTPUT_DIR,
    summary_out: Path = SUMMARY_PATH,
) -> dict[str, Any]:
    harness = load_records(harness_plan_path)
    fixtures = load_records(parity_fixtures_path)
    backend = load_records(backend_capability_path)
    matrix = load_records(future_kernel_matrix_path)
    targets = load_records(target_plan_path)
    stage5a_summary = read_yaml(stage5a_summary_path)
    non_targets = load_records(non_targets_path)
    ready_targets = [record for record in targets if record.get("target_status") == "ready_for_planning"]
    blocked_targets = [record for record in targets if str(record.get("target_status", "")).startswith("blocked")]
    summary = {
        "record_type": "stage5b_cuda_parity_harness_summary",
        "schema": "schemas/cuda/stage5b-cuda-parity-harness-summary-v0.schema.json",
        "stage_id": "stage-5b",
        "status": "complete",
        "harness_plan_records": len(harness),
        "parity_fixture_records": len(fixtures),
        "backend_capability_records": len(backend),
        "future_kernel_matrix_records": len(matrix),
        "stage5a_targets_loaded": len(targets),
        "ready_targets_loaded": len(ready_targets),
        "blocked_targets_loaded": len(blocked_targets),
        "non_targets_loaded": len(non_targets),
        "ready_for_future_kernel": sum(1 for record in fixtures if record.get("fixture_status") == "ready_for_future_kernel"),
        "blocked_future_kernels": sum(1 for record in matrix if record.get("future_kernel_status") == "blocked"),
        "skipped_non_targets": sum(1 for record in harness if record.get("harness_status") == "skipped_non_target"),
        "stage4o_parity_references_used": int(stage5a_summary.get("stage4o_parity_references_used", 0)),
        "stage4p_unified_result_references_used": int(stage5a_summary.get("stage4p_unified_result_references_used", 0)),
        "local_16gb_profile_recorded": any(record.get("vram_profile") == "local_16gb" for record in backend),
        "local_16gb_profile_required": False,
        "compatibility_8gb_profile_recorded": any(record.get("vram_profile") == "compatibility_8gb" for record in backend),
        "next_stage": "Stage 5C - CUDA build and device-detection scaffold",
        "notes": [
            "Stage 5B creates a CUDA parity harness skeleton only.",
            "No CUDA kernels, GPU benchmarks, performance claims, website expansion, raw-data processing, or solve claims were added.",
            "Local RTX 4060 Ti 16 GB is recorded as optional planning metadata; compatibility 8 GB and CI no-GPU profiles remain represented.",
        ],
        **CUDA_PARITY_POLICY,
    }
    write_yaml(summary_out, summary)
    write_json(out_dir / SUMMARY_REPORT, summary)
    return summary


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)
