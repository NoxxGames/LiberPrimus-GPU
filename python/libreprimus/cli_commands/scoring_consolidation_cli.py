"""Stage 4I scoring consolidation CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cli_commands.bounded import scoring_app
from libreprimus.paths import repo_root
from libreprimus.scoring_consolidation.cpu_batch_integration import check_cpu_batch_summary
from libreprimus.scoring_consolidation.export import consolidate_scoring
from libreprimus.scoring_consolidation.models import DEFAULT_CPU_BATCH_SUMMARY, DEFAULT_DATA_DIR, DEFAULT_OUT_DIR
from libreprimus.scoring_consolidation.summary import load_summary
from libreprimus.scoring_consolidation.validation import validate_data_dir

console = Console()


@scoring_app.command("consolidate")
def scoring_consolidate(
    out_dir: Path = typer.Option(DEFAULT_OUT_DIR, "--out-dir", help="Generated scoring consolidation output directory."),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Committed scoring data directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warning records."),
) -> None:
    """Consolidate existing scoring records and calibration summaries."""

    try:
        summary = consolidate_scoring(out_dir=_resolve(out_dir), data_dir=_resolve(data_dir), allow_warnings=allow_warnings)
    except Exception as error:  # noqa: BLE001 - CLI reports consolidation errors.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@scoring_app.command("validate")
def scoring_validate(
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Committed scoring data directory."),
) -> None:
    """Validate committed scoring consolidation records."""

    try:
        counts, errors = validate_data_dir(_resolve(data_dir))
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
    console.print("scoring_records_valid=true")


@scoring_app.command("report")
def scoring_report(
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Committed scoring data directory."),
) -> None:
    """Print the committed Stage 4I scoring report summary."""

    _print_summary(load_summary(_resolve(data_dir)))


@scoring_app.command("check-cpu-batch-compatibility")
def scoring_check_cpu_batch_compatibility(
    cpu_batch_summary: Path = typer.Option(DEFAULT_CPU_BATCH_SUMMARY, "--cpu-batch-summary", help="Committed Stage 4H CPU batch summary."),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Committed scoring data directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow compatibility warnings."),
) -> None:
    """Check CPU batch scoring compatibility with Stage 4I records."""

    payload = check_cpu_batch_summary(str(_display_path(cpu_batch_summary)))
    _print_summary(payload)
    counts, errors = validate_data_dir(_resolve(data_dir))
    if errors and not allow_warnings:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    if not payload["compatible"] and not allow_warnings:
        raise typer.Exit(1)
    console.print(f"validated_scoring_record_sets={sum(1 for value in counts.values() if value >= 0)}")


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


def _display_path(path: Path) -> Path:
    return path if path.is_absolute() else path


def register(root_app: typer.Typer) -> None:
    """Commands attach to the existing scoring group from Stage 3C."""

    _ = root_app
