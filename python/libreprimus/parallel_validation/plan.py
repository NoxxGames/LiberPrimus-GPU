"""Stage 5AX validation plan construction."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .models import (
    COMMAND_REGISTRY_PATH,
    DEFAULT_RESULTS_DIR,
    NEXT_STAGE_TITLE,
    PLAN_PATH,
    PYTEST_SHARD_PLAN_PATH,
    RUN_POLICY_PATH,
    SAFETY_AUDIT_PATH,
    STAGE_ID,
    STAGE_TITLE,
    ValidationCommand,
)
from .pytest_runner import recommended_pytest_workers, shard_plan_record
from .results import write_yaml


def default_max_workers() -> int:
    return max(1, min(8, os.cpu_count() or 1))


def default_commands() -> list[ValidationCommand]:
    """Return the conservative Stage 5AX command registry."""

    python = "{python}"
    powershell = "{powershell}"
    return [
        ValidationCommand(
            command_id="ruff-check",
            display_name="Ruff",
            command=[python, "-m", "ruff", "check", "python/libreprimus", "tests/python"],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
            notes="Read-only style/lint check.",
        ),
        ValidationCommand(
            command_id="doc-staleness",
            display_name="Document staleness strict check",
            command=[
                python,
                "-m",
                "libreprimus.cli",
                "consistency",
                "check-doc-staleness",
                "--source-of-truth",
                "data/project-state/stage5ah-doc-staleness-source-of-truth.yaml",
                "--strict",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="observation-paths",
            display_name="Observation-review path sanitisation",
            command=[
                python,
                "-m",
                "libreprimus.cli",
                "observation-review",
                "check-paths",
                "--repo-root",
                ".",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="research-synthesis",
            display_name="Research synthesis validation",
            command=[
                python,
                "-m",
                "libreprimus.cli",
                "research-synthesis",
                "validate",
                "--data-dir",
                "data/research",
                "--staged-plan",
                "docs/roadmap/staged-plan.md",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="state-drift",
            display_name="State-drift consistency",
            command=[
                python,
                "-m",
                "libreprimus.cli",
                "consistency",
                "check-state-drift",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="smoke",
            display_name="Python smoke",
            command=[python, "-m", "libreprimus.cli", "smoke"],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=120,
        ),
        ValidationCommand(
            command_id="verify-public-docs-status",
            display_name="Public docs status",
            command=[
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/ci/verify-public-docs-status.ps1",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
            notes="Runs a small read-only pytest subset.",
        ),
        ValidationCommand(
            command_id="verify-lock-hashes",
            display_name="Lock hash validation",
            command=[
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/ci/verify-lock-hashes.ps1",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="validate-workflow-static",
            display_name="Workflow static validation",
            command=[
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/ci/validate-workflow-static.ps1",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="validate-wiki-source",
            display_name="Wiki source validation",
            command=[
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/github/validate-wiki-source.ps1",
            ],
            parallel_class="read_only_parallel_safe",
            requires_serial=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="sync-tutorials-wiki-dryrun",
            display_name="Tutorial-to-wiki dry run",
            command=[
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/github/sync-tutorials-to-wiki.ps1",
                "--DryRun",
            ],
            parallel_class="serial_read_only_final_check",
            requires_serial=True,
            timeout_seconds=300,
            notes="Dry-run sync touches wiki mirror staging state and stays serial.",
        ),
        ValidationCommand(
            command_id="consistency-check-all-final",
            display_name="Full consistency final check",
            command=[python, "-m", "libreprimus.cli", "consistency", "check-all", "--allow-warnings"],
            parallel_class="serial_read_only_final_check",
            requires_serial=True,
            timeout_seconds=1200,
            notes="Recorded as serial final confirmation; not parallelised by the harness.",
        ),
        ValidationCommand(
            command_id="run-consistency-checks-final",
            display_name="Full CI consistency script",
            command=[
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/ci/run-consistency-checks.ps1",
            ],
            parallel_class="serial_read_only_final_check",
            requires_serial=True,
            timeout_seconds=1800,
        ),
        ValidationCommand(
            command_id="git-status",
            display_name="Git status",
            command=["git", "status", "--short"],
            parallel_class="serial_git_mutating",
            uses_git_mutation=False,
            requires_serial=True,
            timeout_seconds=120,
            notes="Serial git safety check; not mutating but kept out of the parallel scheduler.",
        ),
        ValidationCommand(
            command_id="github-issue-update",
            display_name="GitHub issue update",
            command=["gh", "issue", "comment"],
            parallel_class="serial_remote_or_network",
            uses_network=True,
            uses_github_mutation=True,
            requires_serial=True,
            allowed_in_ci=False,
            timeout_seconds=120,
        ),
        ValidationCommand(
            command_id="commit-push",
            display_name="Commit and push",
            command=["git", "push"],
            parallel_class="serial_git_mutating",
            uses_git_mutation=True,
            requires_serial=True,
            allowed_in_ci=False,
            timeout_seconds=300,
        ),
        ValidationCommand(
            command_id="token-block-experiment",
            display_name="Token-block experiment execution",
            command=["blocked"],
            parallel_class="blocked",
            writes_outputs=True,
            requires_serial=True,
            allowed_in_ci=False,
            allowed_in_codex_local=False,
            notes="Blocked by Stage 5AX guardrails.",
        ),
    ]


def build_plan_records(max_workers: int | None = None) -> dict[str, dict[str, Any]]:
    workers = max(1, min(max_workers or default_max_workers(), 8))
    commands = default_commands()
    parallel_count = sum(command.parallel_safe for command in commands)
    serial_count = sum(command.parallel_class.startswith("serial_") for command in commands)
    blocked_count = sum(command.parallel_class == "blocked" for command in commands)
    registry = {
        "record_type": "stage5ax_parallel_command_registry",
        "schema": "schemas/ci/parallel-command-registry-v0.schema.json",
        "stage_id": STAGE_ID,
        "command_count": len(commands),
        "parallel_safe_command_count": parallel_count,
        "serial_command_count": serial_count,
        "blocked_command_count": blocked_count,
        "commands": [command.to_record() for command in commands],
    }
    policy = {
        "record_type": "stage5ax_parallel_run_policy",
        "schema": "schemas/ci/parallel-run-policy-v0.schema.json",
        "stage_id": STAGE_ID,
        "default_workers": "auto",
        "max_workers_default": workers,
        "max_workers_cap": 8,
        "env_override": "LIBERPRIMUS_VALIDATION_WORKERS",
        "pytest_worker_override": "LIBERPRIMUS_PYTEST_WORKERS",
        "pytest_mode_override": "LIBERPRIMUS_PYTEST_MODE",
        "results_dir_override": "LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR",
        "parallel_classes_allowed": [
            "read_only_parallel_safe",
            "read_only_parallel_safe_with_isolated_temp",
        ],
        "serial_classes_blocked_from_parallel": [
            "serial_read_only_final_check",
            "serial_generates_outputs",
            "serial_git_mutating",
            "serial_remote_or_network",
            "serial_manual_only",
            "blocked",
        ],
        "ci_default_parallel": False,
        "codex_local_parallel_recommended": True,
    }
    plan = {
        "record_type": "stage5ax_parallel_validation_plan",
        "schema": "schemas/ci/parallel-validation-plan-v0.schema.json",
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "status": "ready",
        "command_registry": str(COMMAND_REGISTRY_PATH.as_posix()),
        "run_policy": str(RUN_POLICY_PATH.as_posix()),
        "results_dir": str(DEFAULT_RESULTS_DIR.as_posix()),
        "pytest_modes": ["auto", "xdist", "shard", "serial"],
        "parallel_safe_command_count": parallel_count,
        "serial_command_count": serial_count,
        "blocked_command_count": blocked_count,
        "serial_final_confirmation_recorded": True,
        "bounded_preflight_moved_to": NEXT_STAGE_TITLE,
        "no_cryptanalytic_execution": True,
    }
    safety = build_safety_audit(registry, policy, max_workers_used=workers)
    shard_plan = shard_plan_record(Path("tests/python"), recommended_pytest_workers(8, workers))
    return {
        "plan": plan,
        "registry": registry,
        "policy": policy,
        "safety": safety,
        "pytest_shard_plan": shard_plan,
    }


def build_safety_audit(
    registry: dict[str, Any],
    policy: dict[str, Any],
    *,
    max_workers_used: int,
    pytest_mode_used: str = "not_run",
    pytest_workers_used: int = 0,
    pytest_xdist_available: bool = False,
    pytest_shard_fallback_used: bool = False,
    failure_count: int = 0,
    success_count: int = 0,
) -> dict[str, Any]:
    commands = registry["commands"]
    return {
        "record_type": "stage5ax_parallel_validation_safety_audit",
        "schema": "schemas/ci/parallel-validation-safety-audit-v0.schema.json",
        "stage_id": STAGE_ID,
        "git_mutating_commands_parallelised": False,
        "github_issue_commands_parallelised": False,
        "commit_push_commands_parallelised": False,
        "stage_specific_output_generating_build_commands_parallelised": False,
        "network_commands_parallelised": False,
        "raw_data_paths_written": False,
        "experiments_results_outputs_ignored": True,
        "parallel_worker_count_capped": True,
        "logs_separated_per_command": True,
        "failure_aggregation_preserves_all_failures": True,
        "serial_final_confirmation_recorded": True,
        "parallel_safe_command_count": registry["parallel_safe_command_count"],
        "serial_command_count": registry["serial_command_count"],
        "blocked_command_count": registry["blocked_command_count"],
        "max_workers_configured": policy["max_workers_cap"],
        "max_workers_used": max_workers_used,
        "pytest_mode_used": pytest_mode_used,
        "pytest_workers_used": pytest_workers_used,
        "pytest_xdist_available": pytest_xdist_available,
        "pytest_shard_fallback_used": pytest_shard_fallback_used,
        "failure_count": failure_count,
        "success_count": success_count,
        "parallelised_command_ids": [
            command["command_id"]
            for command in commands
            if command["parallel_class"]
            in {"read_only_parallel_safe", "read_only_parallel_safe_with_isolated_temp"}
            and not command["requires_serial"]
        ],
    }


def write_plan_records(
    *,
    out_plan: Path = PLAN_PATH,
    out_command_registry: Path = COMMAND_REGISTRY_PATH,
    out_run_policy: Path = RUN_POLICY_PATH,
    out_safety_audit: Path = SAFETY_AUDIT_PATH,
    out_pytest_shard_plan: Path = PYTEST_SHARD_PLAN_PATH,
) -> dict[str, dict[str, Any]]:
    records = build_plan_records()
    write_yaml(out_plan, records["plan"])
    write_yaml(out_command_registry, records["registry"])
    write_yaml(out_run_policy, records["policy"])
    write_yaml(out_safety_audit, records["safety"])
    write_yaml(out_pytest_shard_plan, records["pytest_shard_plan"])
    return records
