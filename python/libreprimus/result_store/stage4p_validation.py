"""Validation for Stage 4P generated records and committed summary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.result_store.stage4p_export import read_json, read_jsonl, read_yaml, resolve_repo_path
from libreprimus.result_store.unified_models import (
    CROSS_STAGE_REPORT_JSON,
    CROSS_STAGE_REPORT_SCHEMA,
    METHOD_STATUS_JOIN_JSON,
    METHOD_STATUS_JOIN_SCHEMA,
    SOURCE_INVENTORY_JSON,
    SOURCE_INVENTORY_SCHEMA,
    SUMMARY_JSON,
    UNIFICATION_SUMMARY_SCHEMA,
    UNIFIED_RESULT_JSONL,
    UNIFIED_RESULT_SCHEMA,
    UNIFIED_SCORE_JSONL,
    UNIFIED_SCORE_SCHEMA,
)


def validate_stage4p_results(results_dir: Path, summary_path: Path) -> tuple[dict[str, int], list[str]]:
    """Validate Stage 4P generated outputs plus committed summary."""

    resolved = resolve_repo_path(results_dir)
    errors: list[str] = []
    inventory = list(read_json(resolved / SOURCE_INVENTORY_JSON).get("records", []))
    results = read_jsonl(resolved / UNIFIED_RESULT_JSONL)
    scores = read_jsonl(resolved / UNIFIED_SCORE_JSONL)
    joins = list(read_json(resolved / METHOD_STATUS_JOIN_JSON).get("records", []))
    report = read_json(resolved / CROSS_STAGE_REPORT_JSON)
    generated_summary = read_json(resolved / SUMMARY_JSON)
    committed_summary = read_yaml(summary_path)

    errors.extend(_validate_records(inventory, SOURCE_INVENTORY_SCHEMA, "source_inventory"))
    errors.extend(_validate_records(results, UNIFIED_RESULT_SCHEMA, "unified_result"))
    errors.extend(_validate_records(scores, UNIFIED_SCORE_SCHEMA, "unified_score"))
    errors.extend(_validate_records(joins, METHOD_STATUS_JOIN_SCHEMA, "method_status_join"))
    errors.extend(_validate_one(report, CROSS_STAGE_REPORT_SCHEMA, "cross_stage_report"))
    errors.extend(_validate_one(generated_summary, UNIFICATION_SUMMARY_SCHEMA, "summary.json"))
    errors.extend(_validate_one(committed_summary, UNIFICATION_SUMMARY_SCHEMA, str(summary_path)))
    if generated_summary != committed_summary:
        errors.append("Committed Stage 4P summary does not match generated summary.json")
    if report.get("total_source_inventory_records") != len(inventory):
        errors.append("source inventory count mismatch")
    if report.get("unified_result_records") != len(results):
        errors.append("unified result count mismatch")
    if report.get("unified_score_summary_records") != len(scores):
        errors.append("unified score-summary count mismatch")
    if report.get("method_status_joins") != len(joins):
        errors.append("method status join count mismatch")
    errors.extend(_policy_errors(results + scores + joins + [report, generated_summary, committed_summary]))
    counts = {
        "source_inventory_records": len(inventory),
        "committed_summaries_loaded": int(report.get("committed_summaries_loaded", 0)),
        "optional_generated_outputs_present": int(report.get("optional_generated_outputs_present", 0)),
        "optional_generated_outputs_missing": int(report.get("optional_generated_outputs_missing", 0)),
        "unified_result_records": len(results),
        "unified_score_summary_records": len(scores),
        "method_status_joins": len(joins),
        "records_with_output_hashes": int(report.get("records_with_output_hashes", 0)),
        "records_with_parity_expectations": int(report.get("records_with_parity_expectations", 0)),
        "records_skipped_due_raw_required_input": int(report.get("records_skipped_due_raw_required_input", 0)),
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
        ident = str(
            record.get("unified_result_id")
            or record.get("unified_score_id")
            or record.get("join_id")
            or record.get("record_type")
        )
        if record.get("solve_claim") is True:
            errors.append(f"{ident}: solve_claim must be false")
        if record.get("cuda_used") is True:
            errors.append(f"{ident}: cuda_used must be false")
        if record.get("generated_outputs_committed") is True:
            errors.append(f"{ident}: generated_outputs_committed must be false")
        if record.get("raw_data_processed") is True:
            errors.append(f"{ident}: raw_data_processed must be false")
        if record.get("new_experiment_executed") is True:
            errors.append(f"{ident}: new_experiment_executed must be false")
        if record.get("new_scorer_added") is True:
            errors.append(f"{ident}: new_scorer_added must be false")
    return errors
