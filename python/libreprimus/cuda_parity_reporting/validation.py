"""Validation for Stage 5G CUDA parity reporting records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.cuda_parity_reporting.export import read_record_set
from libreprimus.cuda_parity_reporting.models import (
    BAD_TRUE_FLAGS,
    DEVICE_AUDIT_PATH,
    DEVICE_AUDIT_SCHEMA,
    NATIVE_REFERENCE_HASH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    PARITY_SCHEMA,
    PREFLIGHT_PATH,
    PREFLIGHT_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    SUMMARY_JSON,
    SUMMARY_PATH,
    SUMMARY_SCHEMA,
)


def validate_stage5g_results(
    *,
    parity_report_path: Path = PARITY_REPORT_PATH,
    device_code_audit_path: Path = DEVICE_AUDIT_PATH,
    preflight_path: Path = PREFLIGHT_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    parity_records = read_record_set(parity_report_path)
    audit_records = read_record_set(device_code_audit_path)
    preflight_records = read_record_set(preflight_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_JSON
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(parity_records, PARITY_SCHEMA, "parity_report"))
    errors.extend(_validate_records(audit_records, DEVICE_AUDIT_SCHEMA, "device_code_audit"))
    errors.extend(_validate_records(preflight_records, PREFLIGHT_SCHEMA, "preflight"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5G summary does not match generated summary.json")
    records = [*parity_records, *audit_records, *preflight_records, summary]
    errors.extend(_semantic_errors(records))
    audit = audit_records[0] if audit_records else {}
    preflight = preflight_records[0] if preflight_records else {}
    counts = {
        "parity_report_records": len(parity_records),
        "device_code_audit_records": len(audit_records),
        "solved_fixture_preflight_records": len(preflight_records),
        "selected_kernel_id": summary.get("selected_kernel_id"),
        "native_reference_hash": summary.get("native_reference_hash"),
        "stage5f_cuda_output_hash": summary.get("stage5f_cuda_output_hash"),
        "stage5f_cuda_native_hash_match": str(summary.get("stage5f_cuda_native_hash_match")).lower(),
        "device_code_subset_compliant": str(summary.get("device_code_subset_compliant")).lower(),
        "stl_used_in_cuda_device_path": str(audit.get("stl_used_in_cuda_device_path")).lower(),
        "std_array_used_in_cuda_device_path": str(audit.get("std_array_used_in_cuda_device_path")).lower(),
        "cxx_exceptions_in_cuda_device_path": str(audit.get("cxx_exceptions_in_cuda_device_path")).lower(),
        "cuda_source_modified": str(summary.get("cuda_source_modified")).lower(),
        "new_cuda_kernels_added": int(summary.get("new_cuda_kernels_added", -1)),
        "solved_fixture_cuda_execution_allowed": str(preflight.get("solved_fixture_cuda_execution_allowed")).lower(),
        "production_gematria_mod29_cuda_ready": str(preflight.get("production_gematria_mod29_cuda_ready")).lower(),
        "gpu_benchmark_performed": int(bool(summary.get("gpu_benchmark_performed"))),
        "performance_or_speedup_claim": int(bool(summary.get("performance_claim") or summary.get("speedup_claim"))),
    }
    return counts, errors


def _validate_records(records: list[dict[str, Any]], schema_path: Path, label: str) -> list[str]:
    errors: list[str] = []
    for index, record in enumerate(records):
        errors.extend(_validate_one(record, schema_path, f"{label}[{index}]"))
    return errors


def _validate_one(record: dict[str, Any], schema_path: Path, label: str) -> list[str]:
    schema = json.loads(resolve_repo_path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [
        f"{label}.{'.'.join(str(part) for part in error.path)}: {error.message}"
        if error.path
        else f"{label}: {error.message}"
        for error in validator.iter_errors(record)
    ]


def _semantic_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        ident = str(record.get("record_type", "record"))
        if record.get("selected_kernel_id") != "shift_score_kernel":
            errors.append(f"{ident}: selected_kernel_id must be shift_score_kernel")
        if record.get("selected_transform_family") != "caesar_mod29":
            errors.append(f"{ident}: selected_transform_family must be caesar_mod29")
        if record.get("selected_adapter_family") != "native_cpu_synthetic_shift_adapter":
            errors.append(f"{ident}: selected_adapter_family mismatch")
        if record.get("native_reference_hash") not in {NATIVE_REFERENCE_HASH, None}:
            errors.append(f"{ident}: native_reference_hash mismatch")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("stage5f_cuda_output_hash") not in {NATIVE_REFERENCE_HASH, None}:
            errors.append(f"{ident}: Stage 5F CUDA output hash must match native reference hash")
        if record.get("stage5f_cuda_native_hash_match") is False:
            errors.append(f"{ident}: Stage 5F CUDA/native hash match must not be false")
        if record.get("device_code_subset_compliant") is False:
            errors.append(f"{ident}: device-code subset audit must be compliant")
        if record.get("stl_used_in_cuda_device_path") is True:
            errors.append(f"{ident}: STL must not appear in CUDA device path")
        if record.get("std_array_used_in_cuda_device_path") is True:
            errors.append(f"{ident}: std::array must not appear in CUDA device path")
        if record.get("cxx_exceptions_in_cuda_device_path") is True:
            errors.append(f"{ident}: exceptions must not appear in CUDA device path")
        if record.get("new_cuda_kernels_added") not in {0, None}:
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
        if record.get("solved_fixture_cuda_execution_allowed") is True:
            errors.append(f"{ident}: solved-fixture CUDA execution must remain blocked")
        if record.get("production_gematria_mod29_cuda_ready") is True:
            errors.append(f"{ident}: production Gematria mod-29 CUDA must remain not ready")
    return errors
