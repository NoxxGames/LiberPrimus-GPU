"""Validation for Stage 5K Gematria CUDA parity reporting records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_cuda_parity_reporting.export import read_record_set
from libreprimus.gematria_cuda_parity_reporting.models import (
    BAD_TRUE_FLAGS,
    DEVICE_AUDIT_PATH,
    DEVICE_AUDIT_SCHEMA,
    IMPLEMENTED_KERNEL_NAME,
    NATIVE_FIXTURE_HASH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    PARITY_SCHEMA,
    PREFLIGHT_PATH,
    PREFLIGHT_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    SCORE_PREFLIGHT_PATH,
    SCORE_PREFLIGHT_SCHEMA,
    SOURCE_CONTRACT_ID,
    SUMMARY_JSON,
    SUMMARY_PATH,
    SUMMARY_SCHEMA,
)


def validate_stage5k_results(
    *,
    parity_report_path: Path = PARITY_REPORT_PATH,
    device_code_audit_path: Path = DEVICE_AUDIT_PATH,
    preflight_path: Path = PREFLIGHT_PATH,
    score_preflight_path: Path = SCORE_PREFLIGHT_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    parity_records = read_record_set(parity_report_path)
    audit_records = read_record_set(device_code_audit_path)
    preflight_records = read_record_set(preflight_path)
    score_preflight_records = read_record_set(score_preflight_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_JSON
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(parity_records, PARITY_SCHEMA, "parity_report"))
    errors.extend(_validate_records(audit_records, DEVICE_AUDIT_SCHEMA, "device_code_audit"))
    errors.extend(_validate_records(preflight_records, PREFLIGHT_SCHEMA, "preflight"))
    errors.extend(_validate_records(score_preflight_records, SCORE_PREFLIGHT_SCHEMA, "score_preflight"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5K summary does not match generated summary.json")
    records = [*parity_records, *audit_records, *preflight_records, *score_preflight_records, summary]
    errors.extend(_semantic_errors(records))
    counts = {
        "parity_report_records": len(parity_records),
        "device_code_audit_records": len(audit_records),
        "solved_fixture_safe_preflight_records": len(preflight_records),
        "score_summary_preflight_records": len(score_preflight_records),
        "implemented_kernel_name": summary.get("implemented_kernel_name"),
        "native_fixture_hash": summary.get("native_fixture_hash"),
        "cuda_output_hash": summary.get("cuda_output_hash"),
        "cuda_native_hash_match": str(summary.get("cuda_native_hash_match")).lower(),
        "gematria_cuda_synthetic_parity_verified": str(
            summary.get("gematria_cuda_synthetic_parity_verified")
        ).lower(),
        "device_code_subset_compliant": str(summary.get("device_code_subset_compliant")).lower(),
        "new_cuda_kernels_added": int(summary.get("new_cuda_kernels_added", -1)),
        "cuda_source_modified": str(summary.get("cuda_source_modified")).lower(),
        "cuda_execution_performed": str(summary.get("cuda_execution_performed")).lower(),
        "blocker_count": int(summary.get("blocker_count", -1)),
        "readiness_status_counts": summary.get("readiness_status_counts", {}),
        "recommended_next_prompt": summary.get("recommended_next_prompt"),
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
            errors.append(f"{ident}: source_contract_id must be {SOURCE_CONTRACT_ID}")
        if record.get("native_fixture_hash") != NATIVE_FIXTURE_HASH:
            errors.append(f"{ident}: native_fixture_hash mismatch")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("new_cuda_kernels_added") not in {0, None}:
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
        if record.get("cuda_output_hash") not in {NATIVE_FIXTURE_HASH, None}:
            errors.append(f"{ident}: CUDA output hash must match the Stage 5H native fixture hash")
        if record.get("cuda_native_hash_match") is False:
            errors.append(f"{ident}: CUDA/native hash match must not be false")
        if record.get("gematria_cuda_synthetic_parity_verified") is False:
            errors.append(f"{ident}: synthetic parity verified must not be false")
        if record.get("device_code_subset_compliant") is False:
            errors.append(f"{ident}: device-code subset audit must be compliant")
        if record.get("banned_token_finding_count") not in {0, None}:
            errors.append(f"{ident}: device-code audit must have zero banned-token findings")
        if record.get("readiness_status") == "ready_for_future_solved_fixture_safe_cuda_stage":
            errors.append(f"{ident}: Stage 5K must not mark solved-fixture CUDA preflight ready")
        if record.get("score_interpretation") not in {"triage_only", None}:
            errors.append(f"{ident}: score interpretation must remain triage_only")
    return errors
