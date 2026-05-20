"""Validation for Stage 5F synthetic CUDA kernel records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.cuda_kernel.export import read_record_set
from libreprimus.cuda_kernel.models import (
    BAD_TRUE_FLAGS,
    BUILD_RECORDS_PATH,
    BUILD_SCHEMA,
    IMPLEMENTATION_PATH,
    IMPLEMENTATION_SCHEMA,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    PARITY_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)
from libreprimus.cuda_kernel.synthetic_parity import EXPECTED_NATIVE_HASH


def validate_stage5f_results(
    *,
    implementation_path: Path = IMPLEMENTATION_PATH,
    build_records_path: Path = BUILD_RECORDS_PATH,
    parity_records_path: Path = PARITY_RECORDS_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    implementation = read_record_set(implementation_path)
    build_records = read_record_set(build_records_path)
    parity_records = read_record_set(parity_records_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_REPORT
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(implementation, IMPLEMENTATION_SCHEMA, "implementation"))
    errors.extend(_validate_records(build_records, BUILD_SCHEMA, "build"))
    errors.extend(_validate_records(parity_records, PARITY_SCHEMA, "parity"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5F summary does not match generated summary.json")
    errors.extend(_semantic_errors([*implementation, *build_records, *parity_records, summary]))
    parity = parity_records[0] if parity_records else {}
    counts = {
        "implementation_records": len(implementation),
        "build_records": len(build_records),
        "parity_records": len(parity_records),
        "selected_kernel_id": summary.get("selected_kernel_id"),
        "selected_target_id": summary.get("selected_target_id"),
        "selected_adapter_family": summary.get("selected_adapter_family"),
        "native_reference_hash": summary.get("native_reference_hash"),
        "cuda_kernel_added": str(summary.get("cuda_kernel_added")).lower(),
        "cuda_source_modified": str(summary.get("cuda_source_modified")).lower(),
        "cuda_build_attempted": str(summary.get("cuda_build_attempted")).lower(),
        "cuda_build_status": summary.get("cuda_build_status"),
        "cuda_synthetic_parity_attempted": str(summary.get("cuda_synthetic_parity_attempted")).lower(),
        "cuda_synthetic_parity_status": summary.get("cuda_synthetic_parity_status"),
        "cuda_output_hash": parity.get("cuda_output_hash", ""),
        "cuda_native_hash_match": str(parity.get("cuda_native_hash_match", "unknown")).lower(),
        "no_gpu_ci_safe": str(summary.get("no_gpu_ci_safe")).lower(),
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
        if record.get("native_reference_hash") != EXPECTED_NATIVE_HASH:
            errors.append(f"{ident}: native_reference_hash mismatch")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("cuda_kernel_added") is not True:
            errors.append(f"{ident}: cuda_kernel_added must be true")
        if record.get("cuda_source_modified") is not True:
            errors.append(f"{ident}: cuda_source_modified must be true")
    return errors
