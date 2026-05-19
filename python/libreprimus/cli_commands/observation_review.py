"""Stage 4J observation-review CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.observation_review.export import build_observation_review
from libreprimus.observation_review.models import (
    DEFAULT_DECISIONS_OUT,
    DEFAULT_OUT_DIR,
    DEFAULT_POLICY_OUT,
    DEFAULT_PROMOTIONS_OUT,
    DEFAULT_QUARANTINE_OUT,
    DEFAULT_SUMMARY_OUT,
)
from libreprimus.observation_review.summary import load_summary
from libreprimus.observation_review.validation import (
    validate_observation_review_records,
    validate_path_sanitisation,
)
from libreprimus.paths import repo_root

observation_review_app = typer.Typer(no_args_is_help=True)
console = Console()


@observation_review_app.command("build")
def observation_review_build(
    out_dir: Path = typer.Option(DEFAULT_OUT_DIR, "--out-dir", help="Generated report output directory."),
    policy_out: Path = typer.Option(DEFAULT_POLICY_OUT, "--policy-out", help="Committed policy YAML."),
    decisions_out: Path = typer.Option(DEFAULT_DECISIONS_OUT, "--decisions-out", help="Committed decisions YAML."),
    promotions_out: Path = typer.Option(DEFAULT_PROMOTIONS_OUT, "--promotions-out", help="Committed promotions YAML."),
    quarantine_out: Path = typer.Option(DEFAULT_QUARANTINE_OUT, "--quarantine-out", help="Committed quarantine YAML."),
    summary_out: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary-out", help="Committed summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow path/stale-doc warnings during build."),
) -> None:
    """Build Stage 4J observation-review records from committed metadata."""

    try:
        summary = build_observation_review(
            out_dir=_resolve(out_dir),
            policy_out=_resolve(policy_out),
            decisions_out=_resolve(decisions_out),
            promotions_out=_resolve(promotions_out),
            quarantine_out=_resolve(quarantine_out),
            summary_out=_resolve(summary_out),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI surfaces deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@observation_review_app.command("validate")
def observation_review_validate(
    policy: Path = typer.Option(DEFAULT_POLICY_OUT, "--policy", help="Policy YAML."),
    decisions: Path = typer.Option(DEFAULT_DECISIONS_OUT, "--decisions", help="Decisions YAML."),
    promotions: Path = typer.Option(DEFAULT_PROMOTIONS_OUT, "--promotions", help="Promotions YAML."),
    quarantine: Path = typer.Option(DEFAULT_QUARANTINE_OUT, "--quarantine", help="Quarantine YAML."),
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Summary YAML."),
) -> None:
    """Validate committed Stage 4J observation-review records."""

    counts, errors = validate_observation_review_records(
        policy=_resolve(policy),
        decisions=_resolve(decisions),
        promotions=_resolve(promotions),
        quarantine=_resolve(quarantine),
        summary=_resolve(summary),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("observation_review_valid=true")


@observation_review_app.command("summary")
def observation_review_summary(
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Summary YAML."),
) -> None:
    """Print the committed Stage 4J observation-review summary."""

    _print_summary(load_summary(_resolve(summary)))


@observation_review_app.command("check-paths")
def observation_review_check_paths(
    repo_root_path: Path = typer.Option(Path("."), "--repo-root", help="Repository root to scan."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Print findings without failing."),
) -> None:
    """Check committed operational docs/records for local paths and stale state text."""

    root = repo_root_path.resolve() if repo_root_path.is_absolute() else (repo_root() / repo_root_path).resolve()
    counts, errors = validate_path_sanitisation(root)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors and not allow_warnings:
        raise typer.Exit(1)
    console.print("path_sanitisation_valid=true")


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
            continue
        if isinstance(value, dict):
            continue
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register observation-review commands on the public root app."""

    root_app.add_typer(observation_review_app, name="observation-review")
