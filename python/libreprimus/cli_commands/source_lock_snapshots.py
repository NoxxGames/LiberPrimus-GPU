"""Stage 4K source-lock snapshot CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.paths import repo_root
from libreprimus.source_lock_snapshots.allowlist import (
    ALLOWLISTED_DOMAINS,
    REJECTED_DOMAIN_FRAGMENTS,
)
from libreprimus.source_lock_snapshots.export import build_source_lock_snapshots
from libreprimus.source_lock_snapshots.models import (
    DEFAULT_CACHE_DIR,
    DEFAULT_COPYRIGHT_RECORDS_OUT,
    DEFAULT_FETCH_RECORDS_OUT,
    DEFAULT_OUT_DIR,
    DEFAULT_SNAPSHOT_RECORDS_OUT,
    DEFAULT_SUMMARY_OUT,
)
from libreprimus.source_lock_snapshots.summary import load_summary
from libreprimus.source_lock_snapshots.validation import validate_source_lock_snapshot_records

source_lock_snapshots_app = typer.Typer(no_args_is_help=True)
console = Console()


@source_lock_snapshots_app.command("build")
def source_lock_snapshots_build(
    out_dir: Path = typer.Option(DEFAULT_OUT_DIR, "--out-dir", help="Generated report output directory."),
    cache_dir: Path = typer.Option(DEFAULT_CACHE_DIR, "--cache-dir", help="Ignored local source snapshot cache."),
    snapshot_records_out: Path = typer.Option(
        DEFAULT_SNAPSHOT_RECORDS_OUT,
        "--snapshot-records-out",
        help="Committed source-lock snapshot records YAML.",
    ),
    fetch_records_out: Path = typer.Option(
        DEFAULT_FETCH_RECORDS_OUT,
        "--fetch-records-out",
        help="Committed source fetch records YAML.",
    ),
    copyright_records_out: Path = typer.Option(
        DEFAULT_COPYRIGHT_RECORDS_OUT,
        "--copyright-records-out",
        help="Committed source copyright policy records YAML.",
    ),
    summary_out: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary-out", help="Committed source-lock summary YAML."),
    allow_network: bool = typer.Option(False, "--allow-network", help="Permit allowlisted public-source network fetches."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Record warnings without failing the build."),
) -> None:
    """Build Stage 4K allowlisted public source-lock snapshot records."""

    try:
        summary = build_source_lock_snapshots(
            out_dir=_resolve(out_dir),
            cache_dir=_resolve(cache_dir),
            snapshot_records_out=_resolve(snapshot_records_out),
            fetch_records_out=_resolve(fetch_records_out),
            copyright_records_out=_resolve(copyright_records_out),
            summary_out=_resolve(summary_out),
            allow_network=allow_network,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI should surface deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@source_lock_snapshots_app.command("validate")
def source_lock_snapshots_validate(
    snapshot_records: Path = typer.Option(
        DEFAULT_SNAPSHOT_RECORDS_OUT,
        "--snapshot-records",
        help="Source-lock snapshot records YAML.",
    ),
    fetch_records: Path = typer.Option(DEFAULT_FETCH_RECORDS_OUT, "--fetch-records", help="Source fetch records YAML."),
    copyright_records: Path = typer.Option(
        DEFAULT_COPYRIGHT_RECORDS_OUT,
        "--copyright-records",
        help="Source copyright policy records YAML.",
    ),
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Source-lock summary YAML."),
) -> None:
    """Validate committed Stage 4K source-lock snapshot records."""

    counts, errors = validate_source_lock_snapshot_records(
        snapshot_records=_resolve(snapshot_records),
        fetch_records=_resolve(fetch_records),
        copyright_records=_resolve(copyright_records),
        summary=_resolve(summary),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("source_lock_snapshots_valid=true")


@source_lock_snapshots_app.command("summary")
def source_lock_snapshots_summary(
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Source-lock summary YAML."),
) -> None:
    """Print the committed Stage 4K source-lock summary."""

    _print_summary(load_summary(_resolve(summary)))


@source_lock_snapshots_app.command("list-allowlist")
def source_lock_snapshots_list_allowlist() -> None:
    """Print allowlisted and rejected source domains."""

    for domain in ALLOWLISTED_DOMAINS:
        console.print(f"allowlisted_domain={domain}")
    for domain in REJECTED_DOMAIN_FRAGMENTS:
        console.print(f"rejected_domain_fragment={domain}")


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
    """Register source-lock snapshot commands on the public root app."""

    root_app.add_typer(source_lock_snapshots_app, name="source-lock-snapshots")
