"""Stage 5A CUDA planning CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_planning.export import write_empty_warnings
from libreprimus.cuda_planning.implementation_gates import build_implementation_gates
from libreprimus.cuda_planning.models import (
    IMPLEMENTATION_GATES_PATH,
    NON_TARGETS_PATH,
    PARITY_SCAFFOLD_PATH,
    STAGE5A_OUTPUT_DIR,
    SUMMARY_PATH,
    TARGET_PLAN_PATH,
)
from libreprimus.cuda_planning.parity_scaffold import build_parity_scaffold
from libreprimus.cuda_planning.summary import build_summary
from libreprimus.cuda_planning.target_plan import build_target_plan
from libreprimus.cuda_planning.validation import validate_stage5a_results
from libreprimus.paths import repo_root

cuda_planning_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_planning_app.command("build-target-plan")
def cuda_planning_build_target_plan(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5A target-plan manifest."),
    out_dir: Path = typer.Option(STAGE5A_OUTPUT_DIR, "--out-dir", help="Generated Stage 5A output directory."),
    target_plan_out: Path = typer.Option(TARGET_PLAN_PATH, "--target-plan-out", help="Committed target-plan YAML."),
    non_targets_out: Path = typer.Option(NON_TARGETS_PATH, "--non-targets-out", help="Committed non-target YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow blocked/deferred records."),
) -> None:
    """Build planning-only CUDA target and non-target records."""

    _require_manifest(manifest)
    target_plan, non_targets = build_target_plan(
        out_dir=_resolve(out_dir),
        target_plan_out=_resolve(target_plan_out),
        non_targets_out=_resolve(non_targets_out),
    )
    write_empty_warnings(_resolve(out_dir))
    ready = sum(1 for record in target_plan if record["target_status"] == "ready_for_planning")
    blocked = sum(1 for record in target_plan if str(record["target_status"]).startswith("blocked"))
    console.print(f"target_plan_records={len(target_plan)}")
    console.print(f"ready_targets={ready}")
    console.print(f"blocked_targets={blocked}")
    console.print(f"non_target_records={len(non_targets)}")
    console.print("cuda_implementation_added=false")
    console.print("gpu_benchmark_performed=false")
    if blocked and not allow_warnings:
        raise typer.Exit(1)


@cuda_planning_app.command("build-parity-scaffold")
def cuda_planning_build_parity_scaffold(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5A parity-scaffold manifest."),
    out_dir: Path = typer.Option(STAGE5A_OUTPUT_DIR, "--out-dir", help="Generated Stage 5A output directory."),
    parity_scaffold_out: Path = typer.Option(
        PARITY_SCAFFOLD_PATH,
        "--parity-scaffold-out",
        help="Committed parity-scaffold YAML.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow planning warnings."),
) -> None:
    """Build planning-only future CUDA parity scaffold records."""

    _require_manifest(manifest)
    records = build_parity_scaffold(
        out_dir=_resolve(out_dir),
        parity_scaffold_out=_resolve(parity_scaffold_out),
    )
    write_empty_warnings(_resolve(out_dir))
    console.print(f"parity_scaffold_records={len(records)}")
    console.print("cuda_execution_performed=false")
    console.print(f"warning_count={0 if allow_warnings else 0}")


@cuda_planning_app.command("build-implementation-gates")
def cuda_planning_build_implementation_gates(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5A implementation-gates manifest."),
    out_dir: Path = typer.Option(STAGE5A_OUTPUT_DIR, "--out-dir", help="Generated Stage 5A output directory."),
    implementation_gates_out: Path = typer.Option(
        IMPLEMENTATION_GATES_PATH,
        "--implementation-gates-out",
        help="Committed implementation-gates YAML.",
    ),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5A summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow blocked/deferred gates."),
) -> None:
    """Build implementation gate records and the aggregate Stage 5A summary."""

    _require_manifest(manifest)
    gates = build_implementation_gates(
        out_dir=_resolve(out_dir),
        implementation_gates_out=_resolve(implementation_gates_out),
    )
    summary = build_summary(out_dir=_resolve(out_dir), summary_out=_resolve(summary_out))
    write_empty_warnings(_resolve(out_dir))
    console.print(f"implementation_gate_records={len(gates)}")
    console.print(f"satisfied_gates={summary['satisfied_gates']}")
    console.print(f"blocked_deferred_gates={summary['blocked_deferred_gates']}")
    console.print("cuda_implementation_added=false")
    console.print("gpu_benchmark_performed=false")
    if summary["blocked_deferred_gates"] and not allow_warnings:
        raise typer.Exit(1)


@cuda_planning_app.command("validate-stage5a")
def cuda_planning_validate_stage5a(
    target_plan: Path = typer.Option(TARGET_PLAN_PATH, "--target-plan", help="Committed target-plan YAML."),
    parity_scaffold: Path = typer.Option(
        PARITY_SCAFFOLD_PATH,
        "--parity-scaffold",
        help="Committed parity-scaffold YAML.",
    ),
    implementation_gates: Path = typer.Option(
        IMPLEMENTATION_GATES_PATH,
        "--implementation-gates",
        help="Committed implementation-gates YAML.",
    ),
    non_targets: Path = typer.Option(NON_TARGETS_PATH, "--non-targets", help="Committed non-target YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5A summary YAML."),
) -> None:
    """Validate Stage 5A CUDA planning records."""

    try:
        counts, errors = validate_stage5a_results(
            target_plan_path=_resolve(target_plan),
            parity_scaffold_path=_resolve(parity_scaffold),
            implementation_gates_path=_resolve(implementation_gates),
            non_targets_path=_resolve(non_targets),
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
    console.print("cuda_planning_stage5a_valid=true")


@cuda_planning_app.command("summary")
def cuda_planning_summary(
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5A summary YAML."),
) -> None:
    """Print the committed Stage 5A planning summary."""

    from libreprimus.benchmark_planning.export import read_yaml

    payload = read_yaml(_resolve(summary))
    for key in (
        "target_plan_records",
        "ready_targets",
        "blocked_targets",
        "non_target_records",
        "parity_scaffold_records",
        "implementation_gate_records",
        "satisfied_gates",
        "blocked_deferred_gates",
        "stage4o_parity_references_used",
        "stage4p_unified_result_references_used",
    ):
        console.print(f"{key}={payload.get(key)}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_manifest(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]manifest missing: {path}[/red]")
        raise typer.Exit(1)


def register(root_app: typer.Typer) -> None:
    """Register the Stage 5A CUDA planning command group."""

    root_app.add_typer(cuda_planning_app, name="cuda-planning")
