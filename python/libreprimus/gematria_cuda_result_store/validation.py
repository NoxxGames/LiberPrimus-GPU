"""Validation for Stage 5P result-store integration records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_cuda_result_store.export import read_record_set
from libreprimus.gematria_cuda_result_store.models import (
    BAD_TRUE_FLAGS,
    CONTROLLED_EXPANSION_CANDIDATE_SCHEMA,
    CONTROLLED_EXPANSION_CANDIDATES_PATH,
    GENERATED_BODY_POLICY_PATH,
    GENERATED_BODY_POLICY_SCHEMA,
    METHOD_STATUS_IMPACT_PATH,
    METHOD_STATUS_IMPACT_SCHEMA,
    OUTPUT_DIR,
    REQUIRED_TRUE_FLAGS,
    RESULT_STORE_INTEGRATION_PATH,
    RESULT_STORE_INTEGRATION_SCHEMA,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_SCHEMA,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)


def validate_stage5p_results(
    *,
    result_store_integration_path: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration_path: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact_path: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy_path: Path = GENERATED_BODY_POLICY_PATH,
    controlled_expansion_candidates_path: Path = CONTROLLED_EXPANSION_CANDIDATES_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    result_store = read_record_set(result_store_integration_path)
    score = read_record_set(score_summary_integration_path)
    impacts = read_record_set(method_status_impact_path)
    policies = read_record_set(generated_body_policy_path)
    candidates = read_record_set(controlled_expansion_candidates_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_REPORT
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(result_store, RESULT_STORE_INTEGRATION_SCHEMA, "result_store_integration"))
    errors.extend(_validate_records(score, SCORE_SUMMARY_INTEGRATION_SCHEMA, "score_summary_integration"))
    errors.extend(_validate_records(impacts, METHOD_STATUS_IMPACT_SCHEMA, "method_status_impact"))
    errors.extend(_validate_records(policies, GENERATED_BODY_POLICY_SCHEMA, "generated_body_policy"))
    errors.extend(_validate_records(candidates, CONTROLLED_EXPANSION_CANDIDATE_SCHEMA, "controlled_expansion"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5P summary does not match generated summary.json")
    errors.extend(_semantic_errors([*result_store, *score, *impacts, *policies, *candidates, summary]))
    if len(result_store) != 5:
        errors.append("Stage 5P result-store integration must represent exactly five Stage 5O parity records")
    if len(score) != len(result_store):
        errors.append("Stage 5P score-summary/result-store count mismatch")
    if summary.get("result_store_integration_records") != len(result_store):
        errors.append("Stage 5P summary result_store_integration_records mismatch")
    if summary.get("score_summary_integration_records") != len(score):
        errors.append("Stage 5P summary score_summary_integration_records mismatch")
    if summary.get("generated_body_publication_allowed") is not False:
        errors.append("Stage 5P summary must keep generated_body_publication_allowed=false")
    if summary.get("method_status_upgrade_allowed") is not False:
        errors.append("Stage 5P summary must keep method_status_upgrade_allowed=false")
    counts = {
        "result_store_integration_records": len(result_store),
        "score_summary_integration_records": len(score),
        "method_status_impact_records": len(impacts),
        "generated_body_policy_records": len(policies),
        "controlled_expansion_candidate_records": len(candidates),
        "stage4p_compatibility": str(summary.get("stage4p_compatibility", False)).lower(),
        "stage4i_compatibility": str(summary.get("stage4i_compatibility", False)).lower(),
        "generated_body_publication_allowed": str(summary.get("generated_body_publication_allowed", True)).lower(),
        "method_status_upgrade_allowed": str(summary.get("method_status_upgrade_allowed", True)).lower(),
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
        if record.get("new_cuda_kernels_added") not in (0, None):
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("stage5p_integration_status") == "integrated_compact_summary":
            if not record.get("output_token_hash"):
                errors.append(f"{ident}: integrated compact summaries require output_token_hash")
            if record.get("generated_body_reference") != "ignored_stage5o_generated_outputs_not_republished":
                errors.append(f"{ident}: generated bodies must not be republished")
        if record.get("confidence_interpretation") not in (None, "triage_only"):
            errors.append(f"{ident}: confidence_interpretation must be triage_only")
        if record.get("policy_status") == "blocked_generated_body_publication":
            if record.get("body_publication_allowed") is not False:
                errors.append(f"{ident}: generated body publication must remain blocked")
    return errors
