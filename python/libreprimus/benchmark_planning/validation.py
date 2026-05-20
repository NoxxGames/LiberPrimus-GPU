"""Validation for Stage 4Q benchmark planning outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_jsonl, read_yaml, resolve_repo_path
from libreprimus.benchmark_planning.models import (
    ENVIRONMENT_JSON,
    ENVIRONMENT_SCHEMA,
    PLAN_SCHEMA,
    READINESS_JSON,
    READINESS_SCHEMA,
    SMOKE_JSONL,
    SMOKE_SCHEMA,
    STAGE4Q_OUTPUT_DIR,
    STAGE4Q_PLAN_PATH,
    STAGE4Q_READINESS_PATH,
    STAGE4Q_SUMMARY_PATH,
    SUMMARY_JSON,
    SUMMARY_SCHEMA,
)


def validate_stage4q_results(
    *,
    results_dir: Path = STAGE4Q_OUTPUT_DIR,
    plan_path: Path = STAGE4Q_PLAN_PATH,
    readiness_path: Path = STAGE4Q_READINESS_PATH,
    summary_path: Path = STAGE4Q_SUMMARY_PATH,
) -> tuple[dict[str, int], list[str]]:
    """Validate generated Stage 4Q records and committed summaries."""

    resolved = resolve_repo_path(results_dir)
    errors: list[str] = []
    environment = read_json(resolved / ENVIRONMENT_JSON)
    smoke = read_jsonl(resolved / SMOKE_JSONL)
    generated_readiness = list(read_json(resolved / READINESS_JSON).get("records", []))
    generated_summary = read_json(resolved / SUMMARY_JSON)
    plan = list(read_yaml(plan_path).get("records", []))
    committed_readiness = list(read_yaml(readiness_path).get("records", []))
    committed_summary = read_yaml(summary_path)

    errors.extend(_validate_one(environment, ENVIRONMENT_SCHEMA, "environment"))
    errors.extend(_validate_records(smoke, SMOKE_SCHEMA, "cpu_smoke"))
    errors.extend(_validate_records(plan, PLAN_SCHEMA, "plan"))
    errors.extend(_validate_records(generated_readiness, READINESS_SCHEMA, "generated_readiness"))
    errors.extend(_validate_records(committed_readiness, READINESS_SCHEMA, "committed_readiness"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "summary.json"))
    errors.extend(_validate_one(committed_summary, SUMMARY_SCHEMA, str(summary_path)))
    if generated_readiness != committed_readiness:
        errors.append("Committed Stage 4Q readiness does not match generated readiness JSON")
    if generated_summary != committed_summary:
        errors.append("Committed Stage 4Q summary does not match generated summary.json")
    if committed_summary.get("benchmark_plan_records") != len(plan):
        errors.append("benchmark plan record count mismatch")
    if committed_summary.get("parity_readiness_records") != len(committed_readiness):
        errors.append("parity readiness record count mismatch")
    if committed_summary.get("cpu_smoke_records") != len(smoke):
        errors.append("CPU smoke record count mismatch")
    errors.extend(_policy_errors([environment, generated_summary, committed_summary, *smoke, *plan, *committed_readiness]))
    counts = {
        "benchmark_plan_records": len(plan),
        "parity_readiness_records": len(committed_readiness),
        "cpu_smoke_records": len(smoke),
        "future_cuda_targets_ready": int(committed_summary.get("future_cuda_targets_ready", 0)),
        "future_cuda_targets_blocked": int(committed_summary.get("future_cuda_targets_blocked", 0)),
        "skipped_non_cuda_targets": int(committed_summary.get("skipped_non_cuda_targets", 0)),
        "stage4o_parity_references_used": int(committed_summary.get("stage4o_parity_references_used", 0)),
        "stage4p_unified_result_references_used": int(
            committed_summary.get("stage4p_unified_result_references_used", 0)
        ),
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
        ident = str(record.get("record_type", "record"))
        for key, bad in (
            ("cuda_used", True),
            ("cuda_required", True),
            ("gpu_benchmark_performed", True),
            ("cuda_implementation_added", True),
            ("solve_claim", True),
            ("canonical_corpus_active", True),
            ("page_boundaries_final", True),
            ("generated_outputs_committed", True),
            ("raw_data_processed", True),
            ("broad_experiment_executed", True),
        ):
            if record.get(key) is bad:
                errors.append(f"{ident}: {key} must not be {bad}")
        if record.get("no_solve_claim") is False:
            errors.append(f"{ident}: no_solve_claim must be true")
    return errors
