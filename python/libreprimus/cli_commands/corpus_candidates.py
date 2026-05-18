"""Corpus candidate CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

corpus_candidate_app = typer.Typer(no_args_is_help=True)


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




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(corpus_candidate_app, name="corpus-candidate")
