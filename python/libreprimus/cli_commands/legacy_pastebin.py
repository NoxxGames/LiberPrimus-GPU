"""Legacy Pastebin CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

legacy_pastebin_app = typer.Typer(no_args_is_help=True)


def _load_pastebin_extraction_or_exit(input_path: Path | None):
    try:
        resolved = resolve_input_path(input_path)
        return resolved, extract_legacy_pastebin(resolved)
    except FileNotFoundError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(2) from error


@legacy_pastebin_app.command("summary")
def pastebin_summary(
    input_path: Path | None = typer.Option(
        None,
        "--input",
        help="Local Pastebin TXT path. Defaults to raw legacy-pastebins path, then root drops.",
    ),
) -> None:
    """Print a concise legacy Pastebin extraction summary."""
    resolved, extraction = _load_pastebin_extraction_or_exit(input_path)
    summary_record = extraction.summary

    table = Table("Metric", "Value")
    table.add_row("input", str(resolved))
    table.add_row("sha256", summary_record.source_sha256)
    table.add_row("line_pair_count", str(summary_record.line_pair_count))
    table.add_row("empty_pair_count", str(summary_record.empty_pair_count))
    table.add_row("validation_warning_count", str(summary_record.validation_warning_count))
    table.add_row("unknown_glyph_count", str(summary_record.unknown_glyph_count))
    table.add_row("unknown_prime_value_count", str(summary_record.unknown_prime_value_count))
    table.add_row("anchor_count", str(len(extraction.anchors)))
    table.add_row("canonical_corpus_allowed", str(summary_record.canonical_corpus_allowed).lower())
    table.add_row("page_boundary_status", summary_record.page_boundary_status)
    console.print(table)


@legacy_pastebin_app.command("validate")
def pastebin_validate(
    input_path: Path | None = typer.Option(None, "--input", help="Local Pastebin TXT path."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Validate local legacy Pastebin line pairs."""
    _, extraction = _load_pastebin_extraction_or_exit(input_path)
    warning_count = extraction.summary.validation_warning_count
    console.print(f"line_pair_count={extraction.summary.line_pair_count}")
    console.print(f"validation_warning_count={warning_count}")
    console.print(f"canonical_corpus_allowed={str(extraction.summary.canonical_corpus_allowed).lower()}")
    console.print(f"page_boundary_status={extraction.summary.page_boundary_status}")
    if warning_count and not allow_warnings:
        console.print("[red]Legacy Pastebin validation produced warnings.[/red]")
        raise typer.Exit(1)
    console.print("Legacy Pastebin validation OK")


@legacy_pastebin_app.command("extract")
def pastebin_extract(
    input_path: Path | None = typer.Option(None, "--input", help="Local Pastebin TXT path."),
    out_dir: Path = typer.Option(
        default_pastebin_output_dir(),
        "--out-dir",
        help="Generated output directory.",
    ),
) -> None:
    """Extract generated legacy Pastebin records to an ignored output directory."""
    _, extraction = _load_pastebin_extraction_or_exit(input_path)
    output_dir = out_dir if out_dir.is_absolute() else repo_root() / out_dir
    paths = write_pastebin_extraction(output_dir, extraction)

    table = Table("Output", "Path")
    for name, path in paths.items():
        table.add_row(name, str(path))
    console.print(table)
    console.print(f"line_pair_count={extraction.summary.line_pair_count}")
    console.print(f"empty_pair_count={extraction.summary.empty_pair_count}")
    console.print(f"validation_warning_count={extraction.summary.validation_warning_count}")
    console.print(f"unknown_glyph_count={extraction.summary.unknown_glyph_count}")
    console.print(f"unknown_prime_value_count={extraction.summary.unknown_prime_value_count}")
    console.print(f"anchor_count={len(extraction.anchors)}")


@legacy_pastebin_app.command()
def anchors(
    input_path: Path | None = typer.Option(None, "--input", help="Local Pastebin TXT path."),
) -> None:
    """Print non-authoritative anchor counts."""
    _, extraction = _load_pastebin_extraction_or_exit(input_path)
    table = Table("Pair", "Candidate", "Confidence", "Canonical Boundary", "Evidence")
    for anchor in extraction.anchors:
        terminal_evidence = anchor.evidence.encode("unicode_escape").decode("ascii")
        table.add_row(
            str(anchor.pair_index),
            anchor.page_label_candidate,
            anchor.confidence,
            str(anchor.canonical_page_boundary).lower(),
            terminal_evidence,
        )
    console.print(table)
    console.print(f"anchor_count={len(extraction.anchors)}")
    console.print(
        f"parable_anchor_detected={str(any(anchor.page_label_candidate == '57.jpg' for anchor in extraction.anchors)).lower()}"
    )




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(legacy_pastebin_app, name="legacy-pastebin")
