"""Profile validation CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

profile_app = typer.Typer(no_args_is_help=True)


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




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(profile_app, name="profile")
