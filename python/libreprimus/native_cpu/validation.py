"""Validation for Stage 5D native CPU records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.native_cpu.export import read_json, read_yaml
from libreprimus.native_cpu.models import (
    BAD_TRUE_FLAGS,
    CAPABILITIES_PATH,
    CAPABILITY_SCHEMA,
    DIAGNOSTICS_PATH,
    DIAGNOSTIC_SCHEMA,
    OUTPUT_DIR,
    PARITY_PATH,
    PARITY_SCHEMA,
    SUMMARY_JSON,
    SUMMARY_PATH,
    SUMMARY_SCHEMA,
    THREADING_PATH,
    THREADING_SCHEMA,
)


def validate_stage5d_results(
    *,
    capabilities_path: Path = CAPABILITIES_PATH,
    threading_path: Path = THREADING_PATH,
    parity_path: Path = PARITY_PATH,
    diagnostics_path: Path = DIAGNOSTICS_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, int | str | bool | list[int]], list[str]]:
    capabilities = _records(capabilities_path)
    threading = _records(threading_path)
    parity = _records(parity_path)
    diagnostics = _records(diagnostics_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_JSON
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else None
    errors: list[str] = []
    errors.extend(_validate_records(capabilities, CAPABILITY_SCHEMA, "capabilities"))
    errors.extend(_validate_records(threading, THREADING_SCHEMA, "threading"))
    errors.extend(_validate_records(parity, PARITY_SCHEMA, "parity"))
    errors.extend(_validate_records(diagnostics, DIAGNOSTIC_SCHEMA, "diagnostics"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    if generated_summary is not None:
        errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary is not None and summary != generated_summary:
        errors.append("Committed Stage 5D summary does not match generated summary.json")
    errors.extend(_policy_errors([*capabilities, *threading, *parity, *diagnostics, summary]))
    errors.extend(_semantic_errors(capabilities, threading, parity, diagnostics, summary))
    counts: dict[str, int | str | bool | list[int]] = {
        "backend_capability_records": len(capabilities),
        "threading_records": len(threading),
        "parity_records": len(parity),
        "diagnostic_records": len(diagnostics),
        "thread_counts_tested": [int(record["thread_count"]) for record in threading],
        "one_thread_hash": str(summary.get("one_thread_hash", "")),
        "multi_thread_hash": str(summary.get("multi_thread_hash", "")),
        "one_thread_equals_multi_thread": bool(summary.get("one_thread_equals_multi_thread", False)),
        "python_native_parity": bool(summary.get("python_native_parity", False)),
        "native_backend_built": bool(summary.get("native_backend_built", False)),
        "native_backend_executable": str(summary.get("native_backend_executable", "")),
    }
    return counts, errors


def _records(path: Path) -> list[dict[str, Any]]:
    return list(read_yaml(path).get("records", []))


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
        ident = str(
            record.get("backend_id")
            or record.get("threading_record_id")
            or record.get("parity_record_id")
            or record.get("diagnostic_record_id")
            or record.get("record_type")
        )
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        if record.get("native_cpu_only") is not True:
            errors.append(f"{ident}: native_cpu_only must be true")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{ident}: no_solve_claim must be true")
        if record.get("python_semantic_reference_preserved") is not True:
            errors.append(f"{ident}: python_semantic_reference_preserved must be true")
    return errors


def _semantic_errors(
    capabilities: list[dict[str, Any]],
    threading: list[dict[str, Any]],
    parity: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    summary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if len(capabilities) < 1:
        errors.append("Missing native CPU capability records")
    if len(threading) < 2:
        errors.append("Expected at least two threading records")
    tested = {int(record.get("thread_count", 0)) for record in threading}
    if not {1, 2}.issubset(tested):
        errors.append("Threading records must include at least 1 and 2 threads")
    if any(record.get("matches_baseline") is not True for record in threading):
        errors.append("All threading records must match the 1-thread baseline")
    if len(parity) < 1 or any(record.get("parity_passed") is not True for record in parity):
        errors.append("Native/Python parity must pass for the limited synthetic fixture")
    if len(diagnostics) < 1:
        errors.append("Missing native CPU diagnostic record")
    if summary.get("backend_capability_records") != len(capabilities):
        errors.append("backend capability count mismatch")
    if summary.get("threading_records") != len(threading):
        errors.append("threading count mismatch")
    if summary.get("parity_records") != len(parity):
        errors.append("parity count mismatch")
    if summary.get("diagnostic_records") != len(diagnostics):
        errors.append("diagnostic count mismatch")
    if summary.get("one_thread_equals_multi_thread") is not True:
        errors.append("summary one_thread_equals_multi_thread must be true")
    if summary.get("python_native_parity") is not True:
        errors.append("summary python_native_parity must be true")
    return errors
