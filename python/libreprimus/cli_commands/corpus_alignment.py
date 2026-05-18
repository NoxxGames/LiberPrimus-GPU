"""Corpus alignment CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

corpus_alignment_app = typer.Typer(no_args_is_help=True)


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


@corpus_alignment_app.command("stage0d-followup-smoke")
def stage0d_followup_smoke(
    pastebin: Path = typer.Option(..., "--pastebin", help="Legacy Pastebin TXT path."),
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    out_dir: Path = typer.Option(Path("data/normalized/alignment"), "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run the Stage 0D-followup alignment, gap, and boundary-audit smoke pipeline."""
    pastebin_path = _resolve_existing_path(pastebin, "Legacy Pastebin TXT")
    transcript_path = _resolve_existing_path(transcript, "Transcript source")
    result = align_pastebin_to_transcript_followup(pastebin_path, transcript_path)
    paths = write_stage0d_followup_outputs(_resolve_output_path(out_dir), result)
    summary_record = result["summary"]
    gap_summary = result["gap_summary"]
    boundary_summary = result["boundary_audit_summary"]
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"transcript_physical_line_count={summary_record.transcript_physical_line_count}")
    console.print(f"transcript_logical_line_count={summary_record.transcript_logical_line_count}")
    console.print(f"transcript_rune_stream_length={summary_record.transcript_rune_stream_length}")
    console.print(f"pastebin_line_pair_count={summary_record.pastebin_line_pair_count}")
    console.print(f"alignment_record_count={summary_record.alignment_record_count}")
    console.print(f"exact_count={summary_record.exact_count}")
    console.print(f"high_count={summary_record.high_count}")
    console.print(f"medium_count={summary_record.medium_count}")
    console.print(f"low_count={summary_record.low_count}")
    console.print(f"none_count={summary_record.none_count}")
    console.print(f"no_match_reduction={summary_record.no_match_reduction}")
    console.print(f"logical_line_match_count={summary_record.logical_line_match_count}")
    console.print(f"stream_subsequence_match_count={summary_record.stream_subsequence_match_count}")
    console.print(f"decimal_index_match_count={summary_record.decimal_index_match_count}")
    console.print(f"variant_normalized_match_count={summary_record.variant_normalized_match_count}")
    console.print(f"gap_reason_counts={gap_summary.gap_reason_counts}")
    console.print(f"boundary_high_count={boundary_summary.high_count}")
    console.print(f"boundary_medium_count={boundary_summary.medium_count}")
    console.print(f"boundary_low_count={boundary_summary.low_count}")
    console.print(f"boundary_none_count={boundary_summary.none_count}")
    console.print(f"overgeneration_warning={str(boundary_summary.overgeneration_warning).lower()}")
    console.print(f"glyph_variant_observation_count={summary_record.glyph_variant_observation_count}")
    console.print(f"elapsed_milliseconds={summary_record.timing_ms}")
    warning_count = sum(len(alignment.warnings) for alignment in result["alignments"])
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@corpus_alignment_app.command("gap-report")
def gap_report(
    pastebin: Path = typer.Option(..., "--pastebin", help="Legacy Pastebin TXT path."),
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    out_dir: Path = typer.Option(Path("data/normalized/alignment"), "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for script symmetry; gaps are diagnostics."),
) -> None:
    """Write Stage 0D-followup alignment gap diagnostics."""
    del allow_warnings
    pastebin_path = _resolve_existing_path(pastebin, "Legacy Pastebin TXT")
    transcript_path = _resolve_existing_path(transcript, "Transcript source")
    result = align_pastebin_to_transcript_followup(pastebin_path, transcript_path)
    output_dir = _resolve_output_path(out_dir)
    diagnostics_path = output_dir / "alignment_gap_diagnostics.jsonl"
    summary_path = output_dir / "alignment_gap_summary.json"
    write_alignment_jsonl(diagnostics_path, result["gap_diagnostics"])
    write_alignment_json(summary_path, result["gap_summary"])
    gap_summary = result["gap_summary"]
    console.print(f"alignment_gap_diagnostics={diagnostics_path}")
    console.print(f"alignment_gap_summary={summary_path}")
    console.print(f"total_pairs={gap_summary.total_pairs}")
    console.print(f"matched_pairs={gap_summary.matched_pairs}")
    console.print(f"no_match_pairs={gap_summary.no_match_pairs}")
    console.print(f"low_confidence_pairs={gap_summary.low_confidence_pairs}")
    console.print(f"gap_reason_counts={gap_summary.gap_reason_counts}")
    console.print(f"unresolved_pairs={gap_summary.unresolved_pairs}")


def _read_boundary_candidates(path: Path) -> list[PageBoundaryCandidate]:
    records: list[PageBoundaryCandidate] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            records.append(PageBoundaryCandidate(**payload))
    return records


@corpus_alignment_app.command("audit-boundaries")
def audit_boundaries(
    alignment: Path = typer.Option(..., "--alignment", help="Generated alignment JSONL path; sibling boundary file is audited."),
    out_dir: Path = typer.Option(Path("data/normalized/alignment"), "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for script symmetry; audit warnings are reported."),
) -> None:
    """Audit generated page-boundary confidence records."""
    del allow_warnings
    alignment_path = _resolve_existing_path(alignment, "Alignment JSONL")
    output_dir = _resolve_output_path(out_dir)
    boundary_path = alignment_path.parent / "page_boundary_candidates.jsonl"
    if not boundary_path.is_file():
        console.print(f"[red]Boundary candidate file not found: {boundary_path}[/red]")
        raise typer.Exit(2)
    boundaries = _read_boundary_candidates(boundary_path)
    audits, summary = audit_page_boundaries(boundaries)
    audit_path = output_dir / "page_boundary_confidence_audit.jsonl"
    summary_path = output_dir / "page_boundary_audit.json"
    write_alignment_jsonl(audit_path, audits)
    write_alignment_json(summary_path, summary)
    console.print(f"page_boundary_confidence_audit={audit_path}")
    console.print(f"page_boundary_audit={summary_path}")
    console.print(f"total_boundary_candidates={summary.total_boundary_candidates}")
    console.print(f"high_count={summary.high_count}")
    console.print(f"medium_count={summary.medium_count}")
    console.print(f"low_count={summary.low_count}")
    console.print(f"none_count={summary.none_count}")
    console.print(f"overgeneration_warning={str(summary.overgeneration_warning).lower()}")
    console.print(f"canonical_page_boundary_all_false={str(summary.canonical_page_boundary_all_false).lower()}")


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




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(corpus_alignment_app, name="corpus-alignment")
