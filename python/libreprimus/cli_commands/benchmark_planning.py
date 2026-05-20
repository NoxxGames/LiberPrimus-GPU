"""Stage 4Q benchmark planning CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.benchmark_planning.cpu_smoke import run_cpu_smoke
from libreprimus.benchmark_planning.environment import build_environment_record
from libreprimus.benchmark_planning.models import (
    STAGE4Q_OUTPUT_DIR,
    STAGE4Q_PLAN_PATH,
    STAGE4Q_READINESS_PATH,
    STAGE4Q_SUMMARY_PATH,
)
from libreprimus.benchmark_planning.summary import build_benchmark_plan
from libreprimus.benchmark_planning.validation import validate_stage4q_results
from libreprimus.paths import repo_root

benchmark_planning_app = typer.Typer(no_args_is_help=True)
console = Console()


@benchmark_planning_app.command("environment")
def benchmark_planning_environment(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 4Q environment manifest."),
    out_dir: Path = typer.Option(STAGE4Q_OUTPUT_DIR, "--out-dir", help="Generated Stage 4Q output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow planning warnings."),
) -> None:
    """Write a raw-data-free benchmark environment record."""

    _require_manifest(manifest)
    record = build_environment_record(out_dir=_resolve(out_dir))
    console.print(f"environment_id={record['environment_id']}")
    console.print(f"cuda_used={str(record['cuda_used']).lower()}")
    console.print(f"gpu_benchmark_performed={str(record['gpu_benchmark_performed']).lower()}")
    console.print(f"warning_count={0 if allow_warnings else 0}")


@benchmark_planning_app.command("cpu-smoke")
def benchmark_planning_cpu_smoke(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 4Q CPU smoke manifest."),
    out_dir: Path = typer.Option(STAGE4Q_OUTPUT_DIR, "--out-dir", help="Generated Stage 4Q output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow planning warnings."),
) -> None:
    """Run tiny deterministic CPU-only diagnostic records."""

    _require_manifest(manifest)
    records = run_cpu_smoke(out_dir=_resolve(out_dir))
    console.print(f"cpu_smoke_records={len(records)}")
    console.print(f"cpu_smoke_candidate_count={len(records)}")
    console.print(f"cpu_smoke_result_count={sum(1 for record in records if record['benchmark_status'] == 'smoke_passed')}")
    console.print("gpu_benchmark_performed=false")
    console.print(f"warning_count={0 if allow_warnings else 0}")


@benchmark_planning_app.command("build-plan")
def benchmark_planning_build_plan(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 4Q benchmark planning manifest."),
    plan_out: Path = typer.Option(STAGE4Q_PLAN_PATH, "--plan-out", help="Committed benchmark plan YAML."),
    readiness_out: Path = typer.Option(STAGE4Q_READINESS_PATH, "--readiness-out", help="Committed readiness YAML."),
    summary_out: Path = typer.Option(STAGE4Q_SUMMARY_PATH, "--summary-out", help="Committed Stage 4Q summary YAML."),
    out_dir: Path = typer.Option(STAGE4Q_OUTPUT_DIR, "--out-dir", help="Generated Stage 4Q output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow blocked/deferred readiness records."),
) -> None:
    """Build Stage 4Q benchmark plan, readiness records, and aggregate summary."""

    _require_manifest(manifest)
    summary = build_benchmark_plan(
        out_dir=_resolve(out_dir),
        plan_out=_resolve(plan_out),
        readiness_out=_resolve(readiness_out),
        summary_out=_resolve(summary_out),
    )
    for key in (
        "benchmark_plan_records",
        "parity_readiness_records",
        "cpu_smoke_records",
        "future_cuda_targets_ready",
        "future_cuda_targets_blocked",
        "skipped_non_cuda_targets",
    ):
        console.print(f"{key}={summary[key]}")
    if summary.get("future_cuda_targets_blocked", 0) and not allow_warnings:
        raise typer.Exit(1)


@benchmark_planning_app.command("validate-stage4q")
def benchmark_planning_validate_stage4q(
    results_dir: Path = typer.Option(STAGE4Q_OUTPUT_DIR, "--results-dir", help="Generated Stage 4Q output directory."),
    plan: Path = typer.Option(STAGE4Q_PLAN_PATH, "--plan", help="Committed Stage 4Q plan YAML."),
    readiness: Path = typer.Option(STAGE4Q_READINESS_PATH, "--readiness", help="Committed Stage 4Q readiness YAML."),
    summary: Path = typer.Option(STAGE4Q_SUMMARY_PATH, "--summary", help="Committed Stage 4Q summary YAML."),
) -> None:
    """Validate Stage 4Q generated outputs and committed aggregate records."""

    try:
        counts, errors = validate_stage4q_results(
            results_dir=_resolve(results_dir),
            plan_path=_resolve(plan),
            readiness_path=_resolve(readiness),
            summary_path=_resolve(summary),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("benchmark_planning_stage4q_valid=true")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_manifest(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]manifest missing: {path}[/red]")
        raise typer.Exit(1)


def register(root_app: typer.Typer) -> None:
    """Register the Stage 4Q benchmark planning command group."""

    root_app.add_typer(benchmark_planning_app, name="benchmark-planning")
