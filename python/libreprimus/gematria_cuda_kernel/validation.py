"""Validation for Stage 5J Gematria CUDA kernel records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_cuda_kernel.export import read_record_set
from libreprimus.gematria_cuda_kernel.models import (
    BAD_TRUE_FLAGS,
    BUILD_RECORDS_PATH,
    BUILD_SCHEMA,
    IMPLEMENTATION_PATH,
    IMPLEMENTATION_SCHEMA,
    IMPLEMENTED_KERNEL_NAME,
    NATIVE_FIXTURE_HASH,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    PARITY_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    SOURCE_CONTRACT_ID,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)


def validate_stage5j_results(
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
        errors.append("Committed Stage 5J summary does not match generated summary.json")
    errors.extend(_semantic_errors([*implementation, *build_records, *parity_records, summary]))
    build = build_records[0] if build_records else {}
    parity = parity_records[0] if parity_records else {}
    counts = {
        "implementation_records": len(implementation),
        "build_records": len(build_records),
        "parity_records": len(parity_records),
        "implemented_kernel_name": summary.get("implemented_kernel_name"),
        "source_contract_id": summary.get("source_contract_id"),
        "native_fixture_hash": summary.get("native_fixture_hash"),
        "cuda_build_attempted": str(build.get("cuda_build_attempted", False)).lower(),
        "cuda_build_status": build.get("build_status"),
        "cuda_synthetic_parity_attempted": str(parity.get("cuda_synthetic_parity_attempted", False)).lower(),
        "cuda_synthetic_parity_status": parity.get("parity_status"),
        "cuda_output_hash": parity.get("cuda_output_hash", ""),
        "cuda_native_hash_match": str(parity.get("cuda_native_hash_match", "unknown")).lower(),
        "gematria_cuda_synthetic_parity_verified": str(summary.get("gematria_cuda_synthetic_parity_verified", False)).lower(),
        "stage5k_ready": str(summary.get("stage5k_ready", False)).lower(),
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
        if record.get("implemented_kernel_name") != IMPLEMENTED_KERNEL_NAME:
            errors.append(f"{ident}: implemented_kernel_name must be {IMPLEMENTED_KERNEL_NAME}")
        if record.get("source_contract_id") != SOURCE_CONTRACT_ID:
            errors.append(f"{ident}: source_contract_id mismatch")
        if record.get("native_fixture_hash") != NATIVE_FIXTURE_HASH:
            errors.append(f"{ident}: native_fixture_hash mismatch")
        if record.get("new_cuda_kernels_added") != 1:
            errors.append(f"{ident}: new_cuda_kernels_added must be 1")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("parity_status") == "passed":
            if record.get("cuda_output_hash") != NATIVE_FIXTURE_HASH:
                errors.append(f"{ident}: passed parity requires native fixture hash")
            if record.get("cuda_native_hash_match") is not True:
                errors.append(f"{ident}: passed parity requires cuda_native_hash_match=true")
            if record.get("gematria_cuda_synthetic_parity_verified") is not True:
                errors.append(f"{ident}: passed parity requires verification true")
        if record.get("build_status") in {"skipped_not_requested", "skipped_missing_cuda", "failed_missing_cuda", "failed_environment", "failed_toolkit_resolution", "failed"}:
            if record.get("gematria_cuda_synthetic_parity_verified") is True:
                errors.append(f"{ident}: skipped/failed build cannot verify parity")
    return errors
