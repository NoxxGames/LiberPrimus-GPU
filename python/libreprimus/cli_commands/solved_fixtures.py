"""Solved fixture CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *
from libreprimus.cli_commands.corpus_candidates import build_rtkd_v0

solved_fixture_app = typer.Typer(no_args_is_help=True)


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




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(solved_fixture_app, name="solved-fixture")
