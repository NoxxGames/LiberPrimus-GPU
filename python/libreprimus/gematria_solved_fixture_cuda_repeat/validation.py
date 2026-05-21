"""Validation for Stage 5O repeat-verification records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set
from libreprimus.gematria_solved_fixture_cuda_repeat.models import (
    BAD_TRUE_FLAGS,
    EXPANSION_DECISION_PATH,
    EXPANSION_DECISION_SCHEMA,
    IMPLEMENTED_KERNEL_NAME,
    OUTPUT_DIR,
    REPEAT_PARITY_PATH,
    REPEAT_PARITY_SCHEMA,
    REPEAT_RUN_PATH,
    REPEAT_RUN_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    RESULT_STORE_PREFLIGHT_PATH,
    RESULT_STORE_SCHEMA,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    SCORE_SUMMARY_SCHEMA,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)


def validate_stage5o_results(
    *,
    repeat_run_path: Path = REPEAT_RUN_PATH,
    repeat_parity_path: Path = REPEAT_PARITY_PATH,
    result_store_preflight_path: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight_path: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    expansion_decision_path: Path = EXPANSION_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    runs = read_record_set(repeat_run_path)
    parity = read_record_set(repeat_parity_path)
    result_store = read_record_set(result_store_preflight_path)
    score = read_record_set(score_summary_preflight_path)
    decisions = read_record_set(expansion_decision_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_REPORT
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(runs, REPEAT_RUN_SCHEMA, "repeat_run"))
    errors.extend(_validate_records(parity, REPEAT_PARITY_SCHEMA, "repeat_parity"))
    errors.extend(_validate_records(result_store, RESULT_STORE_SCHEMA, "result_store"))
    errors.extend(_validate_records(score, SCORE_SUMMARY_SCHEMA, "score_summary"))
    errors.extend(_validate_records(decisions, EXPANSION_DECISION_SCHEMA, "expansion_decision"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5O summary does not match generated summary.json")
    errors.extend(_semantic_errors([*runs, *parity, *result_store, *score, *decisions, summary]))
    if len(runs) != 5:
        errors.append("Stage 5O must represent exactly five Stage 5M repeat records")
    if len(parity) != len(runs):
        errors.append("Stage 5O repeat parity/run record count mismatch")
    pass_count = int(summary.get("repeat_parity_pass_count", -1))
    fail_count = int(summary.get("repeat_parity_fail_count", -1))
    skip_count = int(summary.get("repeat_parity_skip_count", -1))
    if summary.get("stage5p_ready") is True and (pass_count, fail_count, skip_count) != (5, 0, 0):
        errors.append("stage5p_ready=true requires 5 pass, 0 fail, 0 skip")
    counts = {
        "repeat_run_records": len(runs),
        "repeat_cuda_attempted_count": summary.get("repeat_cuda_attempted_count"),
        "repeat_cuda_pass_count": summary.get("repeat_cuda_pass_count"),
        "repeat_cuda_fail_count": summary.get("repeat_cuda_fail_count"),
        "repeat_cuda_skip_count": summary.get("repeat_cuda_skip_count"),
        "repeat_parity_records": len(parity),
        "result_store_preflight_records": len(result_store),
        "score_summary_preflight_records": len(score),
        "expansion_decision_records": len(decisions),
        "stage5p_ready": str(summary.get("stage5p_ready", False)).lower(),
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
        if record.get("repeat_parity_status") == "passed":
            if record.get("stage5o_repeat_cuda_output_token_hash") != record.get("expected_native_output_token_hash"):
                errors.append(f"{ident}: passed parity requires repeat hash equal Stage 5L native hash")
            if record.get("stage5o_repeat_cuda_output_token_hash") != record.get("stage5m_cuda_output_token_hash"):
                errors.append(f"{ident}: passed parity requires repeat hash equal Stage 5M CUDA hash")
            if record.get("stage5l_native_hash_match") is not True or record.get("stage5m_cuda_hash_match") is not True:
                errors.append(f"{ident}: passed parity requires both hash-match booleans true")
        if record.get("decision_status") == "stage5p_ready" and record.get("stage5p_ready") is not True:
            errors.append(f"{ident}: stage5p_ready decision must set stage5p_ready=true")
    return errors
