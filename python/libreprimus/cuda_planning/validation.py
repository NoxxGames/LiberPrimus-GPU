"""Validation for Stage 5A CUDA planning records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.cuda_planning.models import (
    IMPLEMENTATION_GATE_SCHEMA,
    IMPLEMENTATION_GATES_PATH,
    NON_TARGET_SCHEMA,
    NON_TARGETS_PATH,
    PARITY_SCAFFOLD_PATH,
    PARITY_SCAFFOLD_SCHEMA,
    STAGE5A_OUTPUT_DIR,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
    TARGET_PLAN_PATH,
    TARGET_PLAN_SCHEMA,
)

BAD_TRUE_FLAGS = (
    "cuda_implementation_added",
    "cuda_kernel_added",
    "cuda_source_modified",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "broad_experiment_executed",
    "raw_data_processed",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "generated_outputs_committed",
    "codex_output_committed",
)


def validate_stage5a_results(
    *,
    target_plan_path: Path = TARGET_PLAN_PATH,
    parity_scaffold_path: Path = PARITY_SCAFFOLD_PATH,
    implementation_gates_path: Path = IMPLEMENTATION_GATES_PATH,
    non_targets_path: Path = NON_TARGETS_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = STAGE5A_OUTPUT_DIR,
) -> tuple[dict[str, int], list[str]]:
    target_plan = list(read_yaml(target_plan_path).get("records", []))
    scaffolds = list(read_yaml(parity_scaffold_path).get("records", []))
    gates = list(read_yaml(implementation_gates_path).get("records", []))
    non_targets = list(read_yaml(non_targets_path).get("records", []))
    summary = read_yaml(summary_path)
    generated_summary = read_json(resolve_repo_path(results_dir) / SUMMARY_REPORT)
    errors: list[str] = []
    errors.extend(_validate_records(target_plan, TARGET_PLAN_SCHEMA, "target_plan"))
    errors.extend(_validate_records(scaffolds, PARITY_SCAFFOLD_SCHEMA, "parity_scaffold"))
    errors.extend(_validate_records(gates, IMPLEMENTATION_GATE_SCHEMA, "implementation_gates"))
    errors.extend(_validate_records(non_targets, NON_TARGET_SCHEMA, "non_targets"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5A summary does not match generated summary.json")
    errors.extend(_policy_errors([*target_plan, *scaffolds, *gates, *non_targets, summary]))
    errors.extend(_semantic_errors(target_plan, scaffolds, gates, non_targets, summary))
    counts = {
        "target_plan_records": len(target_plan),
        "ready_targets": int(summary.get("ready_targets", 0)),
        "blocked_targets": int(summary.get("blocked_targets", 0)),
        "non_target_records": len(non_targets),
        "parity_scaffold_records": len(scaffolds),
        "implementation_gate_records": len(gates),
        "satisfied_gates": int(summary.get("satisfied_gates", 0)),
        "blocked_deferred_gates": int(summary.get("blocked_deferred_gates", 0)),
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
        ident = str(record.get("target_id") or record.get("scaffold_id") or record.get("gate_id") or record.get("record_type"))
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        if record.get("cuda_planning_only") is not True:
            errors.append(f"{ident}: cuda_planning_only must be true")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{ident}: no_solve_claim must be true")
    return errors


def _semantic_errors(
    targets: list[dict[str, Any]],
    scaffolds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    non_targets: list[dict[str, Any]],
    summary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    for record in targets:
        target_id = str(record.get("target_id"))
        status = str(record.get("target_status"))
        if status == "ready_for_planning":
            if not record.get("stage4o_parity_expectation_id"):
                errors.append(f"{target_id}: ready target missing Stage 4O parity expectation")
            if not record.get("stage4p_unified_result_reference"):
                errors.append(f"{target_id}: ready target missing Stage 4P unified result reference")
            if not record.get("output_token_hash"):
                errors.append(f"{target_id}: ready target missing output token hash")
        if status.startswith("blocked") and not record.get("blockers"):
            errors.append(f"{target_id}: blocked target requires blockers")
    scaffold_ids = {record.get("target_id") for record in scaffolds}
    ready_ids = {record.get("target_id") for record in targets if record.get("target_status") == "ready_for_planning"}
    if scaffold_ids != ready_ids:
        errors.append("Parity scaffold target set does not match ready target set")
    gate_ids = {str(record.get("gate_id")) for record in gates}
    if "no_speedup_claim_before_parity" not in gate_ids:
        errors.append("Missing no_speedup_claim_before_parity gate")
    non_target_text = " ".join(str(record).lower() for record in non_targets)
    for term in ("discord", "image", "stego", "audio", "cookie", "hash", "bigram", "website"):
        if term not in non_target_text:
            errors.append(f"Non-target records missing boundary term: {term}")
    if summary.get("target_plan_records") != len(targets):
        errors.append("target plan record count mismatch")
    if summary.get("parity_scaffold_records") != len(scaffolds):
        errors.append("parity scaffold record count mismatch")
    if summary.get("implementation_gate_records") != len(gates):
        errors.append("implementation gate record count mismatch")
    if summary.get("non_target_records") != len(non_targets):
        errors.append("non-target record count mismatch")
    return errors
