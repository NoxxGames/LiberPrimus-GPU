"""Summary generation for Stage 5G CUDA parity reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.cuda_parity_reporting.export import read_record_set, write_report, write_warnings
from libreprimus.cuda_parity_reporting.models import (
    COMMON_POLICY_FLAGS,
    DEVICE_AUDIT_PATH,
    NEXT_STAGE,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    PREFLIGHT_PATH,
    SUMMARY_JSON,
    SUMMARY_PATH,
    STAGE_ID,
)


def build_summary(
    *,
    parity_report_path: Path = PARITY_REPORT_PATH,
    device_code_audit_path: Path = DEVICE_AUDIT_PATH,
    preflight_path: Path = PREFLIGHT_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    parity_records = read_record_set(parity_report_path)
    audit_records = read_record_set(device_code_audit_path)
    preflight_records = read_record_set(preflight_path)
    parity = parity_records[0] if parity_records else {}
    audit = audit_records[0] if audit_records else {}
    preflight = preflight_records[0] if preflight_records else {}
    summary: dict[str, Any] = {
        "record_type": "stage5g_cuda_parity_reporting_summary",
        "stage_id": STAGE_ID,
        "status": "complete",
        "parity_report_records": len(parity_records),
        "device_code_audit_records": len(audit_records),
        "solved_fixture_preflight_records": len(preflight_records),
        "native_reference_hash": parity.get("native_reference_hash", ""),
        "stage5f_cuda_output_hash": parity.get("stage5f_cuda_output_hash", ""),
        "stage5f_cuda_native_hash_match": bool(parity.get("stage5f_cuda_native_hash_match")),
        "device_code_subset_compliant": bool(audit.get("device_code_subset_compliant")),
        "stl_used_in_cuda_device_path": bool(audit.get("stl_used_in_cuda_device_path")),
        "std_array_used_in_cuda_device_path": bool(audit.get("std_array_used_in_cuda_device_path")),
        "cxx_exceptions_in_cuda_device_path": bool(audit.get("cxx_exceptions_in_cuda_device_path")),
        "dynamic_allocation_in_device_code": bool(audit.get("dynamic_allocation_in_device_code")),
        "cuda_source_modified": bool(audit.get("cuda_source_modified")),
        "new_cuda_kernels_added": int(audit.get("new_cuda_kernels_added", 0)),
        "solved_fixture_cuda_execution_allowed": bool(preflight.get("solved_fixture_cuda_execution_allowed")),
        "production_gematria_mod29_cuda_ready": bool(preflight.get("production_gematria_mod29_cuda_ready")),
        "preflight_blocker_count": int(preflight.get("preflight_blocker_count", 0)),
        "next_stage": NEXT_STAGE,
        **COMMON_POLICY_FLAGS,
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
