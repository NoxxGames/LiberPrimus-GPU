"""Archive, observation, hash-preimage, and image CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

archive_app = typer.Typer(no_args_is_help=True)
observation_app = typer.Typer(no_args_is_help=True)
hash_preimage_app = typer.Typer(no_args_is_help=True)
image_analysis_app = typer.Typer(no_args_is_help=True)
image_transform_app = typer.Typer(no_args_is_help=True)


@archive_app.command("validate-sources")
def archive_validate_sources(
    records: Path = typer.Option(..., "--records", help="Source archive record YAML path."),
) -> None:
    """Validate Stage 3K source/archive classification records."""
    try:
        count, errors = validate_source_records(_resolve_output_path(records))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"source_record_count={count}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Source archive records OK")


@archive_app.command("scan-local-images")
def archive_scan_local_images(
    source_dir: Path = typer.Option(..., "--source-dir", help="Local page image source directory."),
    lock_out: Path = typer.Option(..., "--lock-out", help="Committed source-lock JSONL output path."),
    artifact_out: Path = typer.Option(..., "--artifact-out", help="Committed image artifact JSONL output path."),
    summary_out: Path = typer.Option(..., "--summary-out", help="Generated scan summary JSON output path."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Write empty outputs if source dir is missing."),
) -> None:
    """Scan local page images and write deterministic source-lock metadata."""
    try:
        summary = scan_local_images(
            source_dir=source_dir,
            lock_out=lock_out,
            artifact_out=artifact_out,
            summary_out=summary_out,
            allow_missing=allow_missing,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("image_scan_executed=true")
    console.print(f"image_count={summary['image_count']}")
    console.print(f"lock_record_count={summary['lock_record_count']}")
    console.print(f"image_artifact_record_count={summary['image_artifact_record_count']}")
    console.print(f"prime_dimension_count={summary['prime_dimension_count']}")
    console.print(f"summary={_resolve_output_path(summary_out)}")


@archive_app.command("validate-image-locks")
def archive_validate_image_locks(
    locks: Path = typer.Option(..., "--locks", help="Source-lock JSONL path."),
    artifacts: Path = typer.Option(..., "--artifacts", help="Image artifact JSONL path."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Allow empty lock/artifact files."),
) -> None:
    """Validate Stage 3K local image lock and artifact records."""
    try:
        lock_count, artifact_count, errors = validate_image_locks(
            locks=_resolve_output_path(locks),
            artifacts=_resolve_output_path(artifacts),
            allow_empty=allow_empty,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"image_lock_record_count={lock_count}")
    console.print(f"image_artifact_record_count={artifact_count}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Image lock records OK")


@observation_app.command("validate-visual")
def observation_validate_visual(
    records: Path = typer.Option(..., "--records", help="Visual observation YAML path."),
) -> None:
    """Validate reviewable visual numeric observation records."""
    try:
        count, errors = validate_visual_records(_resolve_output_path(records))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"visual_observation_count={count}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Visual observation records OK")


@observation_app.command("validate-cookies")
def observation_validate_cookies(
    records: Path = typer.Option(..., "--records", help="Cookie/hash record YAML path."),
) -> None:
    """Validate reviewable cookie/hash artefact records."""
    try:
        count, errors = validate_cookie_records(_resolve_output_path(records))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"cookie_hash_record_count={count}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Cookie/hash records OK")


@observation_app.command("summary")
def observation_summary(
    visual: Path = typer.Option(..., "--visual", help="Visual observation YAML path."),
    cookies: Path = typer.Option(..., "--cookies", help="Cookie/hash record YAML path."),
    sources: Path = typer.Option(..., "--sources", help="Source archive record YAML path."),
) -> None:
    """Print a concise Stage 3K observation registry summary."""
    try:
        summary = summarize_observations(
            visual=_resolve_output_path(visual),
            cookies=_resolve_output_path(cookies),
            sources=_resolve_output_path(sources),
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in summary.items():
        console.print(f"{key}={value}")
    console.print("trusted_as_canonical=false")
    console.print("solve_claim=false")


@hash_preimage_app.command("validate-packs")
def hash_preimage_validate_packs(
    pack_dir: Path = typer.Option(..., "--pack-dir", help="Hash-preimage candidate pack directory."),
) -> None:
    """Validate bounded hash-preimage candidate packs."""
    try:
        resolved = _resolve_output_path(pack_dir)
        count, errors = validate_candidate_packs(resolved)
        packs = load_candidate_packs(resolved)
        expanded = [expand_candidate_pack(pack) for pack in packs] if not errors else []
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"candidate_pack_count={count}")
    console.print(f"validation_error_count={len(errors)}")
    for pack in expanded:
        console.print(
            f"{pack.pack_id}: generated_before_dedup={pack.total_generated_before_dedup} "
            f"candidate_count={len(pack.candidates)} duplicate_count={pack.duplicate_count} "
            f"upper_bound={pack.candidate_count_upper_bound}"
        )
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Hash preimage candidate packs OK")


@hash_preimage_app.command("run")
def hash_preimage_run(
    cookies: Path = typer.Option(..., "--cookies", help="Cookie/hash records YAML path."),
    pack_dir: Path = typer.Option(..., "--pack-dir", help="Hash-preimage candidate pack directory."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated hash-preimage output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow duplicate-candidate warnings."),
) -> None:
    """Run bounded SHA-256 exact-match hash-preimage packs."""
    try:
        summary = run_hash_preimage(
            cookies=_resolve_output_path(cookies),
            pack_dir=_resolve_output_path(pack_dir),
            out_dir=_resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_hash_preimage_summary(summary)


@hash_preimage_app.command("summary")
def hash_preimage_print_summary(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated hash-preimage result directory."),
) -> None:
    """Print a concise generated hash-preimage run summary."""
    try:
        summary = load_hash_preimage_summary(_resolve_output_path(results_dir))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_hash_preimage_summary(summary)


def _print_hash_preimage_summary(summary: dict) -> None:
    for key in [
        "run_id",
        "algorithm",
        "target_cookie_count",
        "pack_count",
        "candidate_count_generated_before_dedup",
        "candidate_count",
        "duplicate_candidate_count",
        "comparison_count",
        "exact_match_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"target_cookie_ids={','.join(summary.get('target_cookie_ids', []))}")
    console.print(f"pack_ids={','.join(summary.get('pack_ids', []))}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    console.print(f"cuda_used={str(summary.get('cuda_used')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@image_analysis_app.command("analyze-local-pages")
def image_analysis_analyze_local_pages(
    source_dir: Path = typer.Option(..., "--source-dir", help="Local page image source directory."),
    image_locks: Path = typer.Option(..., "--image-locks", help="Committed Stage 3K image-lock JSONL path."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated deterministic image-analysis output directory."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Write empty outputs if source dir is missing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite non-blocking warnings."),
) -> None:
    """Analyze local Liber Primus page images with deterministic features only."""
    try:
        summary = analyze_local_pages(
            source_dir=_resolve_output_path(source_dir),
            image_locks=_resolve_output_path(image_locks),
            out_dir=_resolve_output_path(out_dir),
            allow_missing=allow_missing,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_image_analysis_summary(summary)


@image_analysis_app.command("validate-results")
def image_analysis_validate_results(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated image-analysis result directory."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Allow missing generated results."),
) -> None:
    """Validate generated deterministic image-analysis records."""
    try:
        counts, errors = validate_image_analysis_results(
            _resolve_output_path(results_dir),
            allow_missing=allow_missing,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Image analysis results OK")


@image_analysis_app.command("summary")
def image_analysis_print_summary(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated image-analysis result directory."),
) -> None:
    """Print a concise generated deterministic image-analysis summary."""
    try:
        summary = load_image_analysis_summary(_resolve_output_path(results_dir))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_image_analysis_summary(summary)


def _print_image_analysis_summary(summary: dict) -> None:
    for key in [
        "run_id",
        "image_count",
        "threshold_values",
        "component_record_count",
        "symmetry_record_count",
        "bitplane_record_count",
        "threshold_record_count",
        "feature_candidate_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    feature_counts = summary.get("feature_counts", {})
    for feature_name in sorted(feature_counts):
        console.print(f"{feature_name}_count={feature_counts[feature_name]}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    console.print(f"trusted_as_canonical={str(summary.get('trusted_as_canonical')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@image_transform_app.command("run-local-pages")
def image_transform_run_local_pages(
    source_dir: Path = typer.Option(..., "--source-dir", help="Local page image source directory."),
    image_locks: Path = typer.Option(..., "--image-locks", help="Committed Stage 3K image-lock JSONL path."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated deterministic image-transform output directory."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Write empty outputs if source dir is missing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite non-blocking warnings."),
) -> None:
    """Generate deterministic review transforms for local Liber Primus page images."""
    try:
        summary = run_local_page_transforms(
            source_dir=_resolve_output_path(source_dir),
            image_locks=_resolve_output_path(image_locks),
            out_dir=_resolve_output_path(out_dir),
            allow_missing=allow_missing,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_image_transform_summary(summary)


@image_transform_app.command("validate-results")
def image_transform_validate_results(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated image-transform result directory."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Allow missing generated results."),
) -> None:
    """Validate generated deterministic image-transform records."""
    try:
        counts, errors = validate_image_transform_results(
            _resolve_output_path(results_dir),
            allow_missing=allow_missing,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Image transform results OK")


@image_transform_app.command("summary")
def image_transform_print_summary(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated image-transform result directory."),
) -> None:
    """Print a concise generated deterministic image-transform summary."""
    try:
        summary = load_image_transform_summary(_resolve_output_path(results_dir))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_image_transform_summary(summary)


def _print_image_transform_summary(summary: dict) -> None:
    for key in [
        "run_id",
        "image_count",
        "transform_count",
        "derived_image_count",
        "contact_sheet_count",
        "review_page_count",
        "visual_candidate_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    feature_counts = summary.get("feature_counts", {})
    for feature_name in sorted(feature_counts):
        console.print(f"{feature_name}_count={feature_counts[feature_name]}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    console.print(f"trusted_as_canonical={str(summary.get('trusted_as_canonical')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")



def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(archive_app, name="archive")
    root_app.add_typer(observation_app, name="observation")
    root_app.add_typer(hash_preimage_app, name="hash-preimage")
    root_app.add_typer(image_analysis_app, name="image-analysis")
    root_app.add_typer(image_transform_app, name="image-transform")
