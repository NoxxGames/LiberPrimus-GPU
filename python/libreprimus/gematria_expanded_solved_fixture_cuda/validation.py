"""Validation for Stage 5R expanded solved-fixture CUDA parity records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set
from libreprimus.gematria_expanded_solved_fixture_cuda.models import (
    BAD_TRUE_FLAGS,
    BOUNDARY_RECORDS_PATH,
    BOUNDARY_SCHEMA,
    EXPECTED_FIXTURE_IDS,
    IMPLEMENTED_KERNEL_NAME,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    PARITY_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    RESULT_STORE_PREFLIGHT_PATH,
    RESULT_STORE_PREFLIGHT_SCHEMA,
    RUN_RECORDS_PATH,
    RUN_SCHEMA,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_SCHEMA,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)


def validate_stage5r_results(
    *,
    run_records_path: Path = RUN_RECORDS_PATH,
    parity_records_path: Path = PARITY_RECORDS_PATH,
    boundaries_path: Path = BOUNDARY_RECORDS_PATH,
    result_store_preflight_path: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight_path: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    runs = read_record_set(run_records_path)
    parity = read_record_set(parity_records_path)
    boundaries = read_record_set(boundaries_path)
    result_store = read_record_set(result_store_preflight_path)
    score = read_record_set(score_summary_preflight_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_REPORT
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(runs, RUN_SCHEMA, "run"))
    errors.extend(_validate_records(parity, PARITY_SCHEMA, "parity"))
    errors.extend(_validate_records(boundaries, BOUNDARY_SCHEMA, "boundary"))
    errors.extend(_validate_records(result_store, RESULT_STORE_PREFLIGHT_SCHEMA, "result_store"))
    errors.extend(_validate_records(score, SCORE_SUMMARY_PREFLIGHT_SCHEMA, "score_summary"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5R summary does not match generated summary.json")
    errors.extend(_semantic_errors([*runs, *parity, *boundaries, *result_store, *score, summary]))
    fixture_ids = sorted(str(record["fixture_id"]) for record in runs)
    if fixture_ids != sorted(EXPECTED_FIXTURE_IDS):
        errors.append(f"Stage 5R must represent exactly {EXPECTED_FIXTURE_IDS}; got {fixture_ids}")
    if len(runs) != 3:
        errors.append("Stage 5R must contain exactly three run records")
    if len(parity) != len(runs):
        errors.append("Stage 5R parity/run record count mismatch")
    pass_count = int(summary.get("parity_pass_count", -1))
    fail_count = int(summary.get("parity_fail_count", -1))
    skip_count = int(summary.get("parity_skip_count", -1))
    if summary.get("stage5s_ready") is True and (pass_count, fail_count, skip_count) != (3, 0, 0):
        errors.append("stage5s_ready=true requires 3 pass, 0 fail, 0 skip")
    counts = {
        "run_records": len(runs),
        "cuda_attempted_count": summary.get("cuda_attempted_count"),
        "cuda_pass_count": summary.get("cuda_pass_count"),
        "cuda_fail_count": summary.get("cuda_fail_count"),
        "cuda_skip_count": summary.get("cuda_skip_count"),
        "parity_records": len(parity),
        "parity_pass_count": summary.get("parity_pass_count"),
        "parity_fail_count": summary.get("parity_fail_count"),
        "parity_skip_count": summary.get("parity_skip_count"),
        "result_store_preflight_records": len(result_store),
        "score_summary_preflight_records": len(score),
        "stage5s_ready": str(summary.get("stage5s_ready", False)).lower(),
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
        if record.get("implemented_kernel_name") not in (IMPLEMENTED_KERNEL_NAME, None):
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
            if record.get("stage5r_cuda_output_token_hash") != record.get("stage5q_native_output_token_hash"):
                errors.append(f"{ident}: passed parity requires Stage 5R CUDA hash equal Stage 5Q native hash")
            if record.get("cuda_native_hash_match") is not True:
                errors.append(f"{ident}: passed parity requires cuda_native_hash_match=true")
        if record.get("cuda_run_status") == "passed" and record.get("cuda_run_attempted") is not True:
            errors.append(f"{ident}: passed CUDA run requires cuda_run_attempted=true")
        if record.get("score_interpretation") not in (None, "triage_only"):
            errors.append(f"{ident}: score_interpretation must be triage_only")
    return errors
