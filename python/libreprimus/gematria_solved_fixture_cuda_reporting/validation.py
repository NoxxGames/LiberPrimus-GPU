"""Validation for Stage 5N solved-fixture-safe CUDA reporting records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_solved_fixture_cuda_reporting.export import read_record_set
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    BAD_TRUE_FLAGS,
    BOUNDARY_REVIEW_PATH,
    BOUNDARY_SCHEMA,
    CONTROLLED_EXPANSION_GATE_PATH,
    GATE_SCHEMA,
    NO_UNSOLVED_GUARDRAIL_PATH,
    NO_UNSOLVED_SCHEMA,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    PARITY_SCHEMA,
    RESULT_STORE_PREFLIGHT_PATH,
    RESULT_STORE_SCHEMA,
    SUMMARY_JSON,
    SUMMARY_PATH,
    SUMMARY_SCHEMA,
)


def validate_stage5n_results(
    *,
    parity_report_path: Path = PARITY_REPORT_PATH,
    controlled_expansion_gate_path: Path = CONTROLLED_EXPANSION_GATE_PATH,
    boundary_review_path: Path = BOUNDARY_REVIEW_PATH,
    result_store_preflight_path: Path = RESULT_STORE_PREFLIGHT_PATH,
    no_unsolved_guardrail_path: Path = NO_UNSOLVED_GUARDRAIL_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    parity = read_record_set(parity_report_path)
    gates = read_record_set(controlled_expansion_gate_path)
    boundaries = read_record_set(boundary_review_path)
    preflight = read_record_set(result_store_preflight_path)
    guardrails = read_record_set(no_unsolved_guardrail_path)
    summary = read_yaml(summary_path)
    errors: list[str] = []
    errors.extend(_validate_records(parity, PARITY_SCHEMA, "parity"))
    errors.extend(_validate_records(gates, GATE_SCHEMA, "gate"))
    errors.extend(_validate_records(boundaries, BOUNDARY_SCHEMA, "boundary"))
    errors.extend(_validate_records(preflight, RESULT_STORE_SCHEMA, "result_store_preflight"))
    errors.extend(_validate_records(guardrails, NO_UNSOLVED_SCHEMA, "no_unsolved_guardrail"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    generated_summary = _read_optional_generated_summary(results_dir)
    if generated_summary and generated_summary != summary:
        errors.append("Committed Stage 5N summary does not match generated summary.json")
    errors.extend(_semantic_errors([*parity, *gates, *boundaries, *preflight, *guardrails, summary]))
    if len(parity) != 5:
        errors.append("Stage 5N parity report must carry forward all five Stage 5M parity records")
    if summary.get("parity_pass_count") != 5 or summary.get("parity_fail_count") != 0 or summary.get("parity_skip_count") != 0:
        errors.append("Stage 5N summary must preserve Stage 5M 5/0/0 parity counts")
    if not any(record.get("gate_status") == "blocked_unsolved" for record in gates):
        errors.append("Controlled expansion gate must keep unsolved-page CUDA blocked")
    if not all(record.get("guardrail_status") == "enforced" for record in guardrails):
        errors.append("No-unsolved guardrails must all be enforced")
    counts = {
        "parity_report_records": len(parity),
        "gate_records": len(gates),
        "boundary_review_records": len(boundaries),
        "result_store_preflight_records": len(preflight),
        "no_unsolved_guardrail_records": len(guardrails),
        "selected_next_stage": summary.get("selected_next_stage"),
        "unsolved_page_cuda_allowed": str(summary.get("unsolved_page_cuda_allowed")).lower(),
        "additional_cuda_execution_performed": str(summary.get("additional_cuda_execution_performed")).lower(),
        "new_cuda_kernels_added": summary.get("new_cuda_kernels_added"),
        "cuda_source_modified": str(summary.get("cuda_source_modified")).lower(),
    }
    return counts, errors


def _read_optional_generated_summary(results_dir: Path) -> dict[str, Any] | None:
    path = resolve_repo_path(results_dir) / SUMMARY_JSON
    return read_json(path) if path.is_file() else None


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
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        if record.get("new_cuda_kernels_added") not in (0, None):
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{ident}: no_solve_claim must be true")
        if record.get("parity_status") == "passed" and record.get("native_hash") != record.get("cuda_hash"):
            errors.append(f"{ident}: passed parity requires native_hash equal cuda_hash")
        if record.get("gate_id") == "unsolved_page_cuda_gate" and record.get("gate_status") != "blocked_unsolved":
            errors.append(f"{ident}: unsolved_page_cuda_gate must be blocked_unsolved")
        if record.get("preflight_kind") in {"result_store", "score_summary"}:
            if record.get("stage4p_compatibility_required") is not True:
                errors.append(f"{ident}: Stage 4P compatibility must be required")
            if record.get("confidence_label_interpretation") != "triage_only":
                errors.append(f"{ident}: confidence labels must remain triage_only")
        if record.get("guardrail_id") == "canonical_corpus_inactive":
            if record.get("canonical_corpus_active") is not False:
                errors.append(f"{ident}: canonical corpus must remain inactive")
        if record.get("guardrail_id") == "page_boundaries_reviewable":
            if record.get("page_boundaries_final") is not False:
                errors.append(f"{ident}: page boundaries must remain reviewable")
    return errors
