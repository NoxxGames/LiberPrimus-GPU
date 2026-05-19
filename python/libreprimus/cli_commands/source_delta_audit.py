"""Stage 4E source-delta audit CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.paths import repo_root
from libreprimus.source_delta_audit.export import run_source_delta_audit
from libreprimus.source_delta_audit.models import (
    DEFAULT_CACHE_DIR,
    DEFAULT_IMAGE_ARTIFACT,
    DEFAULT_MANIFEST_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_REPO_URL,
    DEFAULT_SOURCE_DELTA,
    DEFAULT_SOURCE_HEALTH,
)
from libreprimus.source_delta_audit.summary import summarize_records
from libreprimus.source_delta_audit.validation import validate_source_delta_records

source_delta_audit_app = typer.Typer(no_args_is_help=True)
console = Console()


@source_delta_audit_app.command("run")
def source_delta_audit_run(
    repo_url: str = typer.Option(DEFAULT_REPO_URL, "--repo-url", help="Git repository URL or local git repository path."),
    cache_dir: Path = typer.Option(DEFAULT_CACHE_DIR, "--cache-dir", help="Ignored local cache for temporary metadata inspection."),
    out_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated Stage 4E output directory."),
    source_delta_out: Path = typer.Option(DEFAULT_SOURCE_DELTA, "--source-delta-out", help="Committed source-delta record YAML."),
    source_health_out: Path = typer.Option(DEFAULT_SOURCE_HEALTH, "--source-health-out", help="Committed source-health record YAML."),
    image_artifact_out: Path = typer.Option(DEFAULT_IMAGE_ARTIFACT, "--image-artifact-out", help="Committed image artifact observation YAML."),
    manifest_out_dir: Path = typer.Option(DEFAULT_MANIFEST_DIR, "--manifest-out-dir", help="Committed disabled manifest directory."),
    allow_network: bool = typer.Option(False, "--allow-network", help="Allow network Git metadata inspection."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow reduced coverage warnings."),
) -> None:
    """Run the Stage 4E metadata-only source-delta audit."""

    try:
        summary = run_source_delta_audit(
            repo_url=repo_url,
            cache_dir=_resolve(cache_dir),
            out_dir=_resolve(out_dir),
            source_delta_out=_resolve(source_delta_out),
            source_health_out=_resolve(source_health_out),
            image_artifact_out=_resolve(image_artifact_out),
            manifest_out_dir=_resolve(manifest_out_dir),
            allow_network=allow_network,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI surfaces deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@source_delta_audit_app.command("validate")
def source_delta_audit_validate(
    source_delta: Path = typer.Option(DEFAULT_SOURCE_DELTA, "--source-delta", help="Source-delta record YAML."),
    source_health: Path = typer.Option(DEFAULT_SOURCE_HEALTH, "--source-health", help="Source-health record YAML."),
    image_artifact: Path = typer.Option(DEFAULT_IMAGE_ARTIFACT, "--image-artifact", help="Image artifact observation YAML."),
    manifest_dir: Path = typer.Option(DEFAULT_MANIFEST_DIR, "--manifest-dir", help="Disabled manifest directory."),
) -> None:
    """Validate Stage 4E source-delta records."""

    counts, errors = validate_source_delta_records(
        source_delta=_resolve(source_delta),
        source_health=_resolve(source_health),
        image_artifact=_resolve(image_artifact),
        manifest_dir=_resolve(manifest_dir),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("source_delta_audit_valid=true")


@source_delta_audit_app.command("summary")
def source_delta_audit_summary(
    source_delta: Path = typer.Option(DEFAULT_SOURCE_DELTA, "--source-delta", help="Source-delta record YAML."),
    source_health: Path = typer.Option(DEFAULT_SOURCE_HEALTH, "--source-health", help="Source-health record YAML."),
    image_artifact: Path = typer.Option(DEFAULT_IMAGE_ARTIFACT, "--image-artifact", help="Image artifact observation YAML."),
    manifest_dir: Path = typer.Option(DEFAULT_MANIFEST_DIR, "--manifest-dir", help="Disabled manifest directory."),
) -> None:
    """Print a concise Stage 4E source-delta summary."""

    _print_summary(
        summarize_records(
            source_delta=_resolve(source_delta),
            source_health=_resolve(source_health),
            image_artifact=_resolve(image_artifact),
            manifest_dir=_resolve(manifest_dir),
        )
    )


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if key == "category_counts" and isinstance(value, dict):
            for category, count in value.items():
                console.print(f"category_{category}={count}")
            continue
        if key == "output_paths" and isinstance(value, dict):
            for output_name, output_path in value.items():
                console.print(f"{output_name}={output_path}")
            continue
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(source_delta_audit_app, name="source-delta-audit")
