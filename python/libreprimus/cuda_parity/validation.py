"""Validation for Stage 5B CUDA parity harness records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.cuda_parity.loaders import load_records
from libreprimus.cuda_parity.models import (
    BACKEND_CAPABILITY_PATH,
    BACKEND_SCHEMA,
    BAD_TRUE_FLAGS,
    FIXTURE_SCHEMA,
    FUTURE_KERNEL_MATRIX_PATH,
    HARNESS_PLAN_PATH,
    HARNESS_SCHEMA,
    MATRIX_SCHEMA,
    PARITY_FIXTURES_PATH,
    STAGE5B_OUTPUT_DIR,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)


def validate_stage5b_results(
    *,
    harness_plan_path: Path = HARNESS_PLAN_PATH,
    parity_fixtures_path: Path = PARITY_FIXTURES_PATH,
    backend_capability_path: Path = BACKEND_CAPABILITY_PATH,
    future_kernel_matrix_path: Path = FUTURE_KERNEL_MATRIX_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = STAGE5B_OUTPUT_DIR,
) -> tuple[dict[str, int], list[str]]:
    harness = load_records(harness_plan_path)
    fixtures = load_records(parity_fixtures_path)
    backend = load_records(backend_capability_path)
    matrix = load_records(future_kernel_matrix_path)
    summary = read_yaml(summary_path)
    generated_summary = read_json(resolve_repo_path(results_dir) / SUMMARY_REPORT)
    errors: list[str] = []
    errors.extend(_validate_records(harness, HARNESS_SCHEMA, "harness"))
    errors.extend(_validate_records(fixtures, FIXTURE_SCHEMA, "fixtures"))
    errors.extend(_validate_records(backend, BACKEND_SCHEMA, "backend"))
    errors.extend(_validate_records(matrix, MATRIX_SCHEMA, "matrix"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5B summary does not match generated summary.json")
    errors.extend(_policy_errors([*harness, *fixtures, *backend, *matrix, summary]))
    errors.extend(_semantic_errors(harness, fixtures, backend, matrix, summary))
    counts = {
        "harness_plan_records": len(harness),
        "parity_fixture_records": len(fixtures),
        "backend_capability_records": len(backend),
        "future_kernel_matrix_records": len(matrix),
        "ready_targets_loaded": int(summary.get("ready_targets_loaded", 0)),
        "blocked_targets_loaded": int(summary.get("blocked_targets_loaded", 0)),
        "non_targets_loaded": int(summary.get("non_targets_loaded", 0)),
        "ready_for_future_kernel": int(summary.get("ready_for_future_kernel", 0)),
        "blocked_future_kernels": int(summary.get("blocked_future_kernels", 0)),
        "skipped_non_targets": int(summary.get("skipped_non_targets", 0)),
        "stage4o_parity_references_used": int(summary.get("stage4o_parity_references_used", 0)),
        "stage4p_unified_result_references_used": int(summary.get("stage4p_unified_result_references_used", 0)),
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


def _policy_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        ident = str(record.get("harness_id") or record.get("fixture_id") or record.get("backend_id") or record.get("kernel_id") or record.get("record_type"))
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{ident}: no_solve_claim must be true")
    return errors


def _semantic_errors(
    harness: list[dict[str, Any]],
    fixtures: list[dict[str, Any]],
    backend: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    summary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    fixture_targets = {record.get("stage5a_target_id") for record in fixtures}
    harness_targets = {record.get("stage5a_target_id") for record in harness}
    if fixture_targets != harness_targets:
        errors.append("Harness and fixture target sets differ")
    ready_harness = {record.get("stage5a_target_id") for record in harness if record.get("harness_status") == "ready_for_future_kernel"}
    ready_fixtures = {record.get("stage5a_target_id") for record in fixtures if record.get("fixture_status") == "ready_for_future_kernel"}
    if ready_harness != ready_fixtures:
        errors.append("Ready harness and fixture target sets differ")
    profiles = {record.get("vram_profile") for record in backend}
    if "local_16gb" not in profiles:
        errors.append("Missing local_16gb backend capability profile")
    if "compatibility_8gb" not in profiles:
        errors.append("Missing compatibility_8gb backend capability profile")
    if "ci_no_gpu" not in profiles:
        errors.append("Missing ci_no_gpu backend capability profile")
    for record in backend:
        if record.get("local_16gb_profile_required") is not False:
            errors.append(f"{record.get('backend_id')}: local_16gb_profile_required must be false")
    if summary.get("harness_plan_records") != len(harness):
        errors.append("harness plan count mismatch")
    if summary.get("parity_fixture_records") != len(fixtures):
        errors.append("parity fixture count mismatch")
    if summary.get("backend_capability_records") != len(backend):
        errors.append("backend capability count mismatch")
    if summary.get("future_kernel_matrix_records") != len(matrix):
        errors.append("future kernel matrix count mismatch")
    return errors
