"""Validation for Stage 5M solved-fixture CUDA parity records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_solved_fixture_cuda.export import read_record_set
from libreprimus.gematria_solved_fixture_cuda.models import (
    BAD_TRUE_FLAGS,
    BOUNDARY_RECORDS_PATH,
    BOUNDARY_SCHEMA,
    IMPLEMENTED_KERNEL_NAME,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    PARITY_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    RUN_RECORDS_PATH,
    RUN_SCHEMA,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)


def validate_stage5m_results(
    *,
    run_records_path: Path = RUN_RECORDS_PATH,
    parity_records_path: Path = PARITY_RECORDS_PATH,
    boundaries_path: Path = BOUNDARY_RECORDS_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    run_records = read_record_set(run_records_path)
    parity_records = read_record_set(parity_records_path)
    boundary_records = read_record_set(boundaries_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_REPORT
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(run_records, RUN_SCHEMA, "run"))
    errors.extend(_validate_records(parity_records, PARITY_SCHEMA, "parity"))
    errors.extend(_validate_records(boundary_records, BOUNDARY_SCHEMA, "boundary"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5M summary does not match generated summary.json")
    errors.extend(_semantic_errors([*run_records, *parity_records, *boundary_records, summary]))
    if len(run_records) != 5:
        errors.append("Stage 5M must represent exactly five Stage 5L mappings")
    if len(parity_records) != len(run_records):
        errors.append("Stage 5M parity/run record count mismatch")
    pass_count = int(summary.get("parity_pass_count", -1))
    fail_count = int(summary.get("parity_fail_count", -1))
    skip_count = int(summary.get("parity_skip_count", -1))
    if summary.get("stage5n_ready") is True and (pass_count, fail_count, skip_count) != (5, 0, 0):
        errors.append("stage5n_ready=true requires 5 pass, 0 fail, 0 skip")
    counts = {
        "run_records": len(run_records),
        "cuda_attempted_count": summary.get("cuda_attempted_count"),
        "cuda_pass_count": summary.get("cuda_pass_count"),
        "cuda_fail_count": summary.get("cuda_fail_count"),
        "cuda_skip_count": summary.get("cuda_skip_count"),
        "parity_records": len(parity_records),
        "boundary_records": len(boundary_records),
        "stage5n_ready": str(summary.get("stage5n_ready", False)).lower(),
        "selected_next_stage": summary.get("selected_next_stage"),
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
        if record.get("new_cuda_kernels_added") not in (0, None):
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("parity_status") == "passed":
            if record.get("cuda_output_token_hash") != record.get("expected_native_output_token_hash"):
                errors.append(f"{ident}: passed parity requires CUDA hash equal native hash")
            if record.get("cuda_native_hash_match") is not True:
                errors.append(f"{ident}: passed parity requires cuda_native_hash_match=true")
        if str(record.get("parity_status", "")).startswith("skipped") and record.get("cuda_native_hash_match") is True:
            errors.append(f"{ident}: skipped parity cannot claim cuda_native_hash_match=true")
    return errors
