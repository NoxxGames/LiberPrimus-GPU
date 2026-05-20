"""Stage 4H CPU batch transform API CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cpu_batch.adapter_expansion import build_adapter_coverage
from libreprimus.cpu_batch.export import run_cpu_batch, write_adapter_coverage
from libreprimus.cpu_batch.models import DEFAULT_OUTPUT_DIR, DEFAULT_REGISTRY, STAGE4O_OUTPUT_DIR, STAGE4O_SUMMARY_PATH
from libreprimus.cpu_batch.parity_readiness import write_stage4o_readiness
from libreprimus.cpu_batch.summary import load_generated_summary
from libreprimus.cpu_batch.validation import validate_manifest_path, validate_results_dir, validate_stage4o_results
from libreprimus.paths import repo_root

cpu_batch_app = typer.Typer(no_args_is_help=True)
console = Console()


@cpu_batch_app.command("validate-manifest")
def cpu_batch_validate_manifest(
    manifest: Path = typer.Option(..., "--manifest", help="CPU batch manifest to validate."),
) -> None:
    """Validate a CPU batch manifest."""

    errors = validate_manifest_path(_resolve(manifest))
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("cpu_batch_manifest_valid=true")


@cpu_batch_app.command("run")
def cpu_batch_run(
    manifest: Path = typer.Option(..., "--manifest", help="CPU batch manifest to run."),
    out_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warning records."),
) -> None:
    """Run a small CPU-only transform batch."""

    try:
        summary = run_cpu_batch(manifest=_resolve(manifest), out_dir=_resolve(out_dir), allow_warnings=allow_warnings)
    except Exception as error:  # noqa: BLE001 - CLI reports validation/runtime failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@cpu_batch_app.command("adapter-coverage")
def cpu_batch_adapter_coverage(
    registry: Path = typer.Option(DEFAULT_REGISTRY, "--registry", help="CPU transform registry JSON."),
    out_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow missing-adapter coverage warnings."),
) -> None:
    """Report CPU batch adapter coverage for registry entries."""

    try:
        payload = write_adapter_coverage(registry_path=_resolve(registry), out_dir=_resolve(out_dir))
    except Exception as error:  # noqa: BLE001
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(payload)
    if payload.get("missing_adapter_count", 0) and not allow_warnings:
        raise typer.Exit(1)


@cpu_batch_app.command("validate-results")
def cpu_batch_validate_results(
    results_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--results-dir", help="Generated output directory."),
) -> None:
    """Validate generated CPU batch result files."""

    try:
        counts, errors = validate_results_dir(_resolve(results_dir))
    except Exception as error:  # noqa: BLE001
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("cpu_batch_results_valid=true")


@cpu_batch_app.command("summary")
def cpu_batch_summary(
    results_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--results-dir", help="Generated output directory."),
) -> None:
    """Print generated CPU batch summary fields."""

    _print_summary(load_generated_summary(_resolve(results_dir)))


@cpu_batch_app.command("solved-fixture-parity")
def cpu_batch_solved_fixture_parity(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 4O solved-fixture-safe CPU batch manifest."),
    out_dir: Path = typer.Option(STAGE4O_OUTPUT_DIR, "--out-dir", help="Generated Stage 4O output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warning records."),
) -> None:
    """Run the Stage 4O solved-fixture-safe parity batch."""

    try:
        summary = run_cpu_batch(manifest=_resolve(manifest), out_dir=_resolve(out_dir), allow_warnings=allow_warnings)
    except Exception as error:  # noqa: BLE001
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@cpu_batch_app.command("adapter-expansion")
def cpu_batch_adapter_expansion(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 4O adapter expansion manifest."),
    registry: Path = typer.Option(DEFAULT_REGISTRY, "--registry", help="CPU transform registry JSON."),
    out_dir: Path = typer.Option(STAGE4O_OUTPUT_DIR, "--out-dir", help="Generated Stage 4O output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow deferred adapter coverage warnings."),
) -> None:
    """Report expanded Stage 4O adapter coverage without changing transform semantics."""

    errors = validate_manifest_path(_resolve(manifest))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    try:
        payload = build_adapter_coverage(registry_path=_resolve(registry), out_dir=_resolve(out_dir))
    except Exception as error:  # noqa: BLE001
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(payload)
    if payload.get("missing_or_deferred_adapter_count", 0) and not allow_warnings:
        raise typer.Exit(1)


@cpu_batch_app.command("parity-readiness")
def cpu_batch_parity_readiness(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 4O CPU/CUDA parity readiness manifest."),
    out_dir: Path = typer.Option(STAGE4O_OUTPUT_DIR, "--out-dir", help="Generated Stage 4O output directory."),
    summary_out: Path = typer.Option(STAGE4O_SUMMARY_PATH, "--summary-out", help="Committed Stage 4O summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow parity readiness warnings."),
) -> None:
    """Write Stage 4O parity expectations, scoring compatibility, and committed summary."""

    errors = validate_manifest_path(_resolve(manifest))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    try:
        summary = write_stage4o_readiness(
            manifest=_resolve(manifest),
            results_dir=_resolve(out_dir),
            summary_out=_resolve(summary_out),
        )
    except Exception as error:  # noqa: BLE001
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)
    if summary.get("transform_adapters_missing_or_deferred", 0) and not allow_warnings:
        raise typer.Exit(1)


@cpu_batch_app.command("validate-stage4o")
def cpu_batch_validate_stage4o(
    results_dir: Path = typer.Option(STAGE4O_OUTPUT_DIR, "--results-dir", help="Generated Stage 4O output directory."),
    summary: Path = typer.Option(STAGE4O_SUMMARY_PATH, "--summary", help="Committed Stage 4O summary YAML."),
) -> None:
    """Validate Stage 4O CPU batch expansion outputs and committed summary."""

    try:
        counts, errors = validate_stage4o_results(_resolve(results_dir), _resolve(summary))
    except Exception as error:  # noqa: BLE001
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("cpu_batch_stage4o_valid=true")


def _print_summary(payload: dict) -> None:
    for key, value in payload.items():
        if isinstance(value, dict):
            continue
        if isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
            continue
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(cpu_batch_app, name="cpu-batch")
