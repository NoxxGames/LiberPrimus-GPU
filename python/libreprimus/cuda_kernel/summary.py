"""Summary generation for Stage 5F synthetic CUDA kernel records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.cuda_kernel.export import read_record_set, write_report, write_warnings
from libreprimus.cuda_kernel.models import (
    BUILD_RECORDS_PATH,
    COMMON_POLICY_FLAGS,
    IMPLEMENTATION_PATH,
    NEXT_STAGE,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    STAGE_ID,
)
from libreprimus.cuda_kernel.synthetic_parity import EXPECTED_NATIVE_HASH


def build_summary(
    *,
    implementation_path: Path = IMPLEMENTATION_PATH,
    build_records_path: Path = BUILD_RECORDS_PATH,
    parity_records_path: Path = PARITY_RECORDS_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    implementation = read_record_set(implementation_path)
    build_records = read_record_set(build_records_path)
    parity_records = read_record_set(parity_records_path)
    build = build_records[0] if build_records else {}
    parity = parity_records[0] if parity_records else {}
    summary: dict[str, Any] = {
        "record_type": "stage5f_synthetic_cuda_kernel_summary",
        "stage_id": STAGE_ID,
        "status": "complete",
        "implementation_records": len(implementation),
        "build_records": len(build_records),
        "parity_records": len(parity_records),
        "selected_kernel_id": COMMON_POLICY_FLAGS["selected_kernel_id"],
        "selected_target_id": COMMON_POLICY_FLAGS["selected_target_id"],
        "selected_transform_family": COMMON_POLICY_FLAGS["selected_transform_family"],
        "selected_adapter_family": COMMON_POLICY_FLAGS["selected_adapter_family"],
        "fixture_id": COMMON_POLICY_FLAGS["fixture_id"],
        "native_reference_hash": EXPECTED_NATIVE_HASH,
        "cuda_kernel_added": True,
        "cuda_source_modified": True,
        "cuda_build_attempted": bool(build.get("cuda_build_attempted", False)),
        "cuda_build_status": str(build.get("build_status", "unknown")),
        "cuda_synthetic_parity_attempted": bool(parity.get("cuda_synthetic_parity_attempted", False)),
        "cuda_synthetic_parity_status": str(parity.get("parity_status", "unknown")),
        "cuda_output_hash": str(parity.get("cuda_output_hash", "")),
        "cuda_native_hash_match": parity.get("cuda_native_hash_match"),
        "next_stage": NEXT_STAGE,
        **COMMON_POLICY_FLAGS,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_REPORT, summary)
    write_warnings(out_dir, [])
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload
