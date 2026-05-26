"""CLI commands for the Stage 5AX parallel validation harness."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.parallel_validation.models import (
    COMMAND_REGISTRY_PATH,
    DEFAULT_RESULTS_DIR,
    GUARDRAIL_PATH,
    NEXT_STAGE_DECISION_PATH,
    PLAN_PATH,
    PYTEST_SHARD_PLAN_PATH,
    RUN_POLICY_PATH,
    RUN_SUMMARY_PATH,
    SAFETY_AUDIT_PATH,
    SUMMARY_PATH,
)
from libreprimus.parallel_validation.plan import write_plan_records
from libreprimus.parallel_validation.pytest_runner import run_pytest
from libreprimus.parallel_validation.stage5ax import (
    build_stage5ax_summary,
    run_stage5ax_parallel_validation,
    summary_lines,
)
from libreprimus.parallel_validation.validation import validate_stage5ax_records

console = Console()
app = typer.Typer(no_args_is_help=True)


@app.command("build-stage5ax-plan")
def build_stage5ax_plan_command(
    out_plan: Path = typer.Option(PLAN_PATH),
    out_command_registry: Path = typer.Option(COMMAND_REGISTRY_PATH),
    out_run_policy: Path = typer.Option(RUN_POLICY_PATH),
    out_safety_audit: Path = typer.Option(SAFETY_AUDIT_PATH),
    out_pytest_shard_plan: Path = typer.Option(PYTEST_SHARD_PLAN_PATH),
) -> None:
    records = write_plan_records(
        out_plan=out_plan,
        out_command_registry=out_command_registry,
        out_run_policy=out_run_policy,
        out_safety_audit=out_safety_audit,
        out_pytest_shard_plan=out_pytest_shard_plan,
    )
    console.print(f"parallel_safe_command_count={records['registry']['parallel_safe_command_count']}")
    console.print(f"serial_command_count={records['registry']['serial_command_count']}")
    console.print(f"blocked_command_count={records['registry']['blocked_command_count']}")


@app.command("run-stage5ax-pytest")
def run_stage5ax_pytest_command(
    workers: int = typer.Option(16),
    pytest_mode: str = typer.Option("auto"),
    results_dir: Path = typer.Option(DEFAULT_RESULTS_DIR),
) -> None:
    result = run_pytest(
        repo_root=Path(".").resolve(),
        test_root=Path("tests/python"),
        results_dir=results_dir,
        requested_mode=pytest_mode,
        worker_count=workers,
    )
    console.print(f"pytest_mode_used={result['pytest_mode_used']}")
    console.print(f"pytest_xdist_available={str(result['pytest_xdist_available']).lower()}")
    console.print(f"pytest_shard_fallback_used={str(result['pytest_shard_fallback_used']).lower()}")
    console.print(f"pytest_failed_count={result['failure_count']}")
    if not result["passed"]:
        raise typer.Exit(1)


@app.command("run-stage5ax-parallel-validation")
def run_stage5ax_parallel_validation_command(
    plan: Path = typer.Option(PLAN_PATH),
    workers: int = typer.Option(16),
    pytest_workers: int = typer.Option(16),
    pytest_mode: str = typer.Option("auto"),
    results_dir: Path = typer.Option(DEFAULT_RESULTS_DIR),
    out_run_summary: Path = typer.Option(RUN_SUMMARY_PATH),
) -> None:
    result = run_stage5ax_parallel_validation(
        plan_path=plan,
        workers=workers,
        pytest_workers=pytest_workers,
        pytest_mode=pytest_mode,
        results_dir=results_dir,
        out_run_summary=out_run_summary,
    )
    console.print(f"workers_used={result['workers_used']}")
    console.print(f"pytest_workers_used={result['pytest_workers_used']}")
    console.print(f"pytest_mode_used={result['pytest_mode_used']}")
    console.print(f"pytest_xdist_available={str(result['pytest_xdist_available']).lower()}")
    console.print(f"pytest_shard_fallback_used={str(result['pytest_shard_fallback_used']).lower()}")
    console.print(f"failed_command_count={result['failed_command_count']}")
    if result["failed_command_count"]:
        raise typer.Exit(1)


@app.command("build-stage5ax-summary")
def build_stage5ax_summary_command(
    plan: Path = typer.Option(PLAN_PATH),
    command_registry: Path = typer.Option(COMMAND_REGISTRY_PATH),
    run_policy: Path = typer.Option(RUN_POLICY_PATH),
    run_summary: Path = typer.Option(RUN_SUMMARY_PATH),
    safety_audit: Path = typer.Option(SAFETY_AUDIT_PATH),
    pytest_shard_plan: Path = typer.Option(PYTEST_SHARD_PLAN_PATH),
    out_guardrail: Path = typer.Option(GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(SUMMARY_PATH),
) -> None:
    _, next_stage, summary = build_stage5ax_summary(
        plan_path=plan,
        command_registry_path=command_registry,
        run_policy_path=run_policy,
        run_summary_path=run_summary,
        safety_audit_path=safety_audit,
        pytest_shard_plan_path=pytest_shard_plan,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"summary_status={summary['status']}")
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")


@app.command("validate-stage5ax")
def validate_stage5ax_command(
    plan: Path = typer.Option(PLAN_PATH),
    command_registry: Path = typer.Option(COMMAND_REGISTRY_PATH),
    run_policy: Path = typer.Option(RUN_POLICY_PATH),
    run_summary: Path = typer.Option(RUN_SUMMARY_PATH),
    safety_audit: Path = typer.Option(SAFETY_AUDIT_PATH),
    pytest_shard_plan: Path = typer.Option(PYTEST_SHARD_PLAN_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(DEFAULT_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5ax_records(
        plan_path=plan,
        command_registry_path=command_registry,
        run_policy_path=run_policy,
        run_summary_path=run_summary,
        safety_audit_path=safety_audit,
        pytest_shard_plan_path=pytest_shard_plan,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    for line in summary_lines(summary):
        console.print(line)


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="parallel-validation")
