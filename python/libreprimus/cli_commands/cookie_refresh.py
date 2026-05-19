"""Stage 4G cookie exact-candidate refresh CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cookie_refresh.export import run_cookie_refresh
from libreprimus.cookie_refresh.models import (
    DEFAULT_CANDIDATE_SOURCES,
    DEFAULT_COOKIE_TARGETS,
    DEFAULT_MANIFEST,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SUMMARY,
)
from libreprimus.cookie_refresh.summary import load_summary
from libreprimus.cookie_refresh.validation import validate_cookie_refresh_results
from libreprimus.paths import repo_root

cookie_refresh_app = typer.Typer(no_args_is_help=True)
console = Console()


@cookie_refresh_app.command("run")
def cookie_refresh_run(
    manifest: Path = typer.Option(DEFAULT_MANIFEST, "--manifest", help="Stage 4B cookie pack v2 manifest."),
    candidate_sources: Path = typer.Option(DEFAULT_CANDIDATE_SOURCES, "--candidate-sources", help="Stage 4B cookie source records."),
    cookie_targets: Path = typer.Option(DEFAULT_COOKIE_TARGETS, "--cookie-targets", help="Historical cookie target records."),
    out_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated Stage 4G output directory."),
    summary_out: Path = typer.Option(DEFAULT_SUMMARY, "--summary-out", help="Committed aggregate summary path."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow reduced-coverage warnings."),
) -> None:
    """Run the bounded exact cookie candidate refresh."""

    try:
        summary = run_cookie_refresh(
            manifest=_resolve(manifest),
            candidate_sources=_resolve(candidate_sources),
            cookie_targets=_resolve(cookie_targets),
            out_dir=_resolve(out_dir),
            summary_out=_resolve(summary_out),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports deterministic validation failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@cookie_refresh_app.command("validate")
def cookie_refresh_validate(
    results_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--results-dir", help="Generated Stage 4G output directory."),
    summary: Path = typer.Option(DEFAULT_SUMMARY, "--summary", help="Committed aggregate summary path."),
) -> None:
    """Validate generated and committed Stage 4G cookie refresh records."""

    try:
        counts, errors = validate_cookie_refresh_results(results_dir=_resolve(results_dir), summary=_resolve(summary))
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
    console.print("cookie_refresh_valid=true")


@cookie_refresh_app.command("summary")
def cookie_refresh_summary(
    summary: Path = typer.Option(DEFAULT_SUMMARY, "--summary", help="Committed aggregate summary path."),
) -> None:
    """Print a concise Stage 4G cookie refresh summary."""

    _print_summary(load_summary(_resolve(summary)))


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if key == "output_paths":
            continue
        if isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
            continue
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(cookie_refresh_app, name="cookie-refresh")
