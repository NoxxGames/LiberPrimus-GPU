"""Transcript source CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

transcript_source_app = typer.Typer(no_args_is_help=True)


def _resolve_existing_path(path: Path, label: str) -> Path:
    resolved = path if path.is_absolute() else repo_root() / path
    if not resolved.is_file():
        console.print(f"[red]{label} not found: {resolved}[/red]")
        raise typer.Exit(2)
    return resolved


def _resolve_output_path(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


@transcript_source_app.command("summary")
def transcript_source_summary(
    source: str = typer.Option(..., "--source", help="Transcript source: rtkd-master or scream314."),
    input_path: Path = typer.Option(..., "--input", help="Raw transcript/reference path."),
) -> None:
    """Print a transcript-source summary."""
    resolved = _resolve_existing_path(input_path, "Transcript source")
    if source == "rtkd-master":
        _, source_summary = parse_rtkd_master(resolved)
        table = Table("Metric", "Value")
        table.add_row("source", source)
        table.add_row("input", str(resolved))
        table.add_row("sha256", source_summary.source_sha256)
        table.add_row("physical_line_count", str(source_summary.physical_line_count))
        table.add_row("rune_line_count", str(source_summary.rune_line_count))
        table.add_row("rune_count", str(source_summary.rune_count))
        table.add_row("page_marker_count", str(source_summary.page_marker_count))
        table.add_row("parse_warning_count", str(source_summary.parse_warning_count))
        table.add_row("canonical_corpus_active", str(source_summary.canonical_corpus_active).lower())
        console.print(table)
        return
    if source == "scream314":
        _, source_summary = parse_scream314_reference(resolved)
        table = Table("Metric", "Value")
        table.add_row("source", source)
        table.add_row("input", str(resolved))
        table.add_row("sha256", source_summary.source_sha256)
        table.add_row("physical_line_count", str(source_summary.physical_line_count))
        table.add_row("reference_record_count", str(source_summary.reference_record_count))
        table.add_row("page_label_count", str(source_summary.page_label_count))
        table.add_row("lp2_page_count_statement", source_summary.lp2_page_count_statement or "")
        table.add_row("canonical_corpus_active", str(source_summary.canonical_corpus_active).lower())
        console.print(table)
        return
    console.print("[red]Unsupported transcript source. Use rtkd-master or scream314.[/red]")
    raise typer.Exit(2)


@transcript_source_app.command("inventory")
def transcript_source_inventory(
    source: str = typer.Option(..., "--source", help="Transcript source. Stage 0D supports rtkd-master."),
    input_path: Path = typer.Option(..., "--input", help="Raw transcript path."),
    out: Path = typer.Option(..., "--out", help="Generated transcript-line JSONL path."),
) -> None:
    """Write transcript-line inventory JSONL."""
    if source != "rtkd-master":
        console.print("[red]Inventory currently supports --source rtkd-master only.[/red]")
        raise typer.Exit(2)
    resolved = _resolve_existing_path(input_path, "Transcript source")
    output_path = _resolve_output_path(out)
    records, source_summary = parse_rtkd_master(resolved)
    write_transcript_jsonl(output_path, records)
    console.print(f"transcript_lines={output_path}")
    console.print(f"physical_line_count={source_summary.physical_line_count}")
    console.print(f"rune_line_count={source_summary.rune_line_count}")
    console.print(f"parse_warning_count={source_summary.parse_warning_count}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(transcript_source_app, name="transcript-source")
