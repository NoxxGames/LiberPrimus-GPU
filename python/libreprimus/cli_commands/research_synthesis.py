"""Research-synthesis CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from libreprimus.research_synthesis.loader import load_all_record_sets
from libreprimus.research_synthesis.models import DEFAULT_DATA_DIR, DEFAULT_STAGED_PLAN
from libreprimus.research_synthesis.summary import build_summary
from libreprimus.research_synthesis.validation import validate_research_synthesis

research_synthesis_app = typer.Typer(no_args_is_help=True)
console = Console()


@research_synthesis_app.command("validate")
def research_synthesis_validate(
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Research synthesis data directory."),
    staged_plan: Path = typer.Option(DEFAULT_STAGED_PLAN, "--staged-plan", help="Durable staged plan document."),
) -> None:
    """Validate Stage 3Y research-synthesis records and staged plan."""

    summary, errors = validate_research_synthesis(data_dir=data_dir, staged_plan=staged_plan)
    _print_summary(summary)
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("research_synthesis_valid=true")


@research_synthesis_app.command("summary")
def research_synthesis_summary(
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Research synthesis data directory."),
) -> None:
    """Print a concise Stage 3Y research-synthesis summary."""

    _print_summary(build_summary(data_dir=data_dir))


@research_synthesis_app.command("check-retirement")
def research_synthesis_check_retirement(
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data-dir", help="Research synthesis data directory."),
    method_family: str = typer.Option(..., "--method-family", help="Method family id to inspect."),
) -> None:
    """Print method-family and retirement status for one family."""

    records = load_all_record_sets(data_dir)
    method = next(
        (
            record
            for record in records["method_families"]
            if record.get("method_family_id") == method_family
        ),
        None,
    )
    if method is None:
        console.print(f"[red]method_family_not_found={method_family}[/red]")
        raise typer.Exit(1)

    retirement = next(
        (
            record
            for record in records["method_retirements"]
            if record.get("method_family_id") == method_family
        ),
        None,
    )
    console.print(f"method_family_id={method_family}")
    console.print(f"name={method.get('name')}")
    console.print(f"status={method.get('status')}")
    console.print(f"next_action={method.get('next_action')}")
    console.print(f"reopen_conditions={'; '.join(str(item) for item in method.get('reopen_conditions', []))}")
    console.print(f"stop_conditions={'; '.join(str(item) for item in method.get('stop_conditions', []))}")
    if retirement is None:
        console.print("retirement_record=false")
        return
    console.print("retirement_record=true")
    console.print(f"retired_status={retirement.get('retired_status')}")
    console.print(f"reason={retirement.get('reason')}")
    console.print(
        "prohibited_expansions="
        + "; ".join(str(item) for item in retirement.get("prohibited_expansions", []))
    )


def _print_summary(payload: dict) -> None:
    for key in [
        "data_dir",
        "staged_plan",
        "stage_summary_count",
        "method_family_count",
        "retirement_count",
        "deep_research_influence_count",
        "direction_change_count",
    ]:
        if key in payload:
            console.print(f"{key}={payload[key]}")

    record_counts = payload.get("record_counts")
    if isinstance(record_counts, dict):
        table = Table("record_set", "count")
        for key, value in sorted(record_counts.items()):
            table.add_row(key, str(value))
        console.print(table)

    method_status_counts = payload.get("method_status_counts")
    if isinstance(method_status_counts, dict):
        table = Table("method_status", "count")
        for key, value in sorted(method_status_counts.items()):
            table.add_row(key, str(value))
        console.print(table)

    retirement_status_counts = payload.get("retirement_status_counts")
    if isinstance(retirement_status_counts, dict):
        table = Table("retirement_status", "count")
        for key, value in sorted(retirement_status_counts.items()):
            table.add_row(key, str(value))
        console.print(table)


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(research_synthesis_app, name="research-synthesis")
