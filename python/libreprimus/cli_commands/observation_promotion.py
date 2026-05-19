"""Stage 4L observation-promotion CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.observation_promotion.export import build_observation_promotion
from libreprimus.observation_promotion.models import (
    DEFAULT_BLOCKERS_OUT,
    DEFAULT_LEDGER_OUT,
    DEFAULT_MANIFEST_READINESS_OUT,
    DEFAULT_OUT_DIR,
    DEFAULT_READINESS_OUT,
    DEFAULT_SUMMARY_OUT,
)
from libreprimus.observation_promotion.summary import load_summary
from libreprimus.observation_promotion.validation import validate_observation_promotion_records
from libreprimus.paths import repo_root

observation_promotion_app = typer.Typer(no_args_is_help=True)
console = Console()


@observation_promotion_app.command("build")
def observation_promotion_build(
    out_dir: Path = typer.Option(DEFAULT_OUT_DIR, "--out-dir", help="Generated report output directory."),
    ledger_out: Path = typer.Option(DEFAULT_LEDGER_OUT, "--ledger-out", help="Committed promotion ledger YAML."),
    readiness_out: Path = typer.Option(
        DEFAULT_READINESS_OUT,
        "--readiness-out",
        help="Committed observation readiness YAML.",
    ),
    blockers_out: Path = typer.Option(
        DEFAULT_BLOCKERS_OUT,
        "--blockers-out",
        help="Committed promotion blocker YAML.",
    ),
    manifest_readiness_out: Path = typer.Option(
        DEFAULT_MANIFEST_READINESS_OUT,
        "--manifest-readiness-out",
        help="Committed manifest readiness YAML.",
    ),
    summary_out: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary-out", help="Committed summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Record warnings without failing build."),
) -> None:
    """Build Stage 4L reviewed observation promotion records."""

    try:
        summary = build_observation_promotion(
            out_dir=_resolve(out_dir),
            ledger_out=_resolve(ledger_out),
            readiness_out=_resolve(readiness_out),
            blockers_out=_resolve(blockers_out),
            manifest_readiness_out=_resolve(manifest_readiness_out),
            summary_out=_resolve(summary_out),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI should surface deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@observation_promotion_app.command("validate")
def observation_promotion_validate(
    ledger: Path = typer.Option(DEFAULT_LEDGER_OUT, "--ledger", help="Promotion ledger YAML."),
    readiness: Path = typer.Option(DEFAULT_READINESS_OUT, "--readiness", help="Readiness records YAML."),
    blockers: Path = typer.Option(DEFAULT_BLOCKERS_OUT, "--blockers", help="Blocker records YAML."),
    manifest_readiness: Path = typer.Option(
        DEFAULT_MANIFEST_READINESS_OUT,
        "--manifest-readiness",
        help="Manifest readiness records YAML.",
    ),
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Promotion summary YAML."),
) -> None:
    """Validate Stage 4L reviewed observation promotion records."""

    counts, errors = validate_observation_promotion_records(
        ledger=_resolve(ledger),
        readiness=_resolve(readiness),
        blockers=_resolve(blockers),
        manifest_readiness=_resolve(manifest_readiness),
        summary=_resolve(summary),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("observation_promotion_valid=true")


@observation_promotion_app.command("summary")
def observation_promotion_summary(
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Promotion summary YAML."),
) -> None:
    """Print the committed Stage 4L promotion summary."""

    _print_summary(load_summary(_resolve(summary)))


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if isinstance(value, dict):
            continue
        if isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
            continue
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register observation-promotion commands on the public root app."""

    root_app.add_typer(observation_promotion_app, name="observation-promotion")
