"""Stage 4F stego/audio fixture source-lock CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.paths import repo_root
from libreprimus.stego_fixtures.export import build_stego_fixture_records
from libreprimus.stego_fixtures.models import (
    DEFAULT_AUDIO_FIXTURES,
    DEFAULT_MANIFEST_DIR,
    DEFAULT_OUTGUESS_FIXTURES,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SOURCE_HEALTH,
    DEFAULT_STAGE4B_SOURCES,
    DEFAULT_STAGE4E_SOURCE_DELTA,
    DEFAULT_STAGE4E_SOURCE_HEALTH,
    DEFAULT_TOOLCHAIN,
)
from libreprimus.stego_fixtures.summary import summarize_records
from libreprimus.stego_fixtures.validation import validate_stego_fixture_records

stego_fixtures_app = typer.Typer(no_args_is_help=True)
console = Console()


@stego_fixtures_app.command("build")
def stego_fixtures_build(
    stage4e_source_delta: Path = typer.Option(DEFAULT_STAGE4E_SOURCE_DELTA, "--stage4e-source-delta", help="Stage 4E source-delta record YAML."),
    stage4e_source_health: Path = typer.Option(DEFAULT_STAGE4E_SOURCE_HEALTH, "--stage4e-source-health", help="Stage 4E source-health record YAML."),
    stage4b_sources: Path = typer.Option(DEFAULT_STAGE4B_SOURCES, "--stage4b-sources", help="Stage 4B promoted public source records."),
    out_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated Stage 4F output directory."),
    outguess_fixtures_out: Path = typer.Option(DEFAULT_OUTGUESS_FIXTURES, "--outguess-fixtures-out", help="Committed OutGuess fixture source records."),
    audio_fixtures_out: Path = typer.Option(DEFAULT_AUDIO_FIXTURES, "--audio-fixtures-out", help="Committed audio fixture source records."),
    source_health_out: Path = typer.Option(DEFAULT_SOURCE_HEALTH, "--source-health-out", help="Committed fixture source-health records."),
    toolchain_out: Path = typer.Option(DEFAULT_TOOLCHAIN, "--toolchain-out", help="Committed toolchain requirement records."),
    manifest_out_dir: Path = typer.Option(DEFAULT_MANIFEST_DIR, "--manifest-out-dir", help="Committed disabled manifest directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow reduced coverage warnings."),
) -> None:
    """Build Stage 4F fixture source-lock metadata."""

    try:
        summary = build_stego_fixture_records(
            stage4e_source_delta=_resolve(stage4e_source_delta),
            stage4e_source_health=_resolve(stage4e_source_health),
            stage4b_sources=_resolve(stage4b_sources),
            out_dir=_resolve(out_dir),
            outguess_fixtures_out=_resolve(outguess_fixtures_out),
            audio_fixtures_out=_resolve(audio_fixtures_out),
            source_health_out=_resolve(source_health_out),
            toolchain_out=_resolve(toolchain_out),
            manifest_out_dir=_resolve(manifest_out_dir),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI surfaces deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@stego_fixtures_app.command("validate")
def stego_fixtures_validate(
    outguess_fixtures: Path = typer.Option(DEFAULT_OUTGUESS_FIXTURES, "--outguess-fixtures", help="OutGuess fixture source records."),
    audio_fixtures: Path = typer.Option(DEFAULT_AUDIO_FIXTURES, "--audio-fixtures", help="Audio fixture source records."),
    source_health: Path = typer.Option(DEFAULT_SOURCE_HEALTH, "--source-health", help="Fixture source-health records."),
    toolchain: Path = typer.Option(DEFAULT_TOOLCHAIN, "--toolchain", help="Toolchain requirement records."),
    manifest_dir: Path = typer.Option(DEFAULT_MANIFEST_DIR, "--manifest-dir", help="Disabled manifest directory."),
) -> None:
    """Validate Stage 4F fixture records."""

    counts, errors = validate_stego_fixture_records(
        outguess_fixtures=_resolve(outguess_fixtures),
        audio_fixtures=_resolve(audio_fixtures),
        source_health=_resolve(source_health),
        toolchain=_resolve(toolchain),
        manifest_dir=_resolve(manifest_dir),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("stego_fixtures_valid=true")


@stego_fixtures_app.command("summary")
def stego_fixtures_summary(
    outguess_fixtures: Path = typer.Option(DEFAULT_OUTGUESS_FIXTURES, "--outguess-fixtures", help="OutGuess fixture source records."),
    audio_fixtures: Path = typer.Option(DEFAULT_AUDIO_FIXTURES, "--audio-fixtures", help="Audio fixture source records."),
    source_health: Path = typer.Option(DEFAULT_SOURCE_HEALTH, "--source-health", help="Fixture source-health records."),
    toolchain: Path = typer.Option(DEFAULT_TOOLCHAIN, "--toolchain", help="Toolchain requirement records."),
    manifest_dir: Path = typer.Option(DEFAULT_MANIFEST_DIR, "--manifest-dir", help="Disabled manifest directory."),
) -> None:
    """Print a concise Stage 4F fixture summary."""

    _print_summary(
        summarize_records(
            outguess_fixtures=_resolve(outguess_fixtures),
            audio_fixtures=_resolve(audio_fixtures),
            source_health=_resolve(source_health),
            toolchain=_resolve(toolchain),
            manifest_dir=_resolve(manifest_dir),
        )
    )


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if key == "local_availability_counts" and isinstance(value, dict):
            for name, count in value.items():
                console.print(f"local_availability_{name}_count={count}")
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

    root_app.add_typer(stego_fixtures_app, name="stego-fixtures")
