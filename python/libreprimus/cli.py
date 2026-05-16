"""Command-line interface for Stage 0A smoke validation."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from libreprimus.legacy_workbook.export import extract_workbook, write_extraction, write_json
from libreprimus.legacy_workbook.paths import default_output_dir, resolve_workbook_path
from libreprimus.legacy_pastebin.export import (
    extract_legacy_pastebin,
    write_extraction as write_pastebin_extraction,
)
from libreprimus.legacy_pastebin.loader import (
    default_output_dir as default_pastebin_output_dir,
    resolve_input_path,
)
from libreprimus.alignment.export import (
    write_json as write_alignment_json,
    write_jsonl as write_alignment_jsonl,
    write_stage0d_outputs,
)
from libreprimus.alignment.page_boundaries import infer_boundaries_from_alignment_file
from libreprimus.alignment.pastebin_to_transcript import (
    align_pastebin_to_transcript,
    build_alignment_records,
    glyph_variant_observations,
)
from libreprimus.paths import package_root, repo_root
from libreprimus.transcript_sources.export import write_jsonl as write_transcript_jsonl
from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master
from libreprimus.transcript_sources.scream314_reference import parse_scream314_reference
from libreprimus.toolchain import ToolStatus, collect_toolchain

app = typer.Typer(no_args_is_help=True)
legacy_workbook_app = typer.Typer(no_args_is_help=True)
legacy_pastebin_app = typer.Typer(no_args_is_help=True)
transcript_source_app = typer.Typer(no_args_is_help=True)
corpus_alignment_app = typer.Typer(no_args_is_help=True)
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


@legacy_workbook_app.command("summary")
def workbook_summary(
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


@legacy_workbook_app.command("inventory")
def workbook_inventory(
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


@legacy_workbook_app.command("extract")
def workbook_extract(
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


@legacy_workbook_app.command("validate")
def workbook_validate(
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


app.add_typer(legacy_pastebin_app, name="legacy-pastebin")


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


app.add_typer(transcript_source_app, name="transcript-source")


@corpus_alignment_app.command("align-pastebin")
def align_pastebin(
    pastebin: Path = typer.Option(..., "--pastebin", help="Legacy Pastebin TXT path."),
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    out_dir: Path = typer.Option(Path("data/normalized/alignment"), "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Align legacy Pastebin line pairs to transcript records."""
    pastebin_path = _resolve_existing_path(pastebin, "Legacy Pastebin TXT")
    transcript_path = _resolve_existing_path(transcript, "Transcript source")
    result = align_pastebin_to_transcript(pastebin_path, transcript_path)
    output_dir = _resolve_output_path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    alignment_path = output_dir / "pastebin_alignment.jsonl"
    summary_path = output_dir / "alignment_summary.json"
    write_alignment_jsonl(alignment_path, result["alignments"])
    write_alignment_json(summary_path, result["summary"])
    warning_count = len(result["summary"].warnings)
    console.print(f"pastebin_alignment={alignment_path}")
    console.print(f"alignment_summary={summary_path}")
    console.print(f"alignment_record_count={result['summary'].alignment_record_count}")
    console.print(f"exact_confidence_match_count={result['summary'].exact_confidence_match_count}")
    console.print(f"high_confidence_match_count={result['summary'].high_confidence_match_count}")
    console.print(f"no_match_count={result['summary'].no_match_count}")
    console.print(f"warning_count={warning_count}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@corpus_alignment_app.command("infer-boundaries")
def infer_boundaries(
    alignment: Path = typer.Option(..., "--alignment", help="Generated alignment JSONL path."),
    out: Path = typer.Option(..., "--out", help="Generated boundary candidate JSONL path."),
) -> None:
    """Infer boundary candidates from generated alignment records."""
    alignment_path = _resolve_existing_path(alignment, "Alignment JSONL")
    output_path = _resolve_output_path(out)
    boundary_records = infer_boundaries_from_alignment_file(alignment_path)
    write_alignment_jsonl(output_path, boundary_records)
    console.print(f"page_boundary_candidates={output_path}")
    console.print(f"boundary_candidate_count={len(boundary_records)}")
    console.print("canonical_page_boundary=false")


@corpus_alignment_app.command("stage0d-smoke")
def stage0d_smoke(
    pastebin: Path = typer.Option(..., "--pastebin", help="Legacy Pastebin TXT path."),
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    out_dir: Path = typer.Option(Path("data/normalized/alignment"), "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run the full Stage 0D generated-output smoke pipeline."""
    pastebin_path = _resolve_existing_path(pastebin, "Legacy Pastebin TXT")
    transcript_path = _resolve_existing_path(transcript, "Transcript source")
    result = align_pastebin_to_transcript(pastebin_path, transcript_path)
    paths = write_stage0d_outputs(_resolve_output_path(out_dir), result)
    summary_record = result["summary"]
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"transcript_physical_line_count={summary_record.transcript_physical_line_count}")
    console.print(f"pastebin_line_pair_count={summary_record.pastebin_line_pair_count}")
    console.print(f"alignment_record_count={summary_record.alignment_record_count}")
    console.print(f"exact_confidence_match_count={summary_record.exact_confidence_match_count}")
    console.print(f"high_confidence_match_count={summary_record.high_confidence_match_count}")
    console.print(f"medium_confidence_match_count={summary_record.medium_confidence_match_count}")
    console.print(f"low_confidence_match_count={summary_record.low_confidence_match_count}")
    console.print(f"no_match_count={summary_record.no_match_count}")
    console.print(f"page_boundary_candidate_count={summary_record.page_boundary_candidate_count}")
    console.print(f"high_confidence_boundary_count={summary_record.high_confidence_boundary_count}")
    console.print(f"parable_boundary_candidate_present={str(summary_record.parable_boundary_candidate_present).lower()}")
    console.print(f"glyph_variant_observation_count={summary_record.glyph_variant_observation_count}")
    console.print(f"glyph_variant_occurrence_count={summary_record.glyph_variant_occurrence_count}")
    console.print(f"elapsed_milliseconds={summary_record.elapsed_milliseconds}")
    if summary_record.warnings and not allow_warnings:
        raise typer.Exit(1)


@corpus_alignment_app.command("glyph-variants")
def glyph_variants(
    pastebin: Path = typer.Option(..., "--pastebin", help="Legacy Pastebin TXT path."),
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    out: Path = typer.Option(..., "--out", help="Generated glyph-variant observations JSONL path."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Write glyph variant observations."""
    pastebin_path = _resolve_existing_path(pastebin, "Legacy Pastebin TXT")
    transcript_path = _resolve_existing_path(transcript, "Transcript source")
    pastebin_extraction = extract_legacy_pastebin(pastebin_path)
    transcript_records, _ = parse_rtkd_master(transcript_path)
    alignments, _ = build_alignment_records(pastebin_extraction, transcript_records)
    observations = glyph_variant_observations(
        pastebin_extraction.line_pairs,
        alignments,
        transcript_records,
        pastebin_extraction.summary.source_sha256,
    )
    output_path = _resolve_output_path(out)
    write_alignment_jsonl(output_path, observations)
    warning_count = sum(len(observation.warnings) for observation in observations)
    console.print(f"glyph_variant_observations={output_path}")
    console.print(f"glyph_variant_observation_count={len(observations)}")
    console.print(f"glyph_variant_occurrence_count={sum(observation.occurrence_count for observation in observations)}")
    console.print(f"warning_count={warning_count}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


app.add_typer(corpus_alignment_app, name="corpus-alignment")


if __name__ == "__main__":
    app()
