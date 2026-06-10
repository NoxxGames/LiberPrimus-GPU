"""Stage 5AX orchestration."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from .models import (
    GUARDRAIL_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_TITLE,
    SAFETY_AUDIT_PATH,
    STAGE_ID,
    SUMMARY_PATH,
    ValidationCommand,
)
from .plan import build_safety_audit
from .pytest_runner import recommended_pytest_workers, run_pytest
from .results import aggregate_results, export_run_outputs, read_yaml, write_yaml
from .scheduler import cap_workers, run_parallel_commands


def _commands_from_registry(registry: dict[str, Any]) -> list[ValidationCommand]:
    return [ValidationCommand(**record) for record in registry.get("commands", [])]


def run_stage5ax_parallel_validation(
    *,
    plan_path: Path,
    workers: int,
    pytest_workers: int,
    pytest_mode: str,
    results_dir: Path,
    out_run_summary: Path,
    out_safety_audit: Path = SAFETY_AUDIT_PATH,
) -> dict[str, Any]:
    plan = read_yaml(plan_path)
    registry = read_yaml(Path(plan["command_registry"]))
    policy = read_yaml(Path(plan["run_policy"]))
    repo_root = Path(".").resolve()
    workers_used = cap_workers(workers, int(policy["max_workers_cap"]), os.cpu_count())
    pytest_workers_used = recommended_pytest_workers(pytest_workers, int(policy["max_workers_cap"]))
    commands = [
        command for command in _commands_from_registry(registry) if command.parallel_safe
    ]

    started = time.perf_counter()
    pytest_result = run_pytest(
        repo_root=repo_root,
        test_root=Path("tests/python"),
        results_dir=results_dir,
        requested_mode=pytest_mode,
        worker_count=pytest_workers_used,
    )
    command_results = run_parallel_commands(
        commands,
        repo_root=repo_root,
        results_dir=results_dir,
        workers=workers_used,
    )
    run_summary = aggregate_results(
        command_results,
        pytest_result,
        workers_requested=workers,
        workers_used=workers_used,
        pytest_workers_requested=pytest_workers,
        pytest_workers_used=pytest_workers_used,
        duration_seconds=time.perf_counter() - started,
        results_dir=results_dir,
    )
    export_run_outputs(results_dir, run_summary, command_results)
    write_yaml(out_run_summary, run_summary)

    safety = build_safety_audit(
        registry,
        policy,
        max_workers_used=workers_used,
        pytest_mode_used=pytest_result["pytest_mode_used"],
        pytest_workers_used=pytest_workers_used,
        pytest_xdist_available=pytest_result["pytest_xdist_available"],
        pytest_shard_fallback_used=pytest_result["pytest_shard_fallback_used"],
        failure_count=run_summary["failure_count"],
        success_count=run_summary["success_count"],
    )
    write_yaml(out_safety_audit, safety)
    return run_summary


def build_stage5ax_summary(
    *,
    plan_path: Path,
    command_registry_path: Path,
    run_policy_path: Path,
    run_summary_path: Path,
    safety_audit_path: Path,
    pytest_shard_plan_path: Path,
    out_guardrail: Path = GUARDRAIL_PATH,
    out_next_stage: Path = NEXT_STAGE_DECISION_PATH,
    out_summary: Path = SUMMARY_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = read_yaml(plan_path)
    registry = read_yaml(command_registry_path)
    run_summary = read_yaml(run_summary_path)
    safety = read_yaml(safety_audit_path)
    shard_plan = read_yaml(pytest_shard_plan_path)

    guardrail = {
        "record_type": "stage5ax_parallel_validation_guardrail",
        "schema": "schemas/ci/stage5ax-guardrail-v0.schema.json",
        "stage_id": STAGE_ID,
        "infrastructure_stage": True,
        "parallel_validation_only": True,
        "cryptanalytic_execution_performed": False,
        "token_experiments_executed": False,
        "variant_byte_streams_generated": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "stego_tool_execution_performed": False,
        "decode_attempt_performed": False,
        "hash_preimage_search_performed": False,
        "cuda_execution_performed": False,
        "benchmark_performed": False,
        "cryptanalytic_benchmark_performed": False,
        "scored_experiments_executed": False,
        "solve_claim": False,
        "generated_validation_outputs_committed": False,
        "network_fetch_performed": False,
        "live_web_scrape_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "deep_research_performed": False,
        "public_website_publication_performed": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "method_status_upgraded": False,
    }
    next_stage = {
        "record_type": "stage5ax_next_stage_decision",
        "schema": "schemas/project-state/stage5ax-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "selected_option_id": "stage5ay_bounded_token_block_preflight_manifest_design_without_execution",
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "selected_next_stage_reason": (
            "User inserted Stage 5AX validation infrastructure before the Stage 5AW-selected "
            "bounded preflight work; the preflight design moves to Stage 5AY after the harness validates."
        ),
        "recommended_next_prompt_type": "bounded_preflight_manifest_design_without_execution",
        "execution_enabled": False,
        "solve_claim": False,
    }
    summary = {
        "record_type": "stage5ax_parallel_validation_harness_summary",
        "schema": "schemas/project-state/stage5ax-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete" if run_summary.get("failed_command_count") == 0 else "failed",
        "source_stage_id": "stage-5aw",
        "source_stage5aw_commit": "51c6d1c96c0a47420bac12f3f72055b115623eb5",
        "user_override_from_stage5aw_next_stage": True,
        "user_override_inserted_parallel_validation": True,
        "stage5aw_original_next_stage": "Stage 5AX - bounded token-block preflight manifest design without execution",
        "stage5aw_selected_next_stage": "Stage 5AX - bounded token-block preflight manifest design without execution",
        "stage5ax_actual_stage_title": "Stage 5AX - parallel validation harness and fast CI check orchestrator",
        "bounded_preflight_moved_to_stage": NEXT_STAGE_TITLE,
        "parallel_validation_plan_created": True,
        "parallel_command_registry_created": True,
        "parallel_run_policy_created": True,
        "parallel_validation_run_completed": True,
        "parallel_validation_run_passed": run_summary.get("failed_command_count") == 0,
        "parallel_validation_safety_audit_created": True,
        "parallel_validation_plan_status": plan.get("status"),
        "parallel_safe_command_count": registry.get("parallel_safe_command_count"),
        "serial_command_count": registry.get("serial_command_count"),
        "blocked_command_count": registry.get("blocked_command_count"),
        "workers_requested": run_summary.get("workers_requested"),
        "workers_used": run_summary.get("workers_used"),
        "pytest_workers_requested": run_summary.get("pytest_workers_requested"),
        "pytest_workers_used": run_summary.get("pytest_workers_used"),
        "pytest_mode_used": run_summary.get("pytest_mode_used"),
        "pytest_xdist_available": run_summary.get("pytest_xdist_available"),
        "pytest_shard_fallback_used": run_summary.get("pytest_shard_fallback_used"),
        "pytest_shard_count": run_summary.get("pytest_result", {}).get("pytest_shard_count"),
        "pytest_test_file_count": shard_plan.get("test_file_count"),
        "failed_command_count": run_summary.get("failed_command_count"),
        "commands_succeeded": run_summary.get("commands_succeeded"),
        "commands_failed": run_summary.get("commands_failed"),
        "failed_command_ids": run_summary.get("failed_command_ids"),
        "safety_audit_status": "passed" if safety.get("failure_count") == 0 else "failed",
        "serial_final_confirmation_recorded": True,
        "generated_validation_outputs_committed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "raw_data_committed": False,
        "third_party_raw_staged": False,
        "third_party_raw_tracked_new": False,
        "validation_timing_recorded": True,
        "benchmark_performed": False,
        "cryptanalytic_benchmark_performed": False,
        "network_fetch_performed": False,
        "live_web_scrape_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "deep_research_performed": False,
        "public_website_publication_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "stego_tool_execution_performed": False,
        "hash_preimage_search_performed": False,
        "decode_attempt_performed": False,
        "hypothesis_generation_performed": False,
        "hypothesis_execution_performed": False,
        "token_experiments_executed": False,
        "variant_byte_streams_generated": False,
        "variant_experiments_executed": False,
        "raw_images_committed": False,
        "cuda_execution_performed": False,
        "cuda_source_modified": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "scored_experiments_executed": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "method_status_upgraded": False,
        "solve_claim": False,
        "recommended_next_prompt_type": next_stage["recommended_next_prompt_type"],
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_stage_reason": next_stage["selected_next_stage_reason"],
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    return guardrail, next_stage, summary


def summary_lines(summary_path: Path = SUMMARY_PATH) -> list[str]:
    payload = read_yaml(summary_path)
    keys = [
        "status",
        "workers_used",
        "pytest_workers_used",
        "pytest_mode_used",
        "pytest_xdist_available",
        "pytest_shard_fallback_used",
        "parallel_safe_command_count",
        "serial_command_count",
        "failed_command_count",
        "recommended_next_stage_title",
    ]
    return [f"{key}={payload.get(key)}" for key in keys]
