"""Exploratory experiment CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

experiment_app = typer.Typer(no_args_is_help=True)


DEFAULT_EXPLORATORY_MANIFEST_DIR = Path("experiments/manifests/exploratory")
DEFAULT_STAGE2E_DRY_RUN_DIR = Path("experiments/results/exploratory-dry-runs/stage2e")


@experiment_app.command("validate-exploratory")
def experiment_validate_exploratory(
    manifest: Path = typer.Option(..., "--manifest", help="Exploratory experiment manifest path."),
) -> None:
    """Validate a Stage 2E exploratory experiment manifest without execution."""
    try:
        loaded = load_exploratory_manifest(_resolve_existing_path(manifest, "Exploratory manifest"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Exploratory manifest validation OK")
    console.print(f"manifest_id={loaded.manifest_id}")
    console.print(f"manifest_sha256={loaded.sha256}")
    console.print(f"dry_run_only={str(loaded.payload['dry_run_only']).lower()}")
    console.print(f"execution_enabled={str(loaded.payload['execution_enabled']).lower()}")
    console.print(f"search_execution_enabled={str(loaded.payload['search_execution_enabled']).lower()}")
    console.print(f"candidate_generation_enabled={str(loaded.payload['candidate_generation_enabled']).lower()}")
    console.print(f"scoring_enabled={str(loaded.payload['scoring_enabled']).lower()}")
    console.print(f"cuda_enabled={str(loaded.payload['cuda_enabled']).lower()}")


@experiment_app.command("dry-run")
def experiment_dry_run(
    manifest: Path = typer.Option(..., "--manifest", help="Exploratory experiment manifest path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2E_DRY_RUN_DIR, "--out-dir", help="Generated dry-run output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build a dry-run plan for one exploratory manifest without executing it."""
    try:
        plan = build_dry_run_plan(
            _resolve_existing_path(manifest, "Exploratory manifest"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_dry_run_outputs(_resolve_output_path(out_dir), plan)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"plan_id={plan.plan_id}")
    console.print(f"manifest_id={plan.manifest_id}")
    console.print(f"candidate_count_estimate={plan.candidate_count_estimate}")
    console.print(f"candidate_count_upper_bound={plan.candidate_count_upper_bound}")
    pass_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "pass")
    fail_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "fail")
    console.print(f"safety_gate_pass_count={pass_count}")
    console.print(f"safety_gate_fail_count={fail_count}")
    console.print(f"execution_enabled={str(plan.execution_enabled).lower()}")
    console.print(f"search_execution_enabled={str(plan.search_execution_enabled).lower()}")
    console.print(f"scoring_enabled={str(plan.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(plan.cuda_enabled).lower()}")
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)


@experiment_app.command("stage2e-dry-run-all")
def experiment_stage2e_dry_run_all(
    manifest_dir: Path = typer.Option(
        DEFAULT_EXPLORATORY_MANIFEST_DIR,
        "--manifest-dir",
        help="Directory containing Stage 2E exploratory manifests.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE2E_DRY_RUN_DIR, "--out-dir", help="Generated dry-run output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build dry-run plans for every Stage 2E exploratory manifest."""
    resolved_manifest_dir = _resolve_output_path(manifest_dir)
    resolved_out_dir = _resolve_output_path(out_dir)
    plans = []
    for manifest in sorted(resolved_manifest_dir.glob("*-dry-run.yaml")):
        try:
            plan = build_dry_run_plan(manifest, out_dir=resolved_out_dir)
        except (FileNotFoundError, ValueError) as error:
            console.print(f"[red]{manifest}: {error}[/red]")
            raise typer.Exit(1) from error
        write_dry_run_outputs(resolved_out_dir, plan)
        plans.append(plan)
        console.print(f"{plan.manifest_id}={plan.candidate_count_estimate}")
    summary_path = write_dry_run_summary(resolved_out_dir, plans)
    warning_count = sum(len(plan.warnings) for plan in plans)
    console.print(f"summary={summary_path}")
    console.print(f"manifest_count={len(plans)}")
    console.print(f"dry_run_plan_count={len(plans)}")
    console.print(f"candidate_count_total={sum(plan.candidate_count_estimate for plan in plans)}")
    console.print(f"warning_count={warning_count}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@experiment_app.command("dry-run-summary")
def experiment_dry_run_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE2E_DRY_RUN_DIR, "--results-dir", help="Generated dry-run result directory."),
) -> None:
    """Print generated exploratory dry-run summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_dry_run_summary(resolved)
    records = load_plan_records(resolved)
    for key in [
        "plan_count",
        "candidate_count_total",
        "safety_gate_pass_count",
        "safety_gate_fail_count",
        "execution_enabled_any",
        "search_execution_enabled_any",
        "scoring_enabled_any",
        "cuda_enabled_any",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for record in records:
        console.print(f"{record['manifest_id']}={record['candidate_count_estimate']}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(experiment_app, name="experiment")
