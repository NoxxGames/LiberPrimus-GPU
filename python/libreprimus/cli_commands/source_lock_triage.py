"""Stage 4B source-lock triage CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.paths import repo_root
from libreprimus.source_lock_triage.export import run_source_lock_triage
from libreprimus.source_lock_triage.models import (
    DEFAULT_COOKIE_SOURCE_RECORDS,
    DEFAULT_MANIFEST_DIR,
    DEFAULT_NEGATIVE_CONTROLS,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PROMOTED_SOURCES,
    DEFAULT_SOURCE_HEALTH,
    DEFAULT_STAGE4A_DIR,
    DEFAULT_VISUAL_OBSERVATIONS,
)
from libreprimus.source_lock_triage.summary import summarize_records
from libreprimus.source_lock_triage.validation import validate_stage4b_records

source_lock_triage_app = typer.Typer(no_args_is_help=True)
console = Console()


@source_lock_triage_app.command("run")
def source_lock_triage_run(
    stage4a_dir: Path = typer.Option(
        DEFAULT_STAGE4A_DIR, "--stage4a-dir", help="Generated Stage 4A bundle directory."
    ),
    out_dir: Path = typer.Option(
        DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated Stage 4B triage output directory."
    ),
    promoted_sources_out: Path = typer.Option(
        DEFAULT_PROMOTED_SOURCES,
        "--promoted-sources-out",
        help="Committed promoted source records YAML.",
    ),
    source_health_out: Path = typer.Option(
        DEFAULT_SOURCE_HEALTH, "--source-health-out", help="Committed source-health records YAML."
    ),
    visual_observations_out: Path = typer.Option(
        DEFAULT_VISUAL_OBSERVATIONS,
        "--visual-observations-out",
        help="Committed visual observation records YAML.",
    ),
    negative_controls_out: Path = typer.Option(
        DEFAULT_NEGATIVE_CONTROLS,
        "--negative-controls-out",
        help="Committed negative-control records YAML.",
    ),
    cookie_source_records_out: Path = typer.Option(
        DEFAULT_COOKIE_SOURCE_RECORDS,
        "--cookie-source-records-out",
        help="Committed cookie candidate source records YAML.",
    ),
    manifest_out_dir: Path = typer.Option(
        DEFAULT_MANIFEST_DIR,
        "--manifest-out-dir",
        help="Committed disabled manifest output directory.",
    ),
    allow_warnings: bool = typer.Option(
        False, "--allow-warnings", help="Allow reduced coverage warnings."
    ),
) -> None:
    """Run Stage 4B metadata-only source-lock triage."""

    try:
        summary = run_source_lock_triage(
            stage4a_dir=_resolve(stage4a_dir),
            out_dir=_resolve(out_dir),
            promoted_sources_out=_resolve(promoted_sources_out),
            source_health_out=_resolve(source_health_out),
            visual_observations_out=_resolve(visual_observations_out),
            negative_controls_out=_resolve(negative_controls_out),
            cookie_source_records_out=_resolve(cookie_source_records_out),
            manifest_out_dir=_resolve(manifest_out_dir),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI surfaces deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@source_lock_triage_app.command("validate")
def source_lock_triage_validate(
    promoted_sources: Path = typer.Option(
        DEFAULT_PROMOTED_SOURCES, "--promoted-sources", help="Promoted source records YAML."
    ),
    source_health: Path = typer.Option(
        DEFAULT_SOURCE_HEALTH, "--source-health", help="Source-health records YAML."
    ),
    visual_observations: Path = typer.Option(
        DEFAULT_VISUAL_OBSERVATIONS,
        "--visual-observations",
        help="Visual observation records YAML.",
    ),
    negative_controls: Path = typer.Option(
        DEFAULT_NEGATIVE_CONTROLS, "--negative-controls", help="Negative-control records YAML."
    ),
    cookie_source_records: Path = typer.Option(
        DEFAULT_COOKIE_SOURCE_RECORDS,
        "--cookie-source-records",
        help="Cookie candidate source records YAML.",
    ),
    manifest_dir: Path = typer.Option(
        DEFAULT_MANIFEST_DIR, "--manifest-dir", help="Disabled manifest directory."
    ),
) -> None:
    """Validate committed Stage 4B source-lock triage records."""

    counts, errors = validate_stage4b_records(
        promoted_sources=_resolve(promoted_sources),
        source_health=_resolve(source_health),
        visual_observations=_resolve(visual_observations),
        negative_controls=_resolve(negative_controls),
        cookie_source_records=_resolve(cookie_source_records),
        manifest_dir=_resolve(manifest_dir),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("source_lock_triage_valid=true")


@source_lock_triage_app.command("summary")
def source_lock_triage_summary(
    promoted_sources: Path = typer.Option(
        DEFAULT_PROMOTED_SOURCES, "--promoted-sources", help="Promoted source records YAML."
    ),
    visual_observations: Path = typer.Option(
        DEFAULT_VISUAL_OBSERVATIONS,
        "--visual-observations",
        help="Visual observation records YAML.",
    ),
    negative_controls: Path = typer.Option(
        DEFAULT_NEGATIVE_CONTROLS, "--negative-controls", help="Negative-control records YAML."
    ),
    manifest_dir: Path = typer.Option(
        DEFAULT_MANIFEST_DIR, "--manifest-dir", help="Disabled manifest directory."
    ),
) -> None:
    """Print a concise Stage 4B source-lock triage summary."""

    summary = summarize_records(
        promoted_sources=_resolve(promoted_sources),
        visual_observations=_resolve(visual_observations),
        negative_controls=_resolve(negative_controls),
        manifest_dir=_resolve(manifest_dir),
    )
    _print_summary(summary)


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                console.print(f"{inner_key}={inner_value}")
        elif isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
        else:
            console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(source_lock_triage_app, name="source-lock-triage")
