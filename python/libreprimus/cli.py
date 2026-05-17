"""Command-line interface for Stage 0A smoke validation."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from libreprimus.corpus_candidate.export import write_corpus_candidate_outputs
from libreprimus.corpus_candidate.generator import build_rtkd_corpus_candidate
from libreprimus.corpus_candidate.separator_inventory import observed_separator_inventory
from libreprimus.corpus_candidate.summary import load_summary as load_candidate_summary
from libreprimus.corpus_candidate.validation import validate_corpus_candidate
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
    write_stage0d_followup_outputs,
    write_stage0d_outputs,
)
from libreprimus.alignment.boundary_audit import audit_page_boundaries
from libreprimus.alignment.models import PageBoundaryCandidate
from libreprimus.alignment.page_boundaries import infer_boundaries_from_alignment_file
from libreprimus.alignment.pastebin_to_transcript import (
    align_pastebin_to_transcript,
    align_pastebin_to_transcript_followup,
    build_alignment_records,
    glyph_variant_observations,
)
from libreprimus.paths import package_root, repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile, validate_gematria_profile
from libreprimus.profiles.glyph_variant_profile import load_glyph_variant_profile, validate_glyph_variant_profile
from libreprimus.profiles.separator_grammar import load_separator_grammar, validate_separator_grammar
from libreprimus.solved_fixtures.export import write_json as write_fixture_json
from libreprimus.solved_fixtures.export import write_reproduction_outputs
from libreprimus.solved_fixtures.fixture_loader import load_fixtures
from libreprimus.solved_fixtures.reproduction import (
    reproduce_atbash_family_fixtures,
    reproduce_direct_translation_fixtures,
    reproduce_prime_stream_fixtures,
    reproduce_vigenere_fixtures,
)
from libreprimus.solved_fixtures.summary import load_summary as load_fixture_summary
from libreprimus.solved_fixtures.validation import validate_fixture_dir, validate_reproduction_results
from libreprimus.solved_baselines.export import write_manifest_run_outputs
from libreprimus.solved_baselines.manifest_loader import load_manifest
from libreprimus.solved_baselines.runner import run_manifest
from libreprimus.solved_baselines.summary import load_summary as load_baseline_summary
from libreprimus.solved_baselines.validation import validate_manifest_file
from libreprimus.result_store.import_solved_baseline import import_solved_baseline
from libreprimus.result_store.summary import load_summary as load_result_store_summary
from libreprimus.result_store.validation import (
    validate_result_store,
    validate_result_store_manifest_file,
)
from libreprimus.result_store.sqlite_sink import table_counts
from libreprimus.consistency.runner import run_consistency_suite
from libreprimus.experiments.dry_run_planner import build_dry_run_plan
from libreprimus.experiments.export import write_dry_run_outputs, write_summary as write_dry_run_summary
from libreprimus.experiments.manifest_loader import load_exploratory_manifest
from libreprimus.experiments.summary import load_plan_records, load_summary as load_dry_run_summary
from libreprimus.experiment_execution.cpu_runner import run_cpu_execution_manifest
from libreprimus.experiment_execution.execution_planner import build_execution_plan
from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest
from libreprimus.experiment_execution.result_export import (
    write_aggregate_summary as write_execution_aggregate_summary,
    write_execution_outputs,
)
from libreprimus.experiment_execution.summary import (
    load_result_records as load_execution_result_records,
    load_summary as load_execution_summary,
)
from libreprimus.experiment_proposals.approval_gate import evaluate_approval_gate
from libreprimus.experiment_proposals.approval_records import load_approval_record
from libreprimus.experiment_proposals.export import (
    write_review_packet_outputs,
    write_summary as write_review_packet_summary,
)
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal
from libreprimus.experiment_proposals.review_packet import build_review_packet
from libreprimus.experiment_proposals.summary import (
    load_review_packets,
    load_summary as load_review_packet_summary,
)
from libreprimus.approval_execution.execution_bridge import (
    build_approval_execution_plan,
    run_approval_execution_request,
)
from libreprimus.approval_execution.request_loader import load_approval_execution_request
from libreprimus.approval_execution.result_export import (
    write_approval_execution_outputs,
    write_summary as write_approval_execution_summary,
)
from libreprimus.approval_execution.summary import (
    load_result_records as load_approval_execution_result_records,
    load_summary as load_approval_execution_summary,
)
from libreprimus.approval_readiness.export import (
    write_approval_readiness_outputs,
    write_summary as write_approval_readiness_summary,
)
from libreprimus.approval_readiness.packet_generator import build_approval_readiness_packet
from libreprimus.approval_readiness.readiness_analyzer import analyze_approval_readiness
from libreprimus.approval_readiness.summary import (
    load_packets as load_approval_readiness_packets,
    load_summary as load_approval_readiness_summary,
)
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_experiments.runner import (
    check_queue_paths as check_bounded_queue_paths,
    run_all as run_all_bounded_experiments,
    run_next as run_next_bounded_experiment,
)
from libreprimus.bounded_experiments.summary import (
    load_results as load_bounded_experiment_results,
    load_summary as load_bounded_experiment_summary,
)
from libreprimus.bounded_execution.runner import run_caesar_affine_from_paths
from libreprimus.bounded_execution.summary import load_summary as load_bounded_run_summary
from libreprimus.candidate_inspection.analysis import inspect_results, rerank_candidates
from libreprimus.candidate_inspection.loader import load_candidate_records
from libreprimus.candidate_inspection.report import (
    write_inspection_markdown,
    write_json as write_inspection_json,
    write_jsonl as write_inspection_jsonl,
)
from libreprimus.candidate_inspection.summary import to_summary_payload
from libreprimus.candidate_inspection.validation import validate_no_full_dump_in_markdown, validate_summary_payload
from libreprimus.scoring.calibration import run_scoring_calibration
from libreprimus.scoring.crib_checks import DEFAULT_CRIBS_PATH, crib_check, load_cribs
from libreprimus.reference_sources.summary import build_stage1c_reference_summary, write_stage1c_reference_outputs
from libreprimus.transcript_sources.export import write_jsonl as write_transcript_jsonl
from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master
from libreprimus.transcript_sources.scream314_reference import parse_scream314_reference
from libreprimus.toolchain import ToolStatus, collect_toolchain
from libreprimus.transforms.registry import load_registry, resolve_transform
from libreprimus.transforms.validation import validate_registry_file

app = typer.Typer(no_args_is_help=True)
legacy_workbook_app = typer.Typer(no_args_is_help=True)
legacy_pastebin_app = typer.Typer(no_args_is_help=True)
transcript_source_app = typer.Typer(no_args_is_help=True)
corpus_alignment_app = typer.Typer(no_args_is_help=True)
profile_app = typer.Typer(no_args_is_help=True)
corpus_candidate_app = typer.Typer(no_args_is_help=True)
solved_fixture_app = typer.Typer(no_args_is_help=True)
reference_source_app = typer.Typer(no_args_is_help=True)
transform_registry_app = typer.Typer(no_args_is_help=True)
solved_baseline_app = typer.Typer(no_args_is_help=True)
result_store_app = typer.Typer(no_args_is_help=True)
consistency_app = typer.Typer(no_args_is_help=True)
experiment_app = typer.Typer(no_args_is_help=True)
execution_app = typer.Typer(no_args_is_help=True)
proposal_app = typer.Typer(no_args_is_help=True)
approval_execution_app = typer.Typer(no_args_is_help=True)
approval_readiness_app = typer.Typer(no_args_is_help=True)
bounded_experiment_app = typer.Typer(no_args_is_help=True)
bounded_run_app = typer.Typer(no_args_is_help=True)
candidate_inspect_app = typer.Typer(no_args_is_help=True)
scoring_app = typer.Typer(no_args_is_help=True)
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


app.add_typer(corpus_alignment_app, name="corpus-alignment")


DEFAULT_GEMATRIA_PROFILE = Path("data/profiles/gematria/gematria-primus-v0.json")
DEFAULT_GLYPH_VARIANT_PROFILE = Path("data/profiles/glyph-variants/glyph-variants-v0.json")
DEFAULT_SEPARATOR_GRAMMAR = Path("data/profiles/separators/rtkd-separator-grammar-v0.json")
DEFAULT_CORPUS_CANDIDATE_DIR = Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate")
DEFAULT_DIRECT_FIXTURE_DIR = Path("data/fixtures/solved-pages/direct-translation-v0")
DEFAULT_DIRECT_BASELINE_DIR = Path("data/normalized/solved-baselines/direct-translation-v0")
DEFAULT_ATBASH_FIXTURE_DIR = Path("data/fixtures/solved-pages/atbash-family-v0")
DEFAULT_ATBASH_BASELINE_DIR = Path("data/normalized/solved-baselines/atbash-family-v0")
DEFAULT_VIGENERE_FIXTURE_DIR = Path("data/fixtures/solved-pages/vigenere-v0")
DEFAULT_VIGENERE_BASELINE_DIR = Path("data/normalized/solved-baselines/vigenere-v0")
DEFAULT_PRIME_STREAM_FIXTURE_DIR = Path("data/fixtures/solved-pages/prime-stream-v0")
DEFAULT_PRIME_STREAM_BASELINE_DIR = Path("data/normalized/solved-baselines/prime-stream-v0")
DEFAULT_REFERENCE_SUMMARY_DIR = Path("data/normalized/reference-summaries/stage-1c")
DEFAULT_TRANSFORM_REGISTRY = Path("data/transform-registry/cpu-reference-transforms-v0.json")
DEFAULT_SOLVED_BASELINE_MANIFEST = Path(
    "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml"
)
DEFAULT_STAGE2A_RESULTS_DIR = Path("experiments/results/solved-baselines/stage2a")
DEFAULT_RESULT_STORE_MANIFEST = Path("experiments/manifests/result-store/stage2b-solved-baseline-import.yaml")
DEFAULT_STAGE2B_RESULT_STORE_DIR = Path("experiments/results/result-store/stage2b")
DEFAULT_STAGE2B_SQLITE = DEFAULT_STAGE2B_RESULT_STORE_DIR / "results.sqlite3"
DEFAULT_STAGE2D_CONSISTENCY_SUMMARY = Path(
    "experiments/results/consistency/stage2d/consistency_summary.json"
)


@profile_app.command("validate-gematria")
def validate_gematria(
    profile: Path = typer.Option(DEFAULT_GEMATRIA_PROFILE, "--profile", help="Gematria profile JSON path."),
) -> None:
    """Validate the frozen Gematria Primus profile."""
    profile_path = _resolve_existing_path(profile, "Gematria profile")
    gematria = load_gematria_profile(profile_path)
    result = validate_gematria_profile(gematria)
    console.print(f"profile_id={gematria.profile_id}")
    console.print(f"entry_count={len(gematria.entries)}")
    console.print(f"sha256={gematria.sha256}")
    console.print(f"canonical_profile_active={str(gematria.canonical_profile_active).lower()}")
    console.print(f"canonical_corpus_active={str(gematria.canonical_corpus_active).lower()}")
    console.print(f"variant_glyph_canonical={str(chr(0x16C2) in gematria.rune_to_entry).lower()}")
    if not result.valid:
        for error in result.errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Gematria profile validation OK")


@profile_app.command("validate-glyph-variants")
def validate_glyph_variants(
    gematria: Path = typer.Option(DEFAULT_GEMATRIA_PROFILE, "--gematria", help="Gematria profile JSON path."),
    variants: Path = typer.Option(DEFAULT_GLYPH_VARIANT_PROFILE, "--variants", help="Glyph variant profile JSON path."),
) -> None:
    """Validate glyph variants against the Gematria profile."""
    gematria_profile = load_gematria_profile(_resolve_existing_path(gematria, "Gematria profile"))
    variant_profile = load_glyph_variant_profile(_resolve_existing_path(variants, "Glyph variant profile"))
    result = validate_glyph_variant_profile(variant_profile, gematria_profile)
    console.print(f"profile_id={variant_profile.profile_id}")
    console.print(f"variant_count={len(variant_profile.variants)}")
    console.print(f"sha256={variant_profile.sha256}")
    if variant_profile.variants:
        first = variant_profile.variants[0]
        observed = first.observed_glyph.encode("unicode_escape").decode("ascii")
        normalized = first.normalized_rune_candidate.encode("unicode_escape").decode("ascii")
        console.print(f"observed_glyph={observed}")
        console.print(f"normalized_rune_candidate={normalized}")
        console.print(f"normalized_index_candidate={first.normalized_index_candidate}")
        console.print(f"canonical_mapping_change={str(first.canonical_mapping_change).lower()}")
    if not result.valid:
        for error in result.errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Glyph variant profile validation OK")


@profile_app.command("validate-separators")
def validate_separators(
    grammar: Path = typer.Option(DEFAULT_SEPARATOR_GRAMMAR, "--grammar", help="Separator grammar JSON path."),
) -> None:
    """Validate the frozen rtkd separator grammar."""
    separator_grammar = load_separator_grammar(_resolve_existing_path(grammar, "Separator grammar"))
    result = validate_separator_grammar(separator_grammar)
    console.print(f"profile_id={separator_grammar.profile_id}")
    console.print(f"separator_class_count={len(separator_grammar.separator_classes)}")
    console.print(f"sha256={separator_grammar.sha256}")
    console.print(f"canonical_profile_active={str(separator_grammar.canonical_profile_active).lower()}")
    console.print(f"canonical_corpus_active={str(separator_grammar.canonical_corpus_active).lower()}")
    if not result.valid:
        for error in result.errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Separator grammar validation OK")


@profile_app.command("summary")
def profile_summary() -> None:
    """Summarize Stage 0E profile files."""
    gematria = load_gematria_profile(_resolve_existing_path(DEFAULT_GEMATRIA_PROFILE, "Gematria profile"))
    variants = load_glyph_variant_profile(_resolve_existing_path(DEFAULT_GLYPH_VARIANT_PROFILE, "Glyph variant profile"))
    separators = load_separator_grammar(_resolve_existing_path(DEFAULT_SEPARATOR_GRAMMAR, "Separator grammar"))
    table = Table("Profile", "SHA-256", "Active")
    table.add_row(gematria.profile_id, gematria.sha256, str(gematria.canonical_profile_active).lower())
    table.add_row(variants.profile_id, variants.sha256, str(variants.canonical_profile_active).lower())
    table.add_row(separators.profile_id, separators.sha256, str(separators.canonical_profile_active).lower())
    console.print(table)


app.add_typer(profile_app, name="profile")


@corpus_candidate_app.command("build-rtkd-v0")
def build_rtkd_v0(
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    gematria: Path = typer.Option(DEFAULT_GEMATRIA_PROFILE, "--gematria", help="Gematria profile path."),
    glyph_variants: Path = typer.Option(DEFAULT_GLYPH_VARIANT_PROFILE, "--glyph-variants", help="Glyph variant profile path."),
    separators: Path = typer.Option(DEFAULT_SEPARATOR_GRAMMAR, "--separators", help="Separator grammar path."),
    alignment_dir: Path = typer.Option(Path("data/normalized/alignment"), "--alignment-dir", help="Generated alignment output directory."),
    out_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--out-dir", help="Generated corpus candidate directory."),
    allow_boundary_warnings: bool = typer.Option(False, "--allow-boundary-warnings", help="Return success despite page-candidate warnings."),
) -> None:
    """Build generated rtkd master v0 corpus candidate outputs."""
    transcript_path = _resolve_existing_path(transcript, "Transcript source")
    result = build_rtkd_corpus_candidate(
        transcript_path=transcript_path,
        gematria_path=_resolve_existing_path(gematria, "Gematria profile"),
        glyph_variants_path=_resolve_existing_path(glyph_variants, "Glyph variant profile"),
        separators_path=_resolve_existing_path(separators, "Separator grammar"),
        alignment_dir=_resolve_output_path(alignment_dir),
    )
    paths = write_corpus_candidate_outputs(_resolve_output_path(out_dir), result)
    summary = result["summary"]
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"corpus_candidate_id={summary.corpus_candidate_id}")
    console.print(f"physical_line_count={summary.physical_line_count}")
    console.print(f"logical_line_count={summary.logical_line_count}")
    console.print(f"token_count={summary.token_count}")
    console.print(f"rune_token_count={summary.rune_token_count}")
    console.print(f"separator_token_count={summary.separator_token_count}")
    console.print(f"numeric_literal_count={summary.numeric_literal_count}")
    console.print(f"unknown_symbol_count={summary.unknown_symbol_count}")
    console.print(f"variant_mapped_token_count={summary.variant_mapped_token_count}")
    console.print(f"page_candidate_count={summary.page_candidate_count}")
    console.print(f"warning_count={summary.warning_count}")
    console.print(f"canonical_corpus_candidate={str(summary.canonical_corpus_candidate).lower()}")
    console.print(f"canonical_corpus_active={str(summary.canonical_corpus_active).lower()}")
    console.print(f"page_boundaries_final={str(summary.page_boundaries_final).lower()}")
    console.print(f"elapsed_milliseconds={summary.elapsed_milliseconds}")
    boundary_warning = any(warning.warning_code.startswith("page_") for warning in result["warnings"])
    if boundary_warning and not allow_boundary_warnings:
        raise typer.Exit(1)


@corpus_candidate_app.command("validate")
def validate_candidate(
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite generated warnings."),
) -> None:
    """Validate generated corpus candidate outputs."""
    output_dir = _resolve_output_path(candidate_dir)
    errors = validate_corpus_candidate(output_dir, allow_warnings=allow_warnings)
    console.print(f"candidate_dir={output_dir}")
    console.print(f"validation_error_count={len(errors)}")
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Corpus candidate validation OK")


@corpus_candidate_app.command("summary")
def candidate_summary(
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
) -> None:
    """Print generated corpus candidate summary."""
    output_dir = _resolve_output_path(candidate_dir)
    summary = load_candidate_summary(output_dir)
    for key in [
        "corpus_candidate_id",
        "physical_line_count",
        "logical_line_count",
        "token_count",
        "rune_token_count",
        "separator_token_count",
        "numeric_literal_count",
        "unknown_symbol_count",
        "variant_mapped_token_count",
        "page_candidate_count",
        "warning_count",
        "canonical_corpus_candidate",
        "canonical_corpus_active",
        "page_boundaries_final",
    ]:
        console.print(f"{key}={str(summary.get(key)).lower() if isinstance(summary.get(key), bool) else summary.get(key)}")


@corpus_candidate_app.command("separator-inventory")
def separator_inventory(
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    grammar: Path = typer.Option(DEFAULT_SEPARATOR_GRAMMAR, "--grammar", help="Separator grammar path."),
    out: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR / "observed_separator_inventory.json", "--out", help="Generated inventory JSON path."),
) -> None:
    """Generate observed separator inventory."""
    transcript_path = _resolve_existing_path(transcript, "Transcript source")
    separator_grammar = load_separator_grammar(_resolve_existing_path(grammar, "Separator grammar"))
    inventory = observed_separator_inventory(transcript_path, separator_grammar)
    output_path = _resolve_output_path(out)
    write_alignment_json(output_path, inventory)
    console.print(f"observed_separator_inventory={output_path}")
    console.print(f"unknown_observed_separator_count={inventory['unknown_observed_separator_count']}")


@corpus_candidate_app.command("stage0e-smoke")
def stage0e_smoke(
    transcript: Path = typer.Option(..., "--transcript", help="rtkd transcript path."),
    out_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--out-dir", help="Generated corpus candidate directory."),
    allow_boundary_warnings: bool = typer.Option(False, "--allow-boundary-warnings", help="Return success despite page-candidate warnings."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite generated warnings."),
) -> None:
    """Run Stage 0E profile validation and corpus candidate smoke generation."""
    build_rtkd_v0(
        transcript=transcript,
        gematria=DEFAULT_GEMATRIA_PROFILE,
        glyph_variants=DEFAULT_GLYPH_VARIANT_PROFILE,
        separators=DEFAULT_SEPARATOR_GRAMMAR,
        alignment_dir=Path("data/normalized/alignment"),
        out_dir=out_dir,
        allow_boundary_warnings=allow_boundary_warnings,
    )
    validate_candidate(candidate_dir=out_dir, allow_warnings=allow_warnings)


app.add_typer(corpus_candidate_app, name="corpus-candidate")


@reference_source_app.command("extract-stage1c")
def reference_source_extract_stage1c(
    out_dir: Path = typer.Option(DEFAULT_REFERENCE_SUMMARY_DIR, "--out-dir", help="Generated reference summary directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite partial reference notes."),
) -> None:
    """Extract small Stage 1C reference-source summaries from mirrored raw files."""
    output_dir = _resolve_output_path(out_dir)
    payload = build_stage1c_reference_summary()
    paths = write_stage1c_reference_outputs(output_dir, payload)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    summary = payload["summary"]
    console.print(f"scream314_method_note_count={summary['scream314_method_note_count']}")
    console.print(f"lipeeeee_tooling_note_count={summary['lipeeeee_tooling_note_count']}")
    console.print(f"divinity_found={str(summary['divinity_found']).lower()}")
    console.print(f"firfumferenfe_found={str(summary['firfumferenfe_found']).lower()}")
    console.print(f"cleartext_f_skip_note_found={str(summary['cleartext_f_skip_note_found']).lower()}")
    console.print(f"imported_as_dependency={str(summary['imported_as_dependency']).lower()}")
    console.print(f"code_copied={str(summary['code_copied']).lower()}")
    if not allow_warnings and not summary["scream314_method_note_count"]:
        raise typer.Exit(1)


@reference_source_app.command("summary")
def reference_source_summary(
    out_dir: Path = typer.Option(DEFAULT_REFERENCE_SUMMARY_DIR, "--out-dir", help="Generated reference summary directory."),
) -> None:
    """Print generated Stage 1C reference-source summary."""
    summary_path = _resolve_output_path(out_dir) / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for key in [
        "scream314_method_note_count",
        "lipeeeee_tooling_note_count",
        "divinity_found",
        "firfumferenfe_found",
        "cleartext_f_skip_note_found",
        "reference_only",
        "imported_as_dependency",
        "code_copied",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


app.add_typer(reference_source_app, name="reference-source")


@transform_registry_app.command("summary")
def transform_registry_summary(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
) -> None:
    """Print a concise transform registry summary."""
    loaded = load_registry(_resolve_existing_path(registry, "Transform registry"))
    alias_count = sum(1 for definition in loaded.transforms if definition.alias_of)
    console.print(f"registry_id={loaded.registry_id}")
    console.print(f"registry_sha256={loaded.sha256}")
    console.print(f"transform_count={len(loaded.transforms)}")
    console.print(f"alias_count={alias_count}")
    console.print(f"search_enabled={str(loaded.search_enabled).lower()}")
    console.print(f"cuda_enabled={str(loaded.cuda_enabled).lower()}")
    console.print(f"scoring_enabled={str(loaded.scoring_enabled).lower()}")


@transform_registry_app.command("validate")
def transform_registry_validate(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
) -> None:
    """Validate CPU transform registry metadata and implementation links."""
    errors = validate_registry_file(_resolve_existing_path(registry, "Transform registry"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Transform registry validation OK")


@transform_registry_app.command("list")
def transform_registry_list(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
) -> None:
    """List registered CPU reference transforms."""
    loaded = load_registry(_resolve_existing_path(registry, "Transform registry"))
    table = Table("Transform", "Method", "Alias Of", "Search", "CUDA", "Scoring")
    for definition in loaded.transforms:
        table.add_row(
            definition.transform_id,
            definition.method_family,
            definition.alias_of or "",
            str(definition.search_enabled).lower(),
            str(definition.supports_gpu).lower(),
            str(definition.scoring_enabled).lower(),
        )
    console.print(table)


@transform_registry_app.command("resolve")
def transform_registry_resolve(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
    transform_id: str = typer.Option(..., "--transform-id", help="Transform ID or alias ID to resolve."),
) -> None:
    """Resolve a transform alias to its canonical transform."""
    loaded = load_registry(_resolve_existing_path(registry, "Transform registry"))
    try:
        definition = resolve_transform(loaded, transform_id)
    except KeyError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(2) from error
    console.print(f"transform_id={transform_id}")
    console.print(f"canonical_transform_id={definition.transform_id}")
    console.print(f"transform_version={definition.transform_version}")


app.add_typer(transform_registry_app, name="transform-registry")


@solved_baseline_app.command("validate-manifest")
def solved_baseline_validate_manifest(
    manifest: Path = typer.Option(DEFAULT_SOLVED_BASELINE_MANIFEST, "--manifest", help="Solved-baseline run manifest."),
) -> None:
    """Validate a solved-baseline run manifest."""
    errors = validate_manifest_file(_resolve_existing_path(manifest, "Solved-baseline manifest"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Solved-baseline manifest validation OK")


@solved_baseline_app.command("run")
def solved_baseline_run(
    manifest: Path = typer.Option(DEFAULT_SOLVED_BASELINE_MANIFEST, "--manifest", help="Solved-baseline run manifest."),
    candidate_dir: Path | None = typer.Option(None, "--candidate-dir", help="Generated corpus candidate directory override."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2A_RESULTS_DIR, "--out-dir", help="Generated manifest-runner output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite generated warnings."),
) -> None:
    """Run a solved-baseline manifest through CPU registry dispatch."""
    loaded_manifest = load_manifest(_resolve_existing_path(manifest, "Solved-baseline manifest"))
    records, summary, warnings = run_manifest(
        loaded_manifest,
        candidate_dir=_resolve_output_path(candidate_dir) if candidate_dir is not None else None,
    )
    paths = write_manifest_run_outputs(_resolve_output_path(out_dir), records, summary, warnings)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"manifest_id={summary.manifest_id}")
    console.print(f"fixture_group_count={summary.fixture_group_count}")
    console.print(f"fixture_count={summary.fixture_count}")
    console.print(f"pass_count={summary.pass_count}")
    console.print(f"fail_count={summary.fail_count}")
    console.print(f"pending_count={summary.pending_count}")
    console.print(f"skipped_count={summary.skipped_count}")
    console.print(f"search_performed_any={str(summary.search_performed_any).lower()}")
    console.print(f"cuda_used_any={str(summary.cuda_used_any).lower()}")
    console.print(f"scoring_used_any={str(summary.scoring_used_any).lower()}")
    console.print(f"elapsed_ms={summary.elapsed_ms}")
    if summary.fail_count or summary.pending_count or summary.skipped_count:
        raise typer.Exit(1)
    if warnings and not allow_warnings:
        raise typer.Exit(1)


@solved_baseline_app.command("summary")
def solved_baseline_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE2A_RESULTS_DIR, "--results-dir", help="Generated manifest-runner output directory."),
) -> None:
    """Print a generated solved-baseline manifest-run summary."""
    summary = load_baseline_summary(_resolve_output_path(results_dir))
    for key in [
        "manifest_id",
        "registry_id",
        "fixture_group_count",
        "fixture_count",
        "pass_count",
        "fail_count",
        "pending_count",
        "skipped_count",
        "direct_translation_pass_count",
        "atbash_family_pass_count",
        "vigenere_pass_count",
        "prime_stream_pass_count",
        "search_performed_any",
        "cuda_used_any",
        "scoring_used_any",
        "elapsed_ms",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


@solved_baseline_app.command("stage2a-smoke")
def stage2a_smoke(
    manifest: Path = typer.Option(DEFAULT_SOLVED_BASELINE_MANIFEST, "--manifest", help="Solved-baseline run manifest."),
    candidate_dir: Path | None = typer.Option(None, "--candidate-dir", help="Generated corpus candidate directory override."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2A_RESULTS_DIR, "--out-dir", help="Generated manifest-runner output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite generated warnings."),
) -> None:
    """Run the Stage 2A registry and all-known solved-baseline smoke test."""
    transform_registry_validate(registry=DEFAULT_TRANSFORM_REGISTRY)
    solved_baseline_validate_manifest(manifest=manifest)
    solved_baseline_run(
        manifest=manifest,
        candidate_dir=candidate_dir,
        out_dir=out_dir,
        allow_warnings=allow_warnings,
    )
    summary = load_baseline_summary(_resolve_output_path(out_dir))
    loaded_manifest = load_manifest(_resolve_existing_path(manifest, "Solved-baseline manifest"))
    expected_pass = loaded_manifest.expected_counts.get("pass_count", 0)
    expected_fail = loaded_manifest.expected_counts.get("fail_count", 0)
    expected_pending = loaded_manifest.expected_counts.get("pending_count", 0)
    if (
        summary.get("pass_count") != expected_pass
        or summary.get("fail_count") != expected_fail
        or summary.get("pending_count") != expected_pending
    ):
        console.print("[red]Stage 2A smoke counts did not match manifest expectations.[/red]")
        raise typer.Exit(1)
    console.print("Stage 2A smoke OK")


app.add_typer(solved_baseline_app, name="solved-baseline")


@result_store_app.command("validate-manifest")
def result_store_validate_manifest(
    manifest: Path = typer.Option(DEFAULT_RESULT_STORE_MANIFEST, "--manifest", help="Result-store manifest path."),
) -> None:
    """Validate a result-store manifest."""
    errors = validate_result_store_manifest_file(_resolve_existing_path(manifest, "Result-store manifest"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Result-store manifest validation OK")


@result_store_app.command("import-solved-baseline")
def result_store_import_solved_baseline(
    manifest: Path = typer.Option(DEFAULT_RESULT_STORE_MANIFEST, "--manifest", help="Result-store manifest path."),
    solved_baseline_results: Path = typer.Option(
        DEFAULT_STAGE2A_RESULTS_DIR,
        "--solved-baseline-results",
        help="Generated Stage 2A solved-baseline results directory.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE2B_RESULT_STORE_DIR, "--out-dir", help="Generated result-store directory."),
    replace: bool = typer.Option(False, "--replace", help="Replace duplicate run_id rows in SQLite."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite imported warnings."),
) -> None:
    """Import solved-baseline manifest-run outputs into JSONL and SQLite result stores."""
    try:
        result = import_solved_baseline(
            _resolve_existing_path(manifest, "Result-store manifest"),
            solved_baseline_results=_resolve_output_path(solved_baseline_results),
            out_dir=_resolve_output_path(out_dir),
            replace=replace,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = result["paths"]
    summary = result["summary"]
    run_record = result["run_records"][0]
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"run_id={run_record.run_id}")
    console.print(f"manifest_id={run_record.manifest_id}")
    console.print(f"manifest_sha256={run_record.manifest_sha256}")
    console.print(f"registry_sha256={run_record.registry_sha256}")
    console.print(f"run_count={summary.run_count}")
    console.print(f"fixture_total={run_record.fixture_counts['total']}")
    console.print(f"fixture_pass={run_record.fixture_counts['pass']}")
    console.print(f"fixture_fail={run_record.fixture_counts['fail']}")
    console.print(f"fixture_pending={run_record.fixture_counts['pending']}")
    console.print(f"fixture_skipped={run_record.fixture_counts['skipped']}")
    console.print(f"artifact_count={summary.generated_artifact_count}")
    console.print(f"search_performed_any={str(summary.search_performed_any).lower()}")
    console.print(f"cuda_used_any={str(summary.cuda_used_any).lower()}")
    console.print(f"scoring_used_any={str(summary.scoring_used_any).lower()}")
    if summary.warnings and not allow_warnings:
        raise typer.Exit(1)


@result_store_app.command("validate")
def result_store_validate(
    results_dir: Path = typer.Option(DEFAULT_STAGE2B_RESULT_STORE_DIR, "--results-dir", help="Generated result-store directory."),
    sqlite: Path = typer.Option(DEFAULT_STAGE2B_SQLITE, "--sqlite", help="Generated SQLite result-store path."),
) -> None:
    """Validate JSONL and SQLite result-store outputs."""
    errors = validate_result_store(_resolve_output_path(results_dir), _resolve_output_path(sqlite))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Result-store validation OK")


@result_store_app.command("summary")
def result_store_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE2B_RESULT_STORE_DIR, "--results-dir", help="Generated result-store directory."),
) -> None:
    """Print generated result-store summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_result_store_summary(resolved)
    for key in [
        "summary_id",
        "run_count",
        "pass_count",
        "fail_count",
        "partial_count",
        "pending_count",
        "skipped_count",
        "error_count",
        "canonical_corpus_active_any",
        "search_performed_any",
        "scoring_used_any",
        "cuda_used_any",
        "generated_artifact_count",
        "jsonl_path",
        "sqlite_database_path",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    sqlite_path = resolved / "results.sqlite3"
    if sqlite_path.is_file():
        counts = table_counts(sqlite_path)
        console.print(f"sqlite_run_count={counts.get('runs')}")
        console.print(f"sqlite_event_count={counts.get('events')}")
        console.print(f"sqlite_artifact_count={counts.get('artifacts')}")
    run_records_path = resolved / "run_records.jsonl"
    if run_records_path.is_file():
        first_record = json.loads(run_records_path.read_text(encoding="utf-8").splitlines()[0])
        fixture_counts = first_record.get("fixture_counts", {})
        console.print(f"fixture_total={fixture_counts.get('total')}")
        console.print(f"fixture_pass={fixture_counts.get('pass')}")
        console.print(f"fixture_fail={fixture_counts.get('fail')}")
        console.print(f"fixture_pending={fixture_counts.get('pending')}")
        console.print(f"fixture_skipped={fixture_counts.get('skipped')}")


@result_store_app.command("stage2b-smoke")
def stage2b_smoke(
    solved_baseline_manifest: Path = typer.Option(
        DEFAULT_SOLVED_BASELINE_MANIFEST,
        "--solved-baseline-manifest",
        help="Stage 2A solved-baseline manifest.",
    ),
    result_store_manifest: Path = typer.Option(
        DEFAULT_RESULT_STORE_MANIFEST,
        "--result-store-manifest",
        help="Stage 2B result-store import manifest.",
    ),
    solved_baseline_out_dir: Path = typer.Option(
        DEFAULT_STAGE2A_RESULTS_DIR,
        "--solved-baseline-out-dir",
        help="Generated Stage 2A solved-baseline output directory.",
    ),
    result_store_out_dir: Path = typer.Option(
        DEFAULT_STAGE2B_RESULT_STORE_DIR,
        "--result-store-out-dir",
        help="Generated Stage 2B result-store output directory.",
    ),
    replace: bool = typer.Option(False, "--replace", help="Replace duplicate run_id rows in SQLite."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run Stage 2B solved-baseline result-store import smoke."""
    solved_baseline_dir = _resolve_output_path(solved_baseline_out_dir)
    if not (solved_baseline_dir / "summary.json").is_file() or not (
        solved_baseline_dir / "manifest_run_records.jsonl"
    ).is_file():
        stage2a_smoke(
            manifest=solved_baseline_manifest,
            candidate_dir=None,
            out_dir=solved_baseline_out_dir,
            allow_warnings=allow_warnings,
        )
    result_store_validate_manifest(manifest=result_store_manifest)
    result_store_import_solved_baseline(
        manifest=result_store_manifest,
        solved_baseline_results=solved_baseline_out_dir,
        out_dir=result_store_out_dir,
        replace=replace,
        allow_warnings=allow_warnings,
    )
    result_store_validate(
        results_dir=result_store_out_dir,
        sqlite=_resolve_output_path(result_store_out_dir) / "results.sqlite3",
    )
    result_store_summary(results_dir=result_store_out_dir)
    console.print("Stage 2B smoke OK")


app.add_typer(result_store_app, name="result-store")


def _print_consistency_suite(suite) -> None:
    console.print(f"suite_id={suite.suite_id}")
    console.print(f"check_count={suite.check_count}")
    console.print(f"pass_count={suite.pass_count}")
    console.print(f"fail_count={suite.fail_count}")
    console.print(f"warning_count={suite.warning_count}")
    console.print(f"skipped_count={suite.skipped_count}")
    for result in suite.results:
        if result.is_failure:
            console.print(f"[red]{result.check_group}:{result.check_name}: {result.message}[/red]")
        elif result.is_warning:
            console.print(f"[yellow]{result.check_group}:{result.check_name}: {result.message}[/yellow]")


def _run_consistency_cli(
    groups: list[str],
    *,
    out: Path | None = None,
    allow_warnings: bool = False,
    allow_missing_generated: bool = True,
) -> None:
    output_path = _resolve_output_path(out) if out is not None else None
    suite = run_consistency_suite(
        groups,
        out=output_path,
        allow_missing_generated=allow_missing_generated,
    )
    _print_consistency_suite(suite)
    if output_path is not None:
        console.print(f"summary={output_path}")
    if suite.has_failures:
        raise typer.Exit(1)
    if suite.has_warnings and not allow_warnings:
        raise typer.Exit(1)
    console.print("Consistency checks OK")


@consistency_app.command("check-all")
def consistency_check_all(
    out: Path | None = typer.Option(None, "--out", help="Generated consistency summary JSON path."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run all raw-data-free Stage 2D consistency checks."""
    _run_consistency_cli(
        ["registry", "manifests", "schemas", "docs", "ignored_outputs", "result_store"],
        out=out,
        allow_warnings=allow_warnings,
        allow_missing_generated=True,
    )


@consistency_app.command("check-registry")
def consistency_check_registry(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run transform-registry consistency checks."""
    _run_consistency_cli(["registry"], allow_warnings=allow_warnings)


@consistency_app.command("check-manifests")
def consistency_check_manifests(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run solved-baseline and result-store manifest consistency checks."""
    _run_consistency_cli(["manifests"], allow_warnings=allow_warnings)


@consistency_app.command("check-schemas")
def consistency_check_schemas(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run schema consistency checks."""
    _run_consistency_cli(["schemas"], allow_warnings=allow_warnings)


@consistency_app.command("check-docs")
def consistency_check_docs(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run public documentation consistency checks."""
    _run_consistency_cli(["docs"], allow_warnings=allow_warnings)


@consistency_app.command("check-ignored-outputs")
def consistency_check_ignored_outputs(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run ignored-output policy consistency checks."""
    _run_consistency_cli(["ignored_outputs"], allow_warnings=allow_warnings)


@consistency_app.command("check-result-store")
def consistency_check_result_store(
    allow_missing_generated: bool = typer.Option(
        False,
        "--allow-missing-generated",
        help="Return success if local generated result-store outputs are absent.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run result-store consistency checks."""
    _run_consistency_cli(
        ["result_store"],
        allow_warnings=allow_warnings,
        allow_missing_generated=allow_missing_generated,
    )


app.add_typer(consistency_app, name="consistency")


DEFAULT_EXPLORATORY_MANIFEST_DIR = Path("experiments/manifests/exploratory")
DEFAULT_STAGE2E_DRY_RUN_DIR = Path("experiments/results/exploratory-dry-runs/stage2e")


@experiment_app.command("validate-exploratory")
def experiment_validate_exploratory(
    manifest: Path = typer.Option(..., "--manifest", help="Exploratory experiment manifest path."),
) -> None:
    """Validate a Stage 2E exploratory experiment manifest without execution."""
    try:
        loaded = load_exploratory_manifest(_resolve_existing_path(manifest, "Exploratory manifest"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Exploratory manifest validation OK")
    console.print(f"manifest_id={loaded.manifest_id}")
    console.print(f"manifest_sha256={loaded.sha256}")
    console.print(f"dry_run_only={str(loaded.payload['dry_run_only']).lower()}")
    console.print(f"execution_enabled={str(loaded.payload['execution_enabled']).lower()}")
    console.print(f"search_execution_enabled={str(loaded.payload['search_execution_enabled']).lower()}")
    console.print(f"candidate_generation_enabled={str(loaded.payload['candidate_generation_enabled']).lower()}")
    console.print(f"scoring_enabled={str(loaded.payload['scoring_enabled']).lower()}")
    console.print(f"cuda_enabled={str(loaded.payload['cuda_enabled']).lower()}")


@experiment_app.command("dry-run")
def experiment_dry_run(
    manifest: Path = typer.Option(..., "--manifest", help="Exploratory experiment manifest path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2E_DRY_RUN_DIR, "--out-dir", help="Generated dry-run output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build a dry-run plan for one exploratory manifest without executing it."""
    try:
        plan = build_dry_run_plan(
            _resolve_existing_path(manifest, "Exploratory manifest"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_dry_run_outputs(_resolve_output_path(out_dir), plan)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"plan_id={plan.plan_id}")
    console.print(f"manifest_id={plan.manifest_id}")
    console.print(f"candidate_count_estimate={plan.candidate_count_estimate}")
    console.print(f"candidate_count_upper_bound={plan.candidate_count_upper_bound}")
    pass_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "pass")
    fail_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "fail")
    console.print(f"safety_gate_pass_count={pass_count}")
    console.print(f"safety_gate_fail_count={fail_count}")
    console.print(f"execution_enabled={str(plan.execution_enabled).lower()}")
    console.print(f"search_execution_enabled={str(plan.search_execution_enabled).lower()}")
    console.print(f"scoring_enabled={str(plan.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(plan.cuda_enabled).lower()}")
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)


@experiment_app.command("stage2e-dry-run-all")
def experiment_stage2e_dry_run_all(
    manifest_dir: Path = typer.Option(
        DEFAULT_EXPLORATORY_MANIFEST_DIR,
        "--manifest-dir",
        help="Directory containing Stage 2E exploratory manifests.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE2E_DRY_RUN_DIR, "--out-dir", help="Generated dry-run output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build dry-run plans for every Stage 2E exploratory manifest."""
    resolved_manifest_dir = _resolve_output_path(manifest_dir)
    resolved_out_dir = _resolve_output_path(out_dir)
    plans = []
    for manifest in sorted(resolved_manifest_dir.glob("*-dry-run.yaml")):
        try:
            plan = build_dry_run_plan(manifest, out_dir=resolved_out_dir)
        except (FileNotFoundError, ValueError) as error:
            console.print(f"[red]{manifest}: {error}[/red]")
            raise typer.Exit(1) from error
        write_dry_run_outputs(resolved_out_dir, plan)
        plans.append(plan)
        console.print(f"{plan.manifest_id}={plan.candidate_count_estimate}")
    summary_path = write_dry_run_summary(resolved_out_dir, plans)
    warning_count = sum(len(plan.warnings) for plan in plans)
    console.print(f"summary={summary_path}")
    console.print(f"manifest_count={len(plans)}")
    console.print(f"dry_run_plan_count={len(plans)}")
    console.print(f"candidate_count_total={sum(plan.candidate_count_estimate for plan in plans)}")
    console.print(f"warning_count={warning_count}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@experiment_app.command("dry-run-summary")
def experiment_dry_run_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE2E_DRY_RUN_DIR, "--results-dir", help="Generated dry-run result directory."),
) -> None:
    """Print generated exploratory dry-run summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_dry_run_summary(resolved)
    records = load_plan_records(resolved)
    for key in [
        "plan_count",
        "candidate_count_total",
        "safety_gate_pass_count",
        "safety_gate_fail_count",
        "execution_enabled_any",
        "search_execution_enabled_any",
        "scoring_enabled_any",
        "cuda_enabled_any",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for record in records:
        console.print(f"{record['manifest_id']}={record['candidate_count_estimate']}")


app.add_typer(experiment_app, name="experiment")


DEFAULT_CPU_EXECUTION_MANIFEST_DIR = Path("experiments/manifests/cpu-execution")
DEFAULT_STAGE2F_EXECUTION_DIR = Path("experiments/results/cpu-execution/stage2f")


@execution_app.command("validate")
def execution_validate(
    manifest: Path = typer.Option(..., "--manifest", help="CPU execution manifest path."),
) -> None:
    """Validate a Stage 2F CPU execution manifest."""
    try:
        loaded = load_cpu_execution_manifest(_resolve_existing_path(manifest, "CPU execution manifest"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("CPU execution manifest validation OK")
    console.print(f"manifest_id={loaded.manifest_id}")
    console.print(f"manifest_sha256={loaded.sha256}")
    console.print(f"execution_scope={loaded.execution_scope}")
    console.print(f"unsolved_execution_allowed={str(loaded.payload['unsolved_execution_allowed']).lower()}")
    console.print(f"search_execution_enabled={str(loaded.payload['search_execution_enabled']).lower()}")
    console.print(f"candidate_generation_enabled={str(loaded.payload['candidate_generation_enabled']).lower()}")
    console.print(f"scoring_enabled={str(loaded.payload['scoring_enabled']).lower()}")
    console.print(f"cuda_enabled={str(loaded.payload['cuda_enabled']).lower()}")


@execution_app.command("plan")
def execution_plan(
    manifest: Path = typer.Option(..., "--manifest", help="CPU execution manifest path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--out-dir",
        help="Generated CPU execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build a safety-checked CPU execution plan without running it."""
    try:
        plan = build_execution_plan(
            _resolve_existing_path(manifest, "CPU execution manifest"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_execution_outputs(
        _resolve_output_path(out_dir),
        plan,
        [],
        {"record_type": "cpu_execution_summary", "manifest_id": plan.manifest_id, "result_count": 0},
    )
    console.print(f"execution_plan={paths['execution_plan']}")
    _print_execution_plan_summary(plan)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)


@execution_app.command("run")
def execution_run(
    manifest: Path = typer.Option(..., "--manifest", help="CPU execution manifest path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--out-dir",
        help="Generated CPU execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run one safe Stage 2F CPU execution manifest."""
    try:
        plan, results, summary = run_cpu_execution_manifest(
            _resolve_existing_path(manifest, "CPU execution manifest"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_execution_outputs(_resolve_output_path(out_dir), plan, results, summary)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    _print_execution_run_summary(plan, summary)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)
    if summary.get("fail_count") or summary.get("error_count"):
        raise typer.Exit(1)


@execution_app.command("stage2f-run-all")
def execution_stage2f_run_all(
    manifest_dir: Path = typer.Option(
        DEFAULT_CPU_EXECUTION_MANIFEST_DIR,
        "--manifest-dir",
        help="Directory containing Stage 2F CPU execution manifests.",
    ),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--out-dir",
        help="Generated CPU execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run all safe Stage 2F CPU execution manifests and report blocked controls."""
    resolved_manifest_dir = _resolve_output_path(manifest_dir)
    resolved_out_dir = _resolve_output_path(out_dir)
    summaries = []
    blocked_count = 0
    safe_count = 0
    warning_count = 0
    for manifest in sorted(resolved_manifest_dir.glob("*.yaml")):
        text = manifest.read_text(encoding="utf-8")
        is_expected_failure = "expected_validation_status: fail" in text
        try:
            plan, results, summary = run_cpu_execution_manifest(manifest, out_dir=resolved_out_dir)
        except (FileNotFoundError, ValueError) as error:
            if is_expected_failure:
                blocked_count += 1
                console.print(f"{manifest.name}=blocked")
                console.print(f"{manifest.name}_reason={error}")
                continue
            console.print(f"[red]{manifest}: {error}[/red]")
            raise typer.Exit(1) from error
        if is_expected_failure:
            console.print(f"[red]{manifest}: expected failure unexpectedly ran.[/red]")
            raise typer.Exit(1)
        write_execution_outputs(resolved_out_dir, plan, results, summary)
        summaries.append(summary)
        safe_count += 1
        warning_count += len(plan.warnings)
        console.print(f"{plan.manifest_id}=pass_count:{summary.get('pass_count')}")
    summary_path = write_execution_aggregate_summary(resolved_out_dir, summaries)
    console.print(f"summary={summary_path}")
    console.print(f"safe_manifest_count={safe_count}")
    console.print(f"blocked_manifest_count={blocked_count}")
    console.print(f"execution_result_count={sum(int(item.get('result_count', 0)) for item in summaries)}")
    console.print(f"pass_count={sum(int(item.get('pass_count', 0)) for item in summaries)}")
    console.print(f"fail_count={sum(int(item.get('fail_count', 0)) for item in summaries)}")
    console.print(f"error_count={sum(int(item.get('error_count', 0)) for item in summaries)}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@execution_app.command("summary")
def execution_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--results-dir",
        help="Generated CPU execution result directory.",
    ),
) -> None:
    """Print generated Stage 2F execution summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_execution_summary(resolved)
    records = load_execution_result_records(resolved)
    for key in [
        "manifest_count",
        "result_count",
        "pass_count",
        "fail_count",
        "error_count",
        "skipped_count",
        "search_performed_any",
        "candidate_generation_performed_any",
        "scoring_used_any",
        "cuda_used_any",
        "unsolved_execution_allowed_any",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for record in records:
        console.print(f"{record['manifest_id']}={record['match_status']}")


def _print_execution_plan_summary(plan) -> None:
    pass_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "pass")
    fail_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "fail")
    console.print(f"plan_id={plan.plan_id}")
    console.print(f"manifest_id={plan.manifest_id}")
    console.print(f"execution_scope={plan.execution_scope}")
    console.print(f"safety_gate_pass_count={pass_count}")
    console.print(f"safety_gate_fail_count={fail_count}")
    console.print(f"search_execution_enabled={str(plan.search_execution_enabled).lower()}")
    console.print(f"candidate_generation_enabled={str(plan.candidate_generation_enabled).lower()}")
    console.print(f"scoring_enabled={str(plan.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(plan.cuda_enabled).lower()}")


def _print_execution_run_summary(plan, summary: dict) -> None:
    _print_execution_plan_summary(plan)
    console.print(f"result_count={summary.get('result_count')}")
    console.print(f"pass_count={summary.get('pass_count')}")
    console.print(f"fail_count={summary.get('fail_count')}")
    console.print(f"error_count={summary.get('error_count')}")


app.add_typer(execution_app, name="execution")


DEFAULT_STAGE2G_PROPOSAL_DIR = Path("experiments/proposals/stage2g")
DEFAULT_STAGE2G_REVIEW_DIR = Path("experiments/results/proposal-reviews/stage2g")


@proposal_app.command("validate")
def proposal_validate(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
) -> None:
    """Validate a Stage 2G experiment proposal without execution."""
    try:
        loaded = load_experiment_proposal(_resolve_existing_path(proposal, "Experiment proposal"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Experiment proposal validation OK")
    console.print(f"proposal_id={loaded.proposal_id}")
    console.print(f"proposal_sha256={loaded.sha256}")
    console.print("execution_enabled=false")
    console.print("approved_for_execution=false")
    console.print("search_execution_enabled=false")
    console.print("candidate_generation_enabled=false")
    console.print("scoring_enabled=false")
    console.print("cuda_enabled=false")


@proposal_app.command("review-packet")
def proposal_review_packet(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2G_REVIEW_DIR, "--out-dir", help="Generated review packet output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite review warnings."),
) -> None:
    """Generate a human-review packet without executing the proposal."""
    try:
        loaded = load_experiment_proposal(_resolve_existing_path(proposal, "Experiment proposal"))
        output_dir = _resolve_output_path(out_dir)
        packet = build_review_packet(loaded, out_dir=output_dir)
        paths = write_review_packet_outputs(output_dir, packet)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"packet_id={packet.packet_id}")
    console.print(f"proposal_id={packet.proposal_id}")
    console.print(f"approval_status={packet.approval_status}")
    console.print(f"approved_for_execution={str(packet.approved_for_execution).lower()}")
    console.print(f"execution_blocked={str(packet.execution_blocked).lower()}")
    if packet.warnings and not allow_warnings:
        console.print("[red]Review packet produced warnings.[/red]")
        raise typer.Exit(1)


@proposal_app.command("check-approval")
def proposal_check_approval(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
) -> None:
    """Check whether a proposal has a valid approval record."""
    try:
        loaded = load_experiment_proposal(_resolve_existing_path(proposal, "Experiment proposal"))
        approval_record = load_approval_record(_resolve_existing_path(approval, "Approval record")) if approval else None
        gate = evaluate_approval_gate(loaded, approval_record)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"proposal_id={gate.proposal_id}")
    console.print(f"approval_status={gate.approval_status}")
    console.print(f"approved_for_execution={str(gate.approved_for_execution).lower()}")
    console.print(f"execution_blocked={str(gate.execution_blocked).lower()}")
    console.print(f"reason={gate.reason}")


@proposal_app.command("stage2g-review-all")
def proposal_stage2g_review_all(
    proposal_dir: Path = typer.Option(DEFAULT_STAGE2G_PROPOSAL_DIR, "--proposal-dir", help="Directory containing Stage 2G proposals."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2G_REVIEW_DIR, "--out-dir", help="Generated review packet output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite review warnings."),
) -> None:
    """Validate and review all Stage 2G proposal examples without execution."""
    resolved_dir = _resolve_output_path(proposal_dir)
    output_dir = _resolve_output_path(out_dir)
    packets = []
    warning_count = 0
    for proposal_path in sorted(resolved_dir.glob("*.yaml")):
        try:
            loaded = load_experiment_proposal(proposal_path)
            packet = build_review_packet(loaded, out_dir=output_dir)
            write_review_packet_outputs(output_dir, packet)
        except ValueError as error:
            console.print(f"[red]{proposal_path.name}: {error}[/red]")
            raise typer.Exit(1) from error
        packets.append(packet)
        warning_count += len(packet.warnings)
        console.print(f"{loaded.proposal_id}=blocked:{str(packet.execution_blocked).lower()}")
    summary_path = write_review_packet_summary(output_dir, packets)
    console.print(f"summary={summary_path}")
    console.print(f"proposal_count={len(packets)}")
    console.print(f"review_packet_count={len(packets)}")
    console.print(f"blocked_count={sum(1 for packet in packets if packet.execution_blocked)}")
    console.print(f"approved_count={sum(1 for packet in packets if packet.approved_for_execution)}")
    if warning_count and not allow_warnings:
        console.print("[red]Stage 2G review packets produced warnings.[/red]")
        raise typer.Exit(1)


@proposal_app.command("review-summary")
def proposal_review_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE2G_REVIEW_DIR, "--results-dir", help="Generated review packet directory."),
) -> None:
    """Print generated Stage 2G proposal review summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_review_packet_summary(resolved)
    packets = load_review_packets(resolved)
    for key in [
        "packet_count",
        "blocked_count",
        "approved_count",
        "pending_or_missing_count",
        "denied_count",
    ]:
        console.print(f"{key}={summary.get(key, 0)}")
    console.print(f"review_packet_records={len(packets)}")


app.add_typer(proposal_app, name="proposal")


DEFAULT_STAGE2H_REQUEST_DIR = Path("experiments/proposals/stage2h")
DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR = Path("experiments/results/approval-gated-execution/stage2h")


@approval_execution_app.command("validate")
def approval_execution_validate(
    request: Path = typer.Option(..., "--request", help="Approval-gated execution request path."),
) -> None:
    """Validate a Stage 2H approval-gated execution request."""
    try:
        loaded = load_approval_execution_request(_resolve_existing_path(request, "Approval execution request"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Approval-gated execution request validation OK")
    console.print(f"request_id={loaded.request_id}")
    console.print(f"request_sha256={loaded.sha256}")
    console.print(f"execution_scope={loaded.execution_scope}")
    console.print("unsolved_execution_allowed=false")
    console.print("search_execution_enabled=false")
    console.print("candidate_generation_enabled=false")
    console.print("scoring_enabled=false")
    console.print("cuda_enabled=false")


@approval_execution_app.command("plan")
def approval_execution_plan(
    request: Path = typer.Option(..., "--request", help="Approval-gated execution request path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--out-dir",
        help="Generated approval-gated execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build an approval-gated execution plan without running it."""
    try:
        plan = build_approval_execution_plan(
            _resolve_existing_path(request, "Approval execution request"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_approval_execution_outputs(_resolve_output_path(out_dir), plan, None)
    console.print(f"plan={paths['plan']}")
    _print_approval_execution_plan_summary(plan)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)


@approval_execution_app.command("run")
def approval_execution_run(
    request: Path = typer.Option(..., "--request", help="Approval-gated execution request path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--out-dir",
        help="Generated approval-gated execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run one Stage 2H approval-gated safe request or write a blocked result."""
    try:
        plan, result = run_approval_execution_request(
            _resolve_existing_path(request, "Approval execution request"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_approval_execution_outputs(_resolve_output_path(out_dir), plan, result)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    _print_approval_execution_run_summary(plan, result)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)
    if result.execution_status in {"fail", "error"}:
        raise typer.Exit(1)


@approval_execution_app.command("stage2h-run-all")
def approval_execution_stage2h_run_all(
    request_dir: Path = typer.Option(
        DEFAULT_STAGE2H_REQUEST_DIR,
        "--request-dir",
        help="Directory containing Stage 2H approval-gated requests.",
    ),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--out-dir",
        help="Generated approval-gated execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run all Stage 2H approval-gated requests and report blocked controls."""
    resolved_request_dir = _resolve_output_path(request_dir)
    resolved_out_dir = _resolve_output_path(out_dir)
    results = []
    warning_count = 0
    for request_path in sorted(resolved_request_dir.glob("*-request.yaml")):
        try:
            plan, result = run_approval_execution_request(request_path, out_dir=resolved_out_dir)
        except (FileNotFoundError, ValueError) as error:
            console.print(f"[red]{request_path.name}: {error}[/red]")
            raise typer.Exit(1) from error
        write_approval_execution_outputs(resolved_out_dir, plan, result)
        results.append(result)
        warning_count += len(plan.warnings)
        console.print(f"{plan.request_id}={result.execution_status}")
    summary_path = write_approval_execution_summary(resolved_out_dir, results)
    console.print(f"summary={summary_path}")
    console.print(f"request_count={len(results)}")
    console.print(f"approved_synthetic_pass_count={sum(1 for item in results if item.execution_scope == 'synthetic_only' and item.execution_status == 'pass')}")
    console.print(f"approved_solved_pass_count={sum(1 for item in results if item.execution_scope == 'solved_fixture_only' and item.execution_status == 'pass')}")
    console.print(f"blocked_noop_real_count={sum(1 for item in results if item.execution_scope == 'no_op_review_only' and item.execution_status in {'blocked', 'skipped'})}")
    console.print(f"failed_count={sum(1 for item in results if item.execution_status in {'fail', 'error'})}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@approval_execution_app.command("summary")
def approval_execution_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--results-dir",
        help="Generated approval-gated execution result directory.",
    ),
) -> None:
    """Print generated Stage 2H approval-gated execution summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_approval_execution_summary(resolved)
    records = load_approval_execution_result_records(resolved)
    for key in [
        "request_count",
        "execution_result_count",
        "pass_count",
        "fail_count",
        "blocked_count",
        "skipped_count",
        "approved_synthetic_pass_count",
        "approved_solved_pass_count",
        "search_performed_any",
        "candidate_generation_performed_any",
        "scoring_used_any",
        "cuda_used_any",
        "unsolved_execution_allowed_any",
    ]:
        value = summary.get(key, 0)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for record in records:
        console.print(f"{record['request_id']}={record['execution_status']}")


def _print_approval_execution_plan_summary(plan) -> None:
    pass_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "pass")
    fail_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "fail")
    console.print(f"plan_id={plan.plan_id}")
    console.print(f"request_id={plan.request_id}")
    console.print(f"proposal_id={plan.proposal_id}")
    console.print(f"approval_gate_status={plan.approval_gate_status}")
    console.print(f"approved_for_execution={str(plan.approved_for_execution).lower()}")
    console.print(f"execution_scope={plan.execution_scope}")
    console.print(f"safety_gate_pass_count={pass_count}")
    console.print(f"safety_gate_fail_count={fail_count}")
    console.print(f"search_execution_enabled={str(plan.search_execution_enabled).lower()}")
    console.print(f"candidate_generation_enabled={str(plan.candidate_generation_enabled).lower()}")
    console.print(f"scoring_enabled={str(plan.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(plan.cuda_enabled).lower()}")


def _print_approval_execution_run_summary(plan, result) -> None:
    _print_approval_execution_plan_summary(plan)
    console.print(f"execution_performed={str(result.execution_performed).lower()}")
    console.print(f"execution_status={result.execution_status}")
    console.print(f"underlying_execution_result_count={len(result.underlying_execution_result_ids)}")


app.add_typer(approval_execution_app, name="approval-execution")


DEFAULT_STAGE2I_PROPOSAL_DIR = Path("experiments/proposals/stage2i")
DEFAULT_STAGE2I_READINESS_DIR = Path("experiments/results/approval-readiness/stage2i")


@approval_readiness_app.command("validate")
def approval_readiness_validate(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
) -> None:
    """Validate Stage 2I proposal approval readiness without execution."""
    try:
        analysis = analyze_approval_readiness(
            _resolve_existing_path(proposal, "Experiment proposal"),
            approval_path=_resolve_existing_path(approval, "Approval record") if approval else None,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_readiness_analysis(analysis)


@approval_readiness_app.command("human-summary")
def approval_readiness_human_summary(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
) -> None:
    """Print a concise human decision summary without generating outputs."""
    try:
        packet = build_approval_readiness_packet(
            _resolve_existing_path(proposal, "Experiment proposal"),
            approval_path=_resolve_existing_path(approval, "Approval record") if approval else None,
            out_dir=_resolve_output_path(DEFAULT_STAGE2I_READINESS_DIR),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_human_readiness_summary(packet)


@approval_readiness_app.command("inspect-paths")
def approval_readiness_inspect_paths(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
) -> None:
    """Print exact files a reviewer may inspect for a Stage 2I proposal."""
    try:
        proposal_path = _resolve_existing_path(proposal, "Experiment proposal")
        approval_path = _matching_stage2i_pending_approval(proposal_path.parent, proposal_path)
        packet = build_approval_readiness_packet(
            proposal_path,
            approval_path=approval_path,
            out_dir=_resolve_output_path(DEFAULT_STAGE2I_READINESS_DIR),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"proposal_path={packet.proposal_path}")
    console.print(f"proposal_exists={str(Path(packet.proposal_path).is_file()).lower()}")
    console.print(f"approval_path={packet.approval_path}")
    console.print(f"approval_exists={str(Path(packet.approval_path).is_file()).lower()}")
    for key, path in packet.generated_output_preview.items():
        console.print(f"{key}={path}")
        console.print(f"{key}_exists={str(Path(path).is_file()).lower()}")
    for item in packet.corpus_slice.get("metadata_paths", []):
        console.print(f"metadata_path={item['path']}")
        console.print(f"metadata_path_exists={str(item['exists']).lower()}")
        console.print(f"metadata_path_role={item['role']}")


@approval_readiness_app.command("packet")
def approval_readiness_packet(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2I_READINESS_DIR, "--out-dir", help="Generated readiness output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Generate a Stage 2I approval-readiness packet without execution."""
    try:
        packet = build_approval_readiness_packet(
            _resolve_existing_path(proposal, "Experiment proposal"),
            approval_path=_resolve_existing_path(approval, "Approval record") if approval else None,
            out_dir=_resolve_output_path(out_dir),
        )
        paths = write_approval_readiness_outputs(_resolve_output_path(out_dir), packet)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for name, path in paths.items():
        console.print(f"{name}={path}")
    _print_readiness_packet(packet)
    if packet.warnings and not allow_warnings:
        raise typer.Exit(1)


@approval_readiness_app.command("stage2i-review")
def approval_readiness_stage2i_review(
    proposal_dir: Path = typer.Option(
        DEFAULT_STAGE2I_PROPOSAL_DIR,
        "--proposal-dir",
        help="Directory containing Stage 2I proposals.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE2I_READINESS_DIR, "--out-dir", help="Generated readiness output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Generate readiness packets for every Stage 2I proposal."""
    resolved_dir = _resolve_output_path(proposal_dir)
    output_dir = _resolve_output_path(out_dir)
    packets = []
    warning_count = 0
    for proposal_path in sorted(path for path in resolved_dir.glob("*.yaml") if "request" not in path.name):
        approval_path = _matching_stage2i_pending_approval(resolved_dir, proposal_path)
        try:
            packet = build_approval_readiness_packet(proposal_path, approval_path=approval_path, out_dir=output_dir)
            write_approval_readiness_outputs(output_dir, packet)
        except (FileNotFoundError, ValueError) as error:
            console.print(f"[red]{proposal_path.name}: {error}[/red]")
            raise typer.Exit(1) from error
        packets.append(packet)
        warning_count += len(packet.warnings)
        console.print(f"{packet.proposal_id}=approval_status:{packet.approval_status}")
    summary_path = write_approval_readiness_summary(output_dir, packets)
    console.print(f"summary={summary_path}")
    console.print(f"proposal_count={len(packets)}")
    console.print(f"packet_count={len(packets)}")
    console.print(f"pending_count={sum(1 for packet in packets if packet.approval_status == 'pending')}")
    console.print(f"approved_count={sum(1 for packet in packets if packet.approval_status == 'approved')}")
    console.print(f"candidate_count_estimate_total={sum(packet.candidate_count_estimate for packet in packets)}")
    console.print(f"blocking_condition_count={sum(len(packet.blocking_conditions) for packet in packets)}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@approval_readiness_app.command("summary")
def approval_readiness_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2I_READINESS_DIR,
        "--results-dir",
        help="Generated approval-readiness result directory.",
    ),
) -> None:
    """Print generated Stage 2I approval-readiness summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_approval_readiness_summary(resolved)
    packets = load_approval_readiness_packets(resolved)
    for key in [
        "proposal_count",
        "packet_count",
        "pending_count",
        "approved_count",
        "candidate_count_estimate_total",
        "blocking_condition_count",
    ]:
        console.print(f"{key}={summary.get(key, 0)}")
    for packet in packets:
        console.print(f"{packet['proposal_id']}={packet['approval_status']}")
        preview = packet.get("generated_output_preview", {})
        if isinstance(preview, dict) and preview.get("review_markdown"):
            console.print(f"{packet['proposal_id']}_review_markdown={preview['review_markdown']}")


def _matching_stage2i_pending_approval(proposal_dir: Path, proposal_path: Path) -> Path | None:
    expected = proposal_dir / "approval-records" / f"{proposal_path.stem.replace('-review', '-pending-approval')}.yaml"
    if expected.is_file():
        return expected
    candidates = sorted((proposal_dir / "approval-records").glob("*pending-approval.yaml"))
    return candidates[0] if candidates else None


def _print_readiness_analysis(analysis) -> None:
    console.print("Approval-readiness validation OK")
    console.print(f"proposal_id={analysis.proposal.proposal_id}")
    console.print(f"proposal_sha256={analysis.proposal.sha256}")
    console.print(f"readiness_status={analysis.readiness_status}")
    console.print(f"approval_status={analysis.approval_status}")
    console.print(f"real_unsolved_material_touched={str(analysis.real_unsolved_material_touched).lower()}")
    console.print(f"candidate_count_estimate={analysis.candidate_count_estimate}")
    console.print(f"candidate_count_upper_bound={analysis.candidate_count_upper_bound}")
    console.print(f"blocking_condition_count={len(analysis.blocking_conditions)}")
    console.print("execution_enabled=false")
    console.print("approved_for_execution=false")
    console.print("candidate_generation_enabled=false")
    console.print("scoring_enabled=false")
    console.print("cuda_enabled=false")


def _print_readiness_packet(packet) -> None:
    console.print(f"packet_id={packet.packet_id}")
    console.print(f"proposal_id={packet.proposal_id}")
    console.print(f"approval_status={packet.approval_status}")
    console.print(f"approved_for_execution={str(packet.approved_for_execution).lower()}")
    console.print(f"execution_enabled={str(packet.execution_enabled).lower()}")
    console.print(f"candidate_count_estimate={packet.candidate_count_estimate}")
    console.print(f"candidate_count_upper_bound={packet.candidate_count_upper_bound}")
    console.print(f"blocking_condition_count={len(packet.blocking_conditions)}")
    console.print(f"real_unsolved_material_touched={str(packet.real_unsolved_material_touched).lower()}")
    console.print(f"recommended_decision={packet.recommended_decision}")


def _print_human_readiness_summary(packet) -> None:
    console.print(f"proposal_id={packet.proposal_id}")
    console.print(f"approval_status={packet.approval_status}")
    console.print(f"approved_for_execution={str(packet.approved_for_execution).lower()}")
    console.print(f"execution_enabled={str(packet.execution_enabled).lower()}")
    console.print(f"candidate_count={packet.transform_summary['total_candidate_count']}")
    console.print(f"candidate_count_upper_bound={packet.transform_summary['candidate_count_upper_bound']}")
    console.print(f"search_execution_enabled={str(packet.search_execution_enabled).lower()}")
    console.print(f"candidate_generation_enabled={str(packet.candidate_generation_enabled).lower()}")
    console.print(f"scoring_enabled={str(packet.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(packet.cuda_enabled).lower()}")
    console.print(f"blocking_conditions={len(packet.blocking_conditions)}")
    console.print(f"recommended_decision={packet.recommended_decision}")
    for condition in packet.blocking_conditions:
        console.print(f"blocking_condition={condition}")
    for option in packet.decision_options:
        console.print(f"decision_option_{option['option']}={option['decision']}")


app.add_typer(approval_readiness_app, name="approval-readiness")


DEFAULT_STAGE2J_POLICY = Path("experiments/policies/operator-policy-v0.yaml")
DEFAULT_STAGE2J_QUEUE = Path("experiments/queues/stage2j-bounded-cpu-queue.yaml")
DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage2j")
DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3a")
DEFAULT_STAGE3B_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3b")
DEFAULT_STAGE3B_INSPECTION_MD = Path("research-log/2026-05-16-stage-3b-stage3a-lead-inspection.md")
DEFAULT_STAGE3C_CALIBRATION_RESULTS_DIR = Path("experiments/results/scoring-calibration/stage3c")


@bounded_experiment_app.command("validate-policy")
def bounded_experiment_validate_policy(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
) -> None:
    """Validate a standing bounded-experiment operator policy."""
    try:
        loaded = load_operator_policy(_resolve_existing_path(policy, "Operator policy"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Operator policy validation OK")
    console.print(f"policy_id={loaded.policy_id}")
    console.print(f"max_candidate_count={loaded.max_candidate_count}")
    console.print(f"max_estimated_runtime_seconds={loaded.max_estimated_runtime_seconds}")
    console.print(f"max_generated_output_mb={loaded.max_generated_output_mb:g}")


@bounded_experiment_app.command("validate-queue")
def bounded_experiment_validate_queue(
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
) -> None:
    """Validate a bounded experiment queue manifest."""
    try:
        loaded = load_bounded_queue(_resolve_existing_path(queue, "Bounded experiment queue"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Bounded experiment queue validation OK")
    console.print(f"queue_id={loaded.queue_id}")
    console.print(f"policy_id={loaded.policy_id}")
    console.print(f"item_count={len(loaded.items)}")


@bounded_experiment_app.command("check-queue")
def bounded_experiment_check_queue(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
) -> None:
    """Check every queue item against the standing operator policy."""
    try:
        checks = check_bounded_queue_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_bounded_policy_checks(checks)


@bounded_experiment_app.command("run-next")
def bounded_experiment_run_next(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run the next policy-passing bounded experiment item."""
    try:
        checks, results, summary_path = run_next_bounded_experiment(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            _resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_bounded_policy_checks(checks)
    _print_bounded_run_results(results)
    console.print(f"summary={summary_path}")


@bounded_experiment_app.command("run-all")
def bounded_experiment_run_all(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run every policy-passing bounded experiment item and block over-budget items."""
    try:
        checks, results, summary_path = run_all_bounded_experiments(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            _resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_bounded_policy_checks(checks)
    _print_bounded_run_results(results)
    console.print(f"summary={summary_path}")


@bounded_experiment_app.command("summary")
def bounded_experiment_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR,
        "--results-dir",
        help="Generated bounded auto-run results directory.",
    ),
) -> None:
    """Print generated bounded auto-run summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_bounded_experiment_summary(resolved)
    results = load_bounded_experiment_results(resolved)
    for key in [
        "item_count",
        "policy_pass_count",
        "policy_blocked_count",
        "executed_count",
        "deferred_count",
        "blocked_count",
        "result_count",
        "candidate_count_total",
    ]:
        console.print(f"{key}={summary.get(key, 0)}")
    for result in results:
        console.print(f"{result.get('item_id')}={result.get('execution_status')}")


@bounded_run_app.command("run-caesar-affine")
def bounded_run_caesar_affine(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
    item_id: str = typer.Option(
        "stage2j-caesar-affine-first-reviewable-slice",
        "--item-id",
        help="Queue item to run.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
    direction: str = typer.Option("auto", "--direction", help="Transform convention: auto, forward, or reverse."),
) -> None:
    """Run the bounded Stage 3A Caesar plus affine CPU candidate enumeration."""
    try:
        summary = run_caesar_affine_from_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            item_id=item_id,
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
            allow_warnings=allow_warnings,
            direction=direction,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_run_summary(summary)


@bounded_run_app.command("summary")
def bounded_run_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR,
        "--results-dir",
        help="Generated Stage 3A bounded run directory.",
    ),
) -> None:
    """Print the generated Stage 3A bounded run summary."""
    try:
        summary = load_bounded_run_summary(_resolve_output_path(results_dir))
    except FileNotFoundError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_summary_payload(summary)


@bounded_run_app.command("rerank")
def bounded_run_rerank(
    results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--results-dir", help="Existing generated results directory."),
    out_dir: Path = typer.Option(DEFAULT_STAGE3B_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated rerank output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of reranked top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warning-bearing rerank input."),
) -> None:
    """Rerank generated candidates with the current refined minimal triage scorer."""
    try:
        records = load_candidate_records(_resolve_output_path(results_dir))
        reranked = rerank_candidates(records)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    warnings = [] if allow_warnings else []
    top_records = reranked[:top_k]
    original_top = max(records, key=lambda record: float(record.get("score_summary", {}).get("total_score", 0.0)))
    refined_top = top_records[0]
    output_dir = _resolve_output_path(out_dir)
    reranked_path = write_inspection_jsonl(output_dir / "reranked_top_candidates.jsonl", top_records)
    summary_payload = {
        "record_type": "stage3b_rerank_summary",
        "source_results_dir": str(_resolve_output_path(results_dir)),
        "candidate_count": len(records),
        "top_k": len(top_records),
        "original_top": _candidate_cli_summary(original_top),
        "refined_top": _candidate_cli_summary(refined_top),
        "top_candidate_changed": original_top.get("candidate_index") != refined_top.get("candidate_index"),
        "confidence_label": refined_top.get("score_summary", {}).get("confidence_label", "unlabeled"),
        "solve_claim": False,
        "cuda_used": False,
        "generated_outputs_ignored": True,
        "output_paths": {"reranked_top_candidates": str(reranked_path)},
    }
    summary_path = write_inspection_json(output_dir / "rerank_summary.json", summary_payload)
    warning_path = None
    if warnings:
        warning_path = write_inspection_jsonl(output_dir / "warnings.jsonl", [{"record_type": "stage3b_rerank_warning", "warning": warning} for warning in warnings])
    console.print("rerank_executed=true")
    console.print(f"candidate_count={len(records)}")
    console.print(f"original_top_params={json.dumps(original_top.get('transform_parameters', {}), sort_keys=True)}")
    console.print(f"refined_top_params={json.dumps(refined_top.get('transform_parameters', {}), sort_keys=True)}")
    console.print(f"top_candidate_changed={str(summary_payload['top_candidate_changed']).lower()}")
    console.print(f"confidence_label={summary_payload['confidence_label']}")
    console.print(f"reranked_top_candidates={reranked_path}")
    console.print(f"rerank_summary={summary_path}")
    if warning_path:
        console.print(f"warnings={warning_path}")


def _print_stage3a_run_summary(summary) -> None:
    payload = {
        "run_id": summary.run_id,
        "queue_item_id": summary.queue_item_id,
        "input_slice_id": summary.input_slice_id,
        "input_length": summary.input_length,
        "candidate_count": summary.candidate_count,
        "caesar_candidate_count": summary.caesar_candidate_count,
        "affine_candidate_count": summary.affine_candidate_count,
        "top_k_count": summary.top_k_count,
        "top_candidate_score": summary.top_candidate.get("total_score"),
        "top_candidate_length_normalized_score": summary.top_candidate.get("length_normalized_score"),
        "top_candidate_confidence_label": summary.top_candidate.get("confidence_label"),
        "top_candidate_transform_family": summary.top_candidate.get("transform_family"),
        "top_candidate_transform_parameters": json.dumps(summary.top_candidate.get("transform_parameters", {}), sort_keys=True),
        "solve_claim": summary.solve_claim,
    }
    for key, value in payload.items():
        if isinstance(value, bool):
            value = str(value).lower()
        console.print(f"{key}={value}")
    for key, path in summary.output_paths.items():
        console.print(f"{key}={path}")


def _print_stage3a_summary_payload(summary: dict) -> None:
    top = summary.get("top_candidate", {})
    for key in [
        "run_id",
        "queue_item_id",
        "input_slice_id",
        "input_length",
        "candidate_count",
        "caesar_candidate_count",
        "affine_candidate_count",
        "top_k_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"top_candidate_score={top.get('total_score')}")
    console.print(f"top_candidate_length_normalized_score={top.get('length_normalized_score')}")
    console.print(f"top_candidate_confidence_label={top.get('confidence_label')}")
    console.print(f"top_candidate_transform_family={top.get('transform_family')}")
    console.print(f"top_candidate_transform_parameters={json.dumps(top.get('transform_parameters', {}), sort_keys=True)}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@candidate_inspect_app.command("inspect-stage3a")
def candidate_inspect_stage3a(
    results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--results-dir", help="Generated Stage 3A results directory."),
    top_n: int = typer.Option(25, "--top-n", min=1, help="Number of top candidates to inspect."),
    out_markdown: Path = typer.Option(DEFAULT_STAGE3B_INSPECTION_MD, "--out-markdown", help="Committed summary Markdown path."),
) -> None:
    """Inspect Stage 3A leads and write a summary-only Markdown report."""
    try:
        inspection = inspect_results(_resolve_output_path(results_dir), top_n=top_n, rerank=True)
        written = write_inspection_markdown(out_markdown, inspection)
        validate_no_full_dump_in_markdown(written.read_text(encoding="utf-8"))
        payload = validate_summary_payload(to_summary_payload(inspection))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"candidate_count={payload['candidate_count']}")
    console.print(f"top_candidate_transform={payload['top_candidate']['transform_family']}")
    console.print(f"refined_top_transform={payload['refined_top_candidate']['transform_family']}")
    console.print(f"qualitative_label={payload['qualitative_label']}")
    console.print(f"recommendation={payload['recommendation']}")
    console.print(f"markdown={written}")


@candidate_inspect_app.command("summary")
def candidate_inspect_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--results-dir", help="Generated results directory."),
) -> None:
    """Print a concise candidate-inspection summary without full candidate dumps."""
    try:
        inspection = inspect_results(_resolve_output_path(results_dir), top_n=25, rerank=False)
        payload = validate_summary_payload(to_summary_payload(inspection))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"run_id={payload['run_id']}")
    console.print(f"candidate_count={payload['candidate_count']}")
    console.print(f"top_transform_family={payload['top_candidate']['transform_family']}")
    console.print(f"top_transform_parameters={json.dumps(payload['top_candidate']['transform_parameters'], sort_keys=True)}")
    console.print(f"top_score={payload['top_candidate']['total_score']}")
    console.print(f"qualitative_label={payload['qualitative_label']}")
    console.print(f"warning_count={len(payload['warnings'])}")


@scoring_app.command("calibrate")
def scoring_calibrate(
    stage3_results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--stage3-results-dir", help="Generated Stage 3A results directory."),
    stage3b_results_dir: Path = typer.Option(DEFAULT_STAGE3B_BOUNDED_RESULTS_DIR, "--stage3b-results-dir", help="Generated Stage 3B results directory."),
    out_dir: Path = typer.Option(DEFAULT_STAGE3C_CALIBRATION_RESULTS_DIR, "--out-dir", help="Generated calibration output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warning-bearing calibration inputs."),
) -> None:
    """Run Stage 3C scoring calibration against controls and bounded candidates."""
    try:
        result = run_scoring_calibration(
            stage3_results_dir=_resolve_output_path(stage3_results_dir),
            stage3b_results_dir=_resolve_output_path(stage3b_results_dir),
            out_dir=_resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    summary = result.summary
    console.print("calibration_executed=true")
    console.print(f"positive_control_count={summary['positive_control_count']}")
    console.print(f"null_control_count={summary['null_control_count']}")
    console.print(f"negative_control_count={summary['negative_control_count']}")
    console.print(f"candidate_count={summary['candidate_count']}")
    console.print(f"stage3a_top_classification={summary['stage3a_top_classification']}")
    console.print(f"stage3b_top_classification={summary['stage3b_top_classification']}")
    console.print(f"recommended_next_step={summary['recommended_next_step']}")
    for name, path in result.output_paths.items():
        console.print(f"{name}={path}")


@scoring_app.command("crib-check")
def scoring_crib_check(
    text: str = typer.Option(..., "--text", help="Text to check against the tiny crib list."),
    cribs: Path = typer.Option(DEFAULT_CRIBS_PATH, "--cribs", help="Tiny crib-list path."),
) -> None:
    """Run a tiny transparent crib check on inline text."""
    try:
        crib_terms = load_cribs(_resolve_output_path(cribs))
        result = crib_check(text, cribs=crib_terms)
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"crib_hit_count={result['crib_hit_count']}")
    console.print(f"crib_hits={','.join(result['crib_hits'])}")
    console.print("solve_claim=false")


@scoring_app.command("calibration-summary")
def scoring_calibration_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE3C_CALIBRATION_RESULTS_DIR, "--results-dir", help="Generated calibration results directory."),
) -> None:
    """Print a concise generated Stage 3C calibration summary."""
    path = _resolve_output_path(results_dir) / "calibration_summary.json"
    if not path.is_file():
        console.print(f"[red]Missing calibration summary: {path}[/red]")
        raise typer.Exit(1)
    summary = json.loads(path.read_text(encoding="utf-8"))
    console.print(f"calibration_id={summary.get('calibration_id')}")
    console.print(f"positive_control_count={summary.get('positive_control_count')}")
    console.print(f"null_control_count={summary.get('null_control_count')}")
    console.print(f"negative_control_count={summary.get('negative_control_count')}")
    console.print(f"candidate_count={summary.get('candidate_count')}")
    console.print(f"positive_score_range={json.dumps(summary.get('positive_score_range'), sort_keys=True)}")
    console.print(f"null_score_range={json.dumps(summary.get('null_score_range'), sort_keys=True)}")
    console.print(f"negative_score_range={json.dumps(summary.get('negative_score_range'), sort_keys=True)}")
    console.print(f"stage3a_top_classification={summary.get('stage3a_top_classification')}")
    console.print(f"stage3b_top_classification={summary.get('stage3b_top_classification')}")
    console.print(f"recommended_next_step={summary.get('recommended_next_step')}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")


def _candidate_cli_summary(record: dict) -> dict:
    score = dict(record.get("score_summary", {}))
    return {
        "candidate_index": record.get("candidate_index"),
        "transform_family": record.get("transform_family"),
        "transform_parameters": record.get("transform_parameters", {}),
        "total_score": score.get("total_score"),
        "length_normalized_score": score.get("length_normalized_score"),
        "confidence_label": score.get("confidence_label"),
        "output_sha256": record.get("output_sha256"),
    }


def _print_bounded_policy_checks(checks) -> None:
    console.print(f"item_count={len(checks)}")
    console.print(f"policy_pass_count={sum(1 for check in checks if not check.blocking_reasons)}")
    console.print(f"policy_blocked_count={sum(1 for check in checks if check.blocking_reasons)}")
    for check in checks:
        console.print(f"{check.item_id}=policy:{check.status}")
        for reason in check.blocking_reasons:
            console.print(f"{check.item_id}_blocking_reason={reason}")


def _print_bounded_run_results(results) -> None:
    console.print(f"result_count={len(results)}")
    console.print(f"executed_count={sum(1 for result in results if result.execution_performed)}")
    console.print(f"deferred_count={sum(1 for result in results if result.execution_status == 'deferred')}")
    console.print(f"blocked_count={sum(1 for result in results if result.execution_status == 'blocked')}")
    for result in results:
        console.print(f"{result.item_id}=execution:{result.execution_status}")
        if result.deferred_reason:
            console.print(f"{result.item_id}_deferred_reason={result.deferred_reason}")


app.add_typer(bounded_experiment_app, name="bounded-experiment")
app.add_typer(bounded_run_app, name="bounded-run")
app.add_typer(candidate_inspect_app, name="candidate-inspect")
app.add_typer(scoring_app, name="scoring")


@solved_fixture_app.command("list")
def solved_fixture_list(
    fixture_dir: Path = typer.Option(DEFAULT_DIRECT_FIXTURE_DIR, "--fixture-dir", help="Solved fixture directory."),
) -> None:
    """List solved-page fixture IDs and statuses."""
    fixtures = load_fixtures(_resolve_output_path(fixture_dir))
    table = Table("Fixture", "Method", "Status", "In Scope")
    for fixture in fixtures:
        table.add_row(
            fixture.fixture_id,
            fixture.method_family,
            fixture.method_status,
            str(fixture.in_scope_for_stage).lower(),
        )
    console.print(table)
    console.print(f"fixture_count={len(fixtures)}")


@solved_fixture_app.command("validate")
def solved_fixture_validate(
    fixture_dir: Path = typer.Option(DEFAULT_DIRECT_FIXTURE_DIR, "--fixture-dir", help="Solved fixture directory."),
) -> None:
    """Validate solved-page fixture manifests."""
    resolved = _resolve_output_path(fixture_dir)
    errors = validate_fixture_dir(resolved)
    console.print(f"fixture_dir={resolved}")
    console.print(f"validation_error_count={len(errors)}")
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Solved fixture validation OK")


def _ensure_candidate_dir(candidate_dir: Path, *, build_if_missing: bool) -> None:
    manifest = candidate_dir / "corpus_candidate_manifest.json"
    tokens = candidate_dir / "tokens.jsonl"
    if manifest.is_file() and tokens.is_file():
        return
    if not build_if_missing:
        console.print(f"[red]Corpus candidate outputs missing: {candidate_dir}[/red]")
        console.print("Run `libreprimus corpus-candidate stage0e-smoke --transcript data/raw/transcripts/rtkd/liber-primus__transcription--master.txt --out-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate --allow-boundary-warnings --allow-warnings`.")
        raise typer.Exit(2)
    build_rtkd_v0(
        transcript=Path("data/raw/transcripts/rtkd/liber-primus__transcription--master.txt"),
        gematria=DEFAULT_GEMATRIA_PROFILE,
        glyph_variants=DEFAULT_GLYPH_VARIANT_PROFILE,
        separators=DEFAULT_SEPARATOR_GRAMMAR,
        alignment_dir=Path("data/normalized/alignment"),
        out_dir=candidate_dir,
        allow_boundary_warnings=True,
    )


@solved_fixture_app.command("reproduce-direct")
def solved_fixture_reproduce_direct(
    fixture_dir: Path = typer.Option(DEFAULT_DIRECT_FIXTURE_DIR, "--fixture-dir", help="Solved fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    out_dir: Path = typer.Option(DEFAULT_DIRECT_BASELINE_DIR, "--out-dir", help="Generated solved baseline output directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite reproduction warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Reproduce direct-translation solved-page fixtures."""
    fixture_path = _resolve_output_path(fixture_dir)
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=False)
    errors = validate_fixture_dir(fixture_path)
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    records, summary, warnings = reproduce_direct_translation_fixtures(
        fixture_dir=fixture_path,
        candidate_dir=candidate_path,
    )
    paths = write_reproduction_outputs(_resolve_output_path(out_dir), records, summary, warnings)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"fixture_count={summary.fixture_count}")
    console.print(f"pass_count={summary.pass_count}")
    console.print(f"fail_count={summary.fail_count}")
    console.print(f"pending_count={summary.pending_count}")
    console.print(f"skipped_count={summary.skipped_count}")
    console.print(f"direct_translation_pass_count={summary.direct_translation_pass_count}")
    console.print(f"direct_translation_fail_count={summary.direct_translation_fail_count}")
    console.print(f"elapsed_ms={summary.elapsed_ms}")
    if summary.fail_count:
        raise typer.Exit(1)
    if require_all_pass and (summary.pending_count or summary.skipped_count):
        raise typer.Exit(1)
    if (summary.pending_count or summary.skipped_count) and not allow_pending:
        raise typer.Exit(1)
    if warnings and not allow_warnings:
        raise typer.Exit(1)


@solved_fixture_app.command("reproduce-atbash-family")
def solved_fixture_reproduce_atbash_family(
    fixture_dir: Path = typer.Option(DEFAULT_ATBASH_FIXTURE_DIR, "--fixture-dir", help="Atbash-family fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    out_dir: Path = typer.Option(DEFAULT_ATBASH_BASELINE_DIR, "--out-dir", help="Generated Atbash-family solved baseline directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite reproduction warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Reproduce reverse Gematria and rotated reverse Gematria solved-page fixtures."""
    fixture_path = _resolve_output_path(fixture_dir)
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=False)
    errors = validate_fixture_dir(fixture_path)
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    records, summary, warnings = reproduce_atbash_family_fixtures(
        fixture_dir=fixture_path,
        candidate_dir=candidate_path,
    )
    paths = write_reproduction_outputs(_resolve_output_path(out_dir), records, summary, warnings)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"fixture_count={summary.fixture_count}")
    console.print(f"pass_count={summary.pass_count}")
    console.print(f"fail_count={summary.fail_count}")
    console.print(f"pending_count={summary.pending_count}")
    console.print(f"skipped_count={summary.skipped_count}")
    console.print(f"elapsed_ms={summary.elapsed_ms}")
    if summary.fail_count:
        raise typer.Exit(1)
    if require_all_pass and (summary.pending_count or summary.skipped_count):
        raise typer.Exit(1)
    if (summary.pending_count or summary.skipped_count) and not allow_pending:
        raise typer.Exit(1)
    if warnings and not allow_warnings:
        raise typer.Exit(1)


@solved_fixture_app.command("reproduce-vigenere")
def solved_fixture_reproduce_vigenere(
    fixture_dir: Path = typer.Option(DEFAULT_VIGENERE_FIXTURE_DIR, "--fixture-dir", help="Vigenere fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    out_dir: Path = typer.Option(DEFAULT_VIGENERE_BASELINE_DIR, "--out-dir", help="Generated Vigenere solved baseline directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite reproduction warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Reproduce explicit-key Vigenere solved-page fixtures."""
    fixture_path = _resolve_output_path(fixture_dir)
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=False)
    errors = validate_fixture_dir(fixture_path)
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    records, summary, warnings = reproduce_vigenere_fixtures(
        fixture_dir=fixture_path,
        candidate_dir=candidate_path,
    )
    paths = write_reproduction_outputs(_resolve_output_path(out_dir), records, summary, warnings)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"fixture_count={summary.fixture_count}")
    console.print(f"pass_count={summary.pass_count}")
    console.print(f"fail_count={summary.fail_count}")
    console.print(f"pending_count={summary.pending_count}")
    console.print(f"skipped_count={summary.skipped_count}")
    for record in records:
        if record.method_family == "vigenere":
            console.print(
                f"{record.fixture_id}: key_text={record.key_text} "
                f"key_indices={record.key_indices} skip_rule_applied_count={record.skip_rule_applied_count} "
                f"status={record.match_status}"
            )
    console.print(f"elapsed_ms={summary.elapsed_ms}")
    if summary.fail_count:
        raise typer.Exit(1)
    if require_all_pass and (summary.pending_count or summary.skipped_count):
        raise typer.Exit(1)
    if (summary.pending_count or summary.skipped_count) and not allow_pending:
        raise typer.Exit(1)
    if warnings and not allow_warnings:
        raise typer.Exit(1)


@solved_fixture_app.command("reproduce-prime-stream")
def solved_fixture_reproduce_prime_stream(
    fixture_dir: Path = typer.Option(DEFAULT_PRIME_STREAM_FIXTURE_DIR, "--fixture-dir", help="Prime-stream fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    out_dir: Path = typer.Option(DEFAULT_PRIME_STREAM_BASELINE_DIR, "--out-dir", help="Generated prime-stream solved baseline directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite reproduction warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Reproduce prime-minus-one / phi-prime solved-page fixtures."""
    fixture_path = _resolve_output_path(fixture_dir)
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=False)
    errors = validate_fixture_dir(fixture_path)
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    records, summary, warnings = reproduce_prime_stream_fixtures(
        fixture_dir=fixture_path,
        candidate_dir=candidate_path,
    )
    paths = write_reproduction_outputs(_resolve_output_path(out_dir), records, summary, warnings)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"fixture_count={summary.fixture_count}")
    console.print(f"pass_count={summary.pass_count}")
    console.print(f"fail_count={summary.fail_count}")
    console.print(f"pending_count={summary.pending_count}")
    console.print(f"skipped_count={summary.skipped_count}")
    for record in records:
        if record.method_family in {"prime_minus_one_stream", "phi_prime_stream"}:
            payload_status = ",".join(
                str(item.get("match_status")) for item in record.payload_check_results
            ) or "none"
            console.print(
                f"{record.fixture_id}: prime_values_used_count={record.prime_values_used_count} "
                f"stream_values_used_count={record.stream_values_used_count} "
                f"first_prime_values={record.first_prime_values} "
                f"first_stream_values_mod29={record.first_stream_values_mod29} "
                f"skip_rule_applied_count={record.skip_rule_applied_count} "
                f"payload_check_status={payload_status} status={record.match_status}"
            )
    console.print(f"elapsed_ms={summary.elapsed_ms}")
    if summary.fail_count:
        raise typer.Exit(1)
    if require_all_pass and (summary.pending_count or summary.skipped_count):
        raise typer.Exit(1)
    if (summary.pending_count or summary.skipped_count) and not allow_pending:
        raise typer.Exit(1)
    if warnings and not allow_warnings:
        raise typer.Exit(1)


@solved_fixture_app.command("summary")
def solved_fixture_summary(
    results_dir: Path = typer.Option(DEFAULT_DIRECT_BASELINE_DIR, "--results-dir", help="Generated solved baseline directory."),
) -> None:
    """Print generated solved-fixture reproduction summary."""
    summary = load_fixture_summary(_resolve_output_path(results_dir))
    for key in [
        "fixture_set_id",
        "fixture_count",
        "pass_count",
        "fail_count",
        "pending_count",
        "skipped_count",
        "direct_translation_pass_count",
        "direct_translation_fail_count",
        "canonical_corpus_active",
        "page_boundaries_final",
        "elapsed_ms",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


@solved_fixture_app.command("stage1a-smoke")
def stage1a_smoke(
    fixture_dir: Path = typer.Option(DEFAULT_DIRECT_FIXTURE_DIR, "--fixture-dir", help="Solved fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    out_dir: Path = typer.Option(DEFAULT_DIRECT_BASELINE_DIR, "--out-dir", help="Generated solved baseline output directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Run Stage 1A fixture validation and direct-translation reproduction."""
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=True)
    solved_fixture_validate(fixture_dir=fixture_dir)
    solved_fixture_reproduce_direct(
        fixture_dir=fixture_dir,
        candidate_dir=candidate_path,
        out_dir=out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    validation_errors = validate_reproduction_results(_resolve_output_path(out_dir), allow_warnings=allow_warnings)
    if validation_errors:
        for error in validation_errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)


@solved_fixture_app.command("stage1b-smoke")
def stage1b_smoke(
    direct_fixture_dir: Path = typer.Option(DEFAULT_DIRECT_FIXTURE_DIR, "--direct-fixture-dir", help="Direct fixture directory."),
    atbash_fixture_dir: Path = typer.Option(DEFAULT_ATBASH_FIXTURE_DIR, "--atbash-fixture-dir", help="Atbash-family fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    direct_out_dir: Path = typer.Option(DEFAULT_DIRECT_BASELINE_DIR, "--direct-out-dir", help="Generated direct solved baseline directory."),
    atbash_out_dir: Path = typer.Option(DEFAULT_ATBASH_BASELINE_DIR, "--atbash-out-dir", help="Generated Atbash-family solved baseline directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Run Stage 1B direct-regression and Atbash-family fixture reproduction."""
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=True)
    solved_fixture_validate(fixture_dir=direct_fixture_dir)
    solved_fixture_validate(fixture_dir=atbash_fixture_dir)
    solved_fixture_reproduce_direct(
        fixture_dir=direct_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=direct_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    solved_fixture_reproduce_atbash_family(
        fixture_dir=atbash_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=atbash_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    direct_errors = validate_reproduction_results(_resolve_output_path(direct_out_dir), allow_warnings=allow_warnings)
    atbash_errors = validate_reproduction_results(_resolve_output_path(atbash_out_dir), allow_warnings=allow_warnings)
    if direct_errors or atbash_errors:
        for error in direct_errors + atbash_errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    direct_summary = load_fixture_summary(_resolve_output_path(direct_out_dir))
    atbash_summary = load_fixture_summary(_resolve_output_path(atbash_out_dir))
    combined_path = repo_root() / "data/normalized/solved-baselines/stage1b-summary.json"
    write_fixture_json(
        combined_path,
        {
            "record_type": "stage1b_solved_fixture_summary",
            "direct_fixture_count": direct_summary.get("fixture_count"),
            "direct_pass_count": direct_summary.get("pass_count"),
            "atbash_fixture_count": atbash_summary.get("fixture_count"),
            "atbash_pass_count": atbash_summary.get("pass_count"),
            "atbash_fail_count": atbash_summary.get("fail_count"),
            "atbash_pending_count": atbash_summary.get("pending_count"),
            "atbash_skipped_count": atbash_summary.get("skipped_count"),
            "canonical_corpus_active": False,
            "page_boundaries_final": False,
        },
    )
    console.print(f"stage1b_summary={combined_path}")


@solved_fixture_app.command("stage1c-smoke")
def stage1c_smoke(
    direct_fixture_dir: Path = typer.Option(DEFAULT_DIRECT_FIXTURE_DIR, "--direct-fixture-dir", help="Direct fixture directory."),
    atbash_fixture_dir: Path = typer.Option(DEFAULT_ATBASH_FIXTURE_DIR, "--atbash-fixture-dir", help="Atbash-family fixture directory."),
    vigenere_fixture_dir: Path = typer.Option(DEFAULT_VIGENERE_FIXTURE_DIR, "--vigenere-fixture-dir", help="Vigenere fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    direct_out_dir: Path = typer.Option(DEFAULT_DIRECT_BASELINE_DIR, "--direct-out-dir", help="Generated direct solved baseline directory."),
    atbash_out_dir: Path = typer.Option(DEFAULT_ATBASH_BASELINE_DIR, "--atbash-out-dir", help="Generated Atbash-family solved baseline directory."),
    vigenere_out_dir: Path = typer.Option(DEFAULT_VIGENERE_BASELINE_DIR, "--vigenere-out-dir", help="Generated Vigenere solved baseline directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Run Stage 1C direct, Atbash-family, and Vigenere fixture reproduction."""
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=True)
    solved_fixture_validate(fixture_dir=direct_fixture_dir)
    solved_fixture_validate(fixture_dir=atbash_fixture_dir)
    solved_fixture_validate(fixture_dir=vigenere_fixture_dir)
    solved_fixture_reproduce_direct(
        fixture_dir=direct_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=direct_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    solved_fixture_reproduce_atbash_family(
        fixture_dir=atbash_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=atbash_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    solved_fixture_reproduce_vigenere(
        fixture_dir=vigenere_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=vigenere_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    direct_errors = validate_reproduction_results(_resolve_output_path(direct_out_dir), allow_warnings=allow_warnings)
    atbash_errors = validate_reproduction_results(_resolve_output_path(atbash_out_dir), allow_warnings=allow_warnings)
    vigenere_errors = validate_reproduction_results(_resolve_output_path(vigenere_out_dir), allow_warnings=allow_warnings)
    if direct_errors or atbash_errors or vigenere_errors:
        for error in direct_errors + atbash_errors + vigenere_errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    direct_summary = load_fixture_summary(_resolve_output_path(direct_out_dir))
    atbash_summary = load_fixture_summary(_resolve_output_path(atbash_out_dir))
    vigenere_summary = load_fixture_summary(_resolve_output_path(vigenere_out_dir))
    combined_path = repo_root() / "data/normalized/solved-baselines/stage1c-summary.json"
    write_fixture_json(
        combined_path,
        {
            "record_type": "stage1c_solved_fixture_summary",
            "direct_fixture_count": direct_summary.get("fixture_count"),
            "direct_pass_count": direct_summary.get("pass_count"),
            "atbash_fixture_count": atbash_summary.get("fixture_count"),
            "atbash_pass_count": atbash_summary.get("pass_count"),
            "vigenere_fixture_count": vigenere_summary.get("fixture_count"),
            "vigenere_pass_count": vigenere_summary.get("pass_count"),
            "vigenere_fail_count": vigenere_summary.get("fail_count"),
            "vigenere_pending_count": vigenere_summary.get("pending_count"),
            "vigenere_skipped_count": vigenere_summary.get("skipped_count"),
            "canonical_corpus_active": False,
            "page_boundaries_final": False,
        },
    )
    console.print(f"stage1c_summary={combined_path}")


@solved_fixture_app.command("stage1d-smoke")
def stage1d_smoke(
    direct_fixture_dir: Path = typer.Option(DEFAULT_DIRECT_FIXTURE_DIR, "--direct-fixture-dir", help="Direct fixture directory."),
    atbash_fixture_dir: Path = typer.Option(DEFAULT_ATBASH_FIXTURE_DIR, "--atbash-fixture-dir", help="Atbash-family fixture directory."),
    vigenere_fixture_dir: Path = typer.Option(DEFAULT_VIGENERE_FIXTURE_DIR, "--vigenere-fixture-dir", help="Vigenere fixture directory."),
    prime_fixture_dir: Path = typer.Option(DEFAULT_PRIME_STREAM_FIXTURE_DIR, "--prime-fixture-dir", help="Prime-stream fixture directory."),
    candidate_dir: Path = typer.Option(DEFAULT_CORPUS_CANDIDATE_DIR, "--candidate-dir", help="Generated corpus candidate directory."),
    direct_out_dir: Path = typer.Option(DEFAULT_DIRECT_BASELINE_DIR, "--direct-out-dir", help="Generated direct solved baseline directory."),
    atbash_out_dir: Path = typer.Option(DEFAULT_ATBASH_BASELINE_DIR, "--atbash-out-dir", help="Generated Atbash-family solved baseline directory."),
    vigenere_out_dir: Path = typer.Option(DEFAULT_VIGENERE_BASELINE_DIR, "--vigenere-out-dir", help="Generated Vigenere solved baseline directory."),
    prime_out_dir: Path = typer.Option(DEFAULT_PRIME_STREAM_BASELINE_DIR, "--prime-out-dir", help="Generated prime-stream solved baseline directory."),
    allow_pending: bool = typer.Option(False, "--allow-pending", help="Return success with pending fixtures."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
    require_all_pass: bool = typer.Option(False, "--require-all-pass", help="Require every fixture to pass."),
) -> None:
    """Run Stage 1D direct, Atbash-family, Vigenere, and prime-stream fixture reproduction."""
    candidate_path = _resolve_output_path(candidate_dir)
    _ensure_candidate_dir(candidate_path, build_if_missing=True)
    solved_fixture_validate(fixture_dir=direct_fixture_dir)
    solved_fixture_validate(fixture_dir=atbash_fixture_dir)
    solved_fixture_validate(fixture_dir=vigenere_fixture_dir)
    solved_fixture_validate(fixture_dir=prime_fixture_dir)
    solved_fixture_reproduce_direct(
        fixture_dir=direct_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=direct_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    solved_fixture_reproduce_atbash_family(
        fixture_dir=atbash_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=atbash_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    solved_fixture_reproduce_vigenere(
        fixture_dir=vigenere_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=vigenere_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    solved_fixture_reproduce_prime_stream(
        fixture_dir=prime_fixture_dir,
        candidate_dir=candidate_path,
        out_dir=prime_out_dir,
        allow_pending=allow_pending,
        allow_warnings=allow_warnings,
        require_all_pass=require_all_pass,
    )
    direct_errors = validate_reproduction_results(_resolve_output_path(direct_out_dir), allow_warnings=allow_warnings)
    atbash_errors = validate_reproduction_results(_resolve_output_path(atbash_out_dir), allow_warnings=allow_warnings)
    vigenere_errors = validate_reproduction_results(_resolve_output_path(vigenere_out_dir), allow_warnings=allow_warnings)
    prime_errors = validate_reproduction_results(_resolve_output_path(prime_out_dir), allow_warnings=allow_warnings)
    if direct_errors or atbash_errors or vigenere_errors or prime_errors:
        for error in direct_errors + atbash_errors + vigenere_errors + prime_errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    direct_summary = load_fixture_summary(_resolve_output_path(direct_out_dir))
    atbash_summary = load_fixture_summary(_resolve_output_path(atbash_out_dir))
    vigenere_summary = load_fixture_summary(_resolve_output_path(vigenere_out_dir))
    prime_summary = load_fixture_summary(_resolve_output_path(prime_out_dir))
    combined_path = repo_root() / "data/normalized/solved-baselines/stage1d-summary.json"
    write_fixture_json(
        combined_path,
        {
            "record_type": "stage1d_solved_fixture_summary",
            "direct_fixture_count": direct_summary.get("fixture_count"),
            "direct_pass_count": direct_summary.get("pass_count"),
            "atbash_fixture_count": atbash_summary.get("fixture_count"),
            "atbash_pass_count": atbash_summary.get("pass_count"),
            "vigenere_fixture_count": vigenere_summary.get("fixture_count"),
            "vigenere_pass_count": vigenere_summary.get("pass_count"),
            "prime_fixture_count": prime_summary.get("fixture_count"),
            "prime_pass_count": prime_summary.get("pass_count"),
            "prime_fail_count": prime_summary.get("fail_count"),
            "prime_pending_count": prime_summary.get("pending_count"),
            "prime_skipped_count": prime_summary.get("skipped_count"),
            "canonical_corpus_active": False,
            "page_boundaries_final": False,
        },
    )
    console.print(f"stage1d_summary={combined_path}")


app.add_typer(solved_fixture_app, name="solved-fixture")


if __name__ == "__main__":
    app()
