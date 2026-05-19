"""Stage 4N stego/audio positive-control readiness CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.paths import repo_root
from libreprimus.stego_positive_controls.export import build_stego_positive_controls
from libreprimus.stego_positive_controls.models import (
    DEFAULT_AUDIO_READINESS_OUT,
    DEFAULT_AUDIO_SOURCES,
    DEFAULT_CACHE_DIR,
    DEFAULT_EXPECTED_OUTPUT_OUT,
    DEFAULT_FIXTURE_CACHE_OUT,
    DEFAULT_MANIFEST_READINESS,
    DEFAULT_OUT_DIR,
    DEFAULT_OUTGUESS_ARTIFACTS,
    DEFAULT_OUTGUESS_READINESS_OUT,
    DEFAULT_OUTGUESS_SOURCES,
    DEFAULT_SOURCE_FETCHES,
    DEFAULT_SOURCE_HEALTH,
    DEFAULT_SOURCE_LOCKS,
    DEFAULT_SOURCE_LOCK_SUMMARY,
    DEFAULT_SUMMARY_OUT,
    DEFAULT_TOOLCHAIN_OUT,
    DEFAULT_TOOLCHAIN_REQUIREMENTS,
)
from libreprimus.stego_positive_controls.summary import load_summary
from libreprimus.stego_positive_controls.validation import validate_stego_positive_control_records

stego_positive_controls_app = typer.Typer(no_args_is_help=True)
console = Console()


@stego_positive_controls_app.command("build")
def stego_positive_controls_build(
    out_dir: Path = typer.Option(DEFAULT_OUT_DIR, "--out-dir", help="Generated Stage 4N report directory."),
    cache_dir: Path = typer.Option(DEFAULT_CACHE_DIR, "--cache-dir", help="Ignored local fixture cache directory."),
    outguess_sources: Path = typer.Option(
        DEFAULT_OUTGUESS_SOURCES,
        "--outguess-sources",
        help="Stage 4F OutGuess fixture source records.",
    ),
    audio_sources: Path = typer.Option(DEFAULT_AUDIO_SOURCES, "--audio-sources", help="Stage 4F audio source records."),
    source_health: Path = typer.Option(DEFAULT_SOURCE_HEALTH, "--source-health", help="Stage 4F source-health records."),
    toolchain_requirements: Path = typer.Option(
        DEFAULT_TOOLCHAIN_REQUIREMENTS,
        "--toolchain-requirements",
        help="Stage 4F toolchain requirement records.",
    ),
    source_locks: Path = typer.Option(DEFAULT_SOURCE_LOCKS, "--source-locks", help="Stage 4K source-lock records."),
    source_fetches: Path = typer.Option(DEFAULT_SOURCE_FETCHES, "--source-fetches", help="Stage 4K fetch records."),
    source_lock_summary: Path = typer.Option(
        DEFAULT_SOURCE_LOCK_SUMMARY,
        "--source-lock-summary",
        help="Stage 4K source-lock summary.",
    ),
    outguess_artifacts: Path = typer.Option(
        DEFAULT_OUTGUESS_ARTIFACTS,
        "--outguess-artifacts",
        help="Stage 3V OutGuess artifact records.",
    ),
    manifest_readiness: Path = typer.Option(
        DEFAULT_MANIFEST_READINESS,
        "--manifest-readiness",
        help="Stage 4L manifest readiness records.",
    ),
    outguess_readiness_out: Path = typer.Option(
        DEFAULT_OUTGUESS_READINESS_OUT,
        "--outguess-readiness-out",
        help="Committed OutGuess readiness YAML.",
    ),
    audio_readiness_out: Path = typer.Option(
        DEFAULT_AUDIO_READINESS_OUT,
        "--audio-readiness-out",
        help="Committed audio readiness YAML.",
    ),
    fixture_cache_out: Path = typer.Option(
        DEFAULT_FIXTURE_CACHE_OUT,
        "--fixture-cache-out",
        help="Committed fixture-cache records YAML.",
    ),
    expected_output_out: Path = typer.Option(
        DEFAULT_EXPECTED_OUTPUT_OUT,
        "--expected-output-out",
        help="Committed expected-output records YAML.",
    ),
    toolchain_out: Path = typer.Option(
        DEFAULT_TOOLCHAIN_OUT,
        "--toolchain-out",
        help="Committed toolchain readiness YAML.",
    ),
    summary_out: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary-out", help="Committed Stage 4N summary YAML."),
    allow_network: bool = typer.Option(False, "--allow-network", help="Reserved; default build performs no fetches."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Record warnings without failing build."),
) -> None:
    """Build Stage 4N stego/audio positive-control readiness records."""

    try:
        summary = build_stego_positive_controls(
            out_dir=_resolve(out_dir),
            cache_dir=_resolve(cache_dir),
            outguess_sources=_resolve(outguess_sources),
            audio_sources=_resolve(audio_sources),
            source_health=_resolve(source_health),
            toolchain_requirements=_resolve(toolchain_requirements),
            source_locks=_resolve(source_locks),
            source_fetches=_resolve(source_fetches),
            source_lock_summary=_resolve(source_lock_summary),
            outguess_artifacts=_resolve(outguess_artifacts),
            manifest_readiness=_resolve(manifest_readiness),
            outguess_readiness_out=_resolve(outguess_readiness_out),
            audio_readiness_out=_resolve(audio_readiness_out),
            fixture_cache_out=_resolve(fixture_cache_out),
            expected_output_out=_resolve(expected_output_out),
            toolchain_out=_resolve(toolchain_out),
            summary_out=_resolve(summary_out),
            allow_network=allow_network,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI should surface deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@stego_positive_controls_app.command("validate")
def stego_positive_controls_validate(
    outguess_readiness: Path = typer.Option(
        DEFAULT_OUTGUESS_READINESS_OUT,
        "--outguess-readiness",
        help="OutGuess readiness YAML.",
    ),
    audio_readiness: Path = typer.Option(DEFAULT_AUDIO_READINESS_OUT, "--audio-readiness", help="Audio readiness YAML."),
    fixture_cache: Path = typer.Option(DEFAULT_FIXTURE_CACHE_OUT, "--fixture-cache", help="Fixture-cache YAML."),
    expected_output: Path = typer.Option(
        DEFAULT_EXPECTED_OUTPUT_OUT,
        "--expected-output",
        help="Expected-output YAML.",
    ),
    toolchain: Path = typer.Option(DEFAULT_TOOLCHAIN_OUT, "--toolchain", help="Toolchain readiness YAML."),
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Stage 4N summary YAML."),
) -> None:
    """Validate committed Stage 4N stego/audio positive-control records."""

    counts, errors = validate_stego_positive_control_records(
        outguess_readiness=_resolve(outguess_readiness),
        audio_readiness=_resolve(audio_readiness),
        fixture_cache=_resolve(fixture_cache),
        expected_output=_resolve(expected_output),
        toolchain=_resolve(toolchain),
        summary=_resolve(summary),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("stego_positive_controls_valid=true")


@stego_positive_controls_app.command("summary")
def stego_positive_controls_summary(
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Stage 4N summary YAML."),
) -> None:
    """Print the committed Stage 4N summary."""

    _print_summary(load_summary(_resolve(summary)))


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                console.print(f"{key}.{sub_key}={sub_value}")
            continue
        if isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
            continue
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register stego-positive-controls commands on the public root app."""

    root_app.add_typer(stego_positive_controls_app, name="stego-positive-controls")
