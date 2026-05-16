"""Command-line interface for Stage 0A smoke validation."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from libreprimus.legacy_workbook.export import extract_workbook, write_extraction, write_json
from libreprimus.legacy_workbook.paths import default_output_dir, resolve_workbook_path
from libreprimus.paths import package_root, repo_root
from libreprimus.toolchain import ToolStatus, collect_toolchain

app = typer.Typer(no_args_is_help=True)
legacy_workbook_app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def smoke() -> None:
    """Print the Stage 0A Python smoke message."""
    console.print("LiberPrimus Python Stage 0A smoke OK")


@app.command()
def paths() -> None:
    """Print important project paths."""
    table = Table("Name", "Path")
    table.add_row("repo_root", str(repo_root()))
    table.add_row("package_root", str(package_root()))
    console.print(table)


@app.command()
def toolchain() -> None:
    """Print a concise toolchain report."""
    table = Table("Tool", "Present", "Path", "Version")
    report = collect_toolchain()
    for name, status in report.items():
        if isinstance(status, ToolStatus):
            table.add_row(name, str(status.present).lower(), status.path or "", status.version or "")
        else:
            table.add_row(name, "true" if status else "false", status or "", "")
    console.print(table)


def _load_extraction_or_exit(workbook: Path | None):
    try:
        workbook_path = resolve_workbook_path(workbook)
        return workbook_path, extract_workbook(workbook_path)
    except FileNotFoundError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(2) from error


@legacy_workbook_app.command()
def summary(
    workbook: Path | None = typer.Option(
        None,
        "--workbook",
        help="Workbook path. Defaults to data/raw/legacy-workbooks/tranlsations.xlsx then root tranlsations.xlsx.",
    ),
) -> None:
    """Print a concise legacy workbook extraction summary."""
    workbook_path, extraction = _load_extraction_or_exit(workbook)
    summary_record = extraction.summary

    table = Table("Metric", "Value")
    table.add_row("workbook", str(workbook_path))
    table.add_row("sha256", summary_record.workbook_sha256)
    table.add_row("sheet_count", str(summary_record.sheet_count))
    table.add_row("delta_records", str(summary_record.total_delta_records))
    table.add_row("prime_sum_records", str(summary_record.total_prime_sum_records))
    table.add_row("formula_records", str(summary_record.total_formula_records))
    table.add_row("warning_count", str(len(extraction.warning_records)))
    table.add_row("canonical_corpus_allowed", str(summary_record.canonical_corpus_allowed).lower())
    table.add_row("trusted_as_canonical", str(summary_record.trusted_as_canonical).lower())
    console.print(table)


@legacy_workbook_app.command()
def inventory(
    workbook: Path | None = typer.Option(None, "--workbook", help="Workbook path."),
    out: Path | None = typer.Option(None, "--out", help="Output JSON path."),
) -> None:
    """Write sheet inventory JSON."""
    _, extraction = _load_extraction_or_exit(workbook)
    out_path = out if out is not None else default_output_dir() / "sheet_inventory.json"
    if not out_path.is_absolute():
        out_path = repo_root() / out_path
    write_json(out_path, extraction.sheet_records)
    console.print(f"sheet_inventory={out_path}")
    console.print(f"sheet_count={len(extraction.sheet_records)}")


@legacy_workbook_app.command()
def extract(
    workbook: Path | None = typer.Option(None, "--workbook", help="Workbook path."),
    out_dir: Path = typer.Option(default_output_dir(), "--out-dir", help="Generated output directory."),
) -> None:
    """Extract generated legacy workbook records to an ignored output directory."""
    _, extraction = _load_extraction_or_exit(workbook)
    output_dir = out_dir if out_dir.is_absolute() else repo_root() / out_dir
    paths = write_extraction(output_dir, extraction)

    table = Table("Output", "Path")
    for name, path in paths.items():
        table.add_row(name, str(path))
    console.print(table)
    console.print(f"sheet_count={extraction.summary.sheet_count}")
    console.print(f"delta_record_count={extraction.summary.total_delta_records}")
    console.print(f"prime_sum_record_count={extraction.summary.total_prime_sum_records}")
    console.print(f"formula_record_count={extraction.summary.total_formula_records}")
    console.print(f"warning_count={len(extraction.warning_records)}")


@legacy_workbook_app.command()
def validate(
    workbook: Path | None = typer.Option(None, "--workbook", help="Workbook path."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Validate workbook extraction invariants."""
    _, extraction = _load_extraction_or_exit(workbook)
    warning_count = len(extraction.warning_records)
    console.print(f"canonical_corpus_allowed={str(extraction.summary.canonical_corpus_allowed).lower()}")
    console.print(f"trusted_as_canonical={str(extraction.summary.trusted_as_canonical).lower()}")
    console.print(f"warning_count={warning_count}")
    if warning_count and not allow_warnings:
        console.print("[red]Legacy workbook validation produced warnings.[/red]")
        raise typer.Exit(1)
    console.print("Legacy workbook validation OK")


app.add_typer(legacy_workbook_app, name="legacy-workbook")


if __name__ == "__main__":
    app()
