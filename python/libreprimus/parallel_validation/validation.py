"""Validation helpers for Stage 5AX records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import NEXT_STAGE_TITLE, PARALLEL_SAFE_CLASSES
from .results import read_yaml

GUARDRAIL_FALSE_FIELDS = [
    "cryptanalytic_execution_performed",
    "token_experiments_executed",
    "variant_byte_streams_generated",
    "ocr_performed",
    "ai_ml_interpretation_performed",
    "llm_vision_token_reading_performed",
    "semantic_image_interpretation_performed",
    "hidden_content_image_forensics_performed",
    "stego_tool_execution_performed",
    "decode_attempt_performed",
    "hash_preimage_search_performed",
    "cuda_execution_performed",
    "benchmark_performed",
    "cryptanalytic_benchmark_performed",
    "scored_experiments_executed",
    "solve_claim",
    "generated_validation_outputs_committed",
]


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for command in registry.get("commands", []):
        command_id = command.get("command_id")
        if not command_id:
            errors.append("command missing command_id")
            continue
        if command_id in seen:
            errors.append(f"duplicate command_id: {command_id}")
        seen.add(command_id)
        parallel_class = command.get("parallel_class")
        if parallel_class in PARALLEL_SAFE_CLASSES and command.get("requires_serial"):
            errors.append(f"parallel-safe command requires serial: {command_id}")
        if parallel_class not in PARALLEL_SAFE_CLASSES and not command.get("requires_serial"):
            errors.append(f"non-parallel command missing serial protection: {command_id}")
        if command.get("uses_git_mutation") and parallel_class in PARALLEL_SAFE_CLASSES:
            errors.append(f"git-mutating command marked parallel-safe: {command_id}")
        if command.get("uses_github_mutation") and parallel_class in PARALLEL_SAFE_CLASSES:
            errors.append(f"github-mutating command marked parallel-safe: {command_id}")
        if command.get("writes_repo") and parallel_class in PARALLEL_SAFE_CLASSES:
            errors.append(f"repo-writing command marked parallel-safe: {command_id}")
    return errors


def validate_guardrail(guardrail: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in GUARDRAIL_FALSE_FIELDS:
        if guardrail.get(field) is not False:
            errors.append(f"guardrail must be false: {field}")
    if guardrail.get("parallel_validation_only") is not True:
        errors.append("parallel_validation_only must be true")
    return errors


def validate_stage5ax_records(
    *,
    plan_path: Path,
    command_registry_path: Path,
    run_policy_path: Path,
    run_summary_path: Path,
    safety_audit_path: Path,
    pytest_shard_plan_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    plan = read_yaml(plan_path)
    registry = read_yaml(command_registry_path)
    policy = read_yaml(run_policy_path)
    run_summary = read_yaml(run_summary_path)
    safety = read_yaml(safety_audit_path)
    shard_plan = read_yaml(pytest_shard_plan_path)
    guardrail = read_yaml(guardrail_path)
    next_stage = read_yaml(next_stage_decision_path)
    summary = read_yaml(summary_path)

    errors: list[str] = []
    errors.extend(validate_registry(registry))
    errors.extend(validate_guardrail(guardrail))
    if plan.get("stage_id") != "stage-5ax":
        errors.append("plan stage_id must be stage-5ax")
    if policy.get("max_workers_cap", 0) > 16:
        errors.append("worker cap exceeds 16")
    if run_summary.get("failed_command_count", 1) != 0:
        errors.append("run summary has failed commands")
    if run_summary.get("generated_validation_outputs_committed") is not False:
        errors.append("generated validation outputs committed")
    if safety.get("git_mutating_commands_parallelised") is not False:
        errors.append("git-mutating commands parallelised")
    if safety.get("network_commands_parallelised") is not False:
        errors.append("network commands parallelised")
    if shard_plan.get("all_tests_covered_once") is not True:
        errors.append("pytest shard plan does not cover all tests once")
    if next_stage.get("selected_next_stage_title") != NEXT_STAGE_TITLE:
        errors.append("next stage must be Stage 5AY")
    if summary.get("recommended_next_stage_title") != NEXT_STAGE_TITLE:
        errors.append("summary must recommend Stage 5AY")
    if not (results_dir / "run-summary.json").exists():
        errors.append("generated run-summary.json missing")

    counts = {
        "stage5ax_plan_valid": not errors,
        "parallel_safe_command_count": registry.get("parallel_safe_command_count", 0),
        "serial_command_count": registry.get("serial_command_count", 0),
        "blocked_command_count": registry.get("blocked_command_count", 0),
        "workers_requested": run_summary.get("workers_requested", 0),
        "workers_used": run_summary.get("workers_used", 0),
        "pytest_workers_requested": run_summary.get("pytest_workers_requested", 0),
        "pytest_workers_used": run_summary.get("pytest_workers_used", 0),
        "pytest_mode_used": run_summary.get("pytest_mode_used", ""),
        "pytest_xdist_available": run_summary.get("pytest_xdist_available", False),
        "pytest_shard_fallback_used": run_summary.get("pytest_shard_fallback_used", False),
        "failed_command_count": run_summary.get("failed_command_count", 0),
        "safety_audit_valid": not errors,
        "selected_next_stage_title": next_stage.get("selected_next_stage_title", ""),
        "validation_error_count": len(errors),
    }
    return counts, errors
