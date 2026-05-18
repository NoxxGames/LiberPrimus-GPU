"""Post-Discord experiment CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

post_discord_app = typer.Typer(no_args_is_help=True)


@post_discord_app.command("validate-manifest")
def post_discord_validate_manifest(
    manifest: Path = typer.Option(
        Path(DEFAULT_STAGE3S_ONION7_MANIFEST),
        "--manifest",
        help="EXP-3R-003 post-Discord manifest path.",
    ),
) -> None:
    """Validate the Stage 3S Onion 7 manifest without execution."""
    summary, errors = validate_post_discord_manifest(_resolve_existing_path(manifest, "Stage 3S manifest"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("post_discord_manifest_valid=true")
    for key in [
        "experiment_id",
        "candidate_count_cap",
        "expected_candidate_count",
        "value_spaces",
        "routes",
        "directions",
        "reset_modes",
    ]:
        value = summary.get(key)
        if isinstance(value, list):
            value = ",".join(str(item) for item in value)
        console.print(f"{key}={value}")


@post_discord_app.command("run-onion7-seed-pack")
def post_discord_run_onion7_seed_pack(
    manifest: Path = typer.Option(
        Path(DEFAULT_STAGE3S_ONION7_MANIFEST),
        "--manifest",
        help="EXP-3R-003 post-Discord manifest path.",
    ),
    out_dir: Path = typer.Option(
        Path(DEFAULT_STAGE3S_POST_DISCORD_DIR),
        "--out-dir",
        help="Generated Stage 3S output directory.",
    ),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Top candidate count to export."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Execute only the bounded Stage 3S Onion 7 seed pack."""
    try:
        summary = run_onion7_seed_pack(
            manifest_path=_resolve_existing_path(manifest, "Stage 3S manifest"),
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3s_summary(summary)
    if summary.warnings and not allow_warnings:
        raise typer.Exit(1)


@post_discord_app.command("summary")
def post_discord_summary(
    results_dir: Path = typer.Option(
        Path(DEFAULT_STAGE3S_POST_DISCORD_DIR),
        "--results-dir",
        help="Generated Stage 3S result directory.",
    ),
) -> None:
    """Print a concise Stage 3S post-Discord summary."""
    try:
        payload = load_post_discord_summary(_resolve_output_path(results_dir))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3s_payload(payload)


def _print_stage3s_summary(summary) -> None:
    payload = {
        "run_id": summary.run_id,
        "experiment_id": summary.queue_item_id,
        "input_slice_id": summary.input_slice_id,
        "input_length": summary.input_length,
        "expected_candidate_count": summary.expected_candidate_count,
        "executed_candidate_count": summary.executed_candidate_count,
        "deferred_candidate_count": summary.deferred_candidate_count,
        "candidate_count": summary.candidate_count,
        "value_spaces": ",".join(summary.value_spaces or []),
        "routes": ",".join(summary.routes or []),
        "directions": ",".join(summary.directions or []),
        "reset_modes": ",".join(summary.reset_modes or []),
        "top_value_space": summary.top_candidate.get("value_space"),
        "top_route": summary.top_candidate.get("route"),
        "top_direction": summary.top_candidate.get("direction"),
        "top_reset_mode": summary.top_candidate.get("reset_mode"),
        "top_score": summary.top_candidate.get("total_score"),
        "top_length_normalized_score": summary.top_candidate.get("length_normalized_score"),
        "top_confidence_label": summary.top_candidate.get("calibrated_confidence_label"),
        "warning_count": len(summary.warnings),
        "solve_claim": summary.solve_claim,
    }
    for key, value in payload.items():
        if isinstance(value, bool):
            value = str(value).lower()
        console.print(f"{key}={value}")
    for key, path in summary.output_paths.items():
        console.print(f"{key}={path}")


def _print_stage3s_payload(summary: dict) -> None:
    top = summary.get("top_candidate", {})
    for key in [
        "run_id",
        "queue_item_id",
        "input_slice_id",
        "input_length",
        "expected_candidate_count",
        "executed_candidate_count",
        "deferred_candidate_count",
        "candidate_count",
        "value_spaces",
        "routes",
        "directions",
        "reset_modes",
    ]:
        value = summary.get(key)
        if isinstance(value, list):
            value = ",".join(str(item) for item in value)
        console.print(f"{key}={value}")
    console.print(f"top_value_space={top.get('value_space')}")
    console.print(f"top_route={top.get('route')}")
    console.print(f"top_direction={top.get('direction')}")
    console.print(f"top_reset_mode={top.get('reset_mode')}")
    console.print(f"top_score={top.get('total_score')}")
    console.print(f"top_length_normalized_score={top.get('length_normalized_score')}")
    console.print(f"top_confidence_label={top.get('calibrated_confidence_label')}")
    console.print(f"warning_count={len(summary.get('warnings', []))}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@post_discord_app.command("validate-gp-rune-manifest")
def post_discord_validate_gp_rune_manifest(
    manifest: Path = typer.Option(
        Path(DEFAULT_STAGE3T_GP_RUNE_MANIFEST),
        "--manifest",
        help="EXP-3R-004 GP/rune verifier manifest path.",
    ),
) -> None:
    """Validate the Stage 3T GP/rune verifier manifest without execution."""
    payload, errors = validate_gp_rune_manifest(_resolve_existing_path(manifest, "Stage 3T manifest"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("gp_rune_manifest_valid=true")
    for key in ["experiment_id", "claim_cap", "execution_enabled", "cuda_enabled", "no_solve_claim"]:
        value = payload.get(key)
        if isinstance(value, bool):
            value = str(value).lower()
        console.print(f"{key}={value}")


@post_discord_app.command("run-gp-rune-verifier")
def post_discord_run_gp_rune_verifier(
    manifest: Path = typer.Option(
        Path(DEFAULT_STAGE3T_GP_RUNE_MANIFEST),
        "--manifest",
        help="EXP-3R-004 GP/rune verifier manifest path.",
    ),
    promoted_observations: Path = typer.Option(
        Path(DEFAULT_STAGE3T_PROMOTED_OBSERVATIONS),
        "--promoted-observations",
        help="Stage 3R promoted observation records.",
    ),
    visual_observations: Path = typer.Option(
        Path(DEFAULT_STAGE3T_VISUAL_OBSERVATIONS),
        "--visual-observations",
        help="Committed visual numeric observation records.",
    ),
    out_dir: Path = typer.Option(
        Path(DEFAULT_STAGE3T_POST_DISCORD_DIR),
        "--out-dir",
        help="Generated Stage 3T output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Execute only the bounded Stage 3T GP/rune claim verifier."""
    try:
        summary = run_gp_rune_verifier(
            manifest_path=_resolve_existing_path(manifest, "Stage 3T manifest"),
            promoted_observations_path=_resolve_existing_path(
                promoted_observations,
                "Stage 3R promoted observations",
            ),
            visual_observations_path=_resolve_existing_path(
                visual_observations,
                "visual numeric observations",
            ),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3t_payload(summary)
    if summary.get("warnings") and not allow_warnings:
        raise typer.Exit(1)


@post_discord_app.command("gp-rune-summary")
def post_discord_gp_rune_summary(
    results_dir: Path = typer.Option(
        Path(DEFAULT_STAGE3T_POST_DISCORD_DIR),
        "--results-dir",
        help="Generated Stage 3T result directory.",
    ),
) -> None:
    """Print a concise Stage 3T GP/rune verifier summary."""
    try:
        payload = load_gp_rune_summary(_resolve_output_path(results_dir))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3t_payload(payload)


def _print_stage3t_payload(summary: dict) -> None:
    for key in [
        "run_id",
        "experiment_id",
        "manifest_path",
        "claim_cap",
        "claims_loaded",
        "claims_deduplicated",
        "claims_executed",
        "verified_count",
        "unverified_count",
        "boundary_sensitive_count",
        "missing_source_span_count",
        "unsupported_claim_count",
        "malformed_claim_count",
        "duplicate_claim_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"warning_count={len(summary.get('warnings', []))}")
    console.print(f"no_solve_claim={str(summary.get('no_solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@post_discord_app.command("validate-cookie-manifest")
def post_discord_validate_cookie_manifest(
    manifest: Path = typer.Option(
        Path(DEFAULT_STAGE3U_COOKIE_MANIFEST),
        "--manifest",
        help="EXP-3R-001 cookie signed-variant manifest path.",
    ),
) -> None:
    """Validate the Stage 3U cookie signed-variant manifest without execution."""
    payload, errors = validate_cookie_manifest(_resolve_existing_path(manifest, "Stage 3U manifest"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("cookie_manifest_valid=true")
    for key in [
        "experiment_id",
        "candidate_cap",
        "algorithm",
        "base_string_count",
        "byte_variant_count",
        "generated_before_dedup",
        "execution_enabled",
        "cuda_enabled",
        "no_solve_claim",
    ]:
        value = payload.get(key)
        if isinstance(value, bool):
            value = str(value).lower()
        console.print(f"{key}={value}")


@post_discord_app.command("run-cookie-signed-variants")
def post_discord_run_cookie_signed_variants(
    manifest: Path = typer.Option(
        Path(DEFAULT_STAGE3U_COOKIE_MANIFEST),
        "--manifest",
        help="EXP-3R-001 cookie signed-variant manifest path.",
    ),
    cookies: Path = typer.Option(
        Path(DEFAULT_STAGE3U_COOKIES),
        "--cookies",
        help="Committed cookie/hash records.",
    ),
    out_dir: Path = typer.Option(
        Path(DEFAULT_STAGE3U_POST_DISCORD_DIR),
        "--out-dir",
        help="Generated Stage 3U output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Execute only the bounded Stage 3U cookie signed-variant pack."""
    try:
        summary = run_cookie_signed_variant_pack(
            manifest_path=_resolve_existing_path(manifest, "Stage 3U manifest"),
            cookies_path=_resolve_existing_path(cookies, "cookie records"),
            out_dir=_resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3u_payload(summary)
    if summary.get("warnings") and not allow_warnings:
        raise typer.Exit(1)


@post_discord_app.command("cookie-signed-summary")
def post_discord_cookie_signed_summary(
    results_dir: Path = typer.Option(
        Path(DEFAULT_STAGE3U_POST_DISCORD_DIR),
        "--results-dir",
        help="Generated Stage 3U result directory.",
    ),
) -> None:
    """Print a concise Stage 3U cookie signed-variant summary."""
    try:
        payload = load_cookie_signed_summary(_resolve_output_path(results_dir))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3u_payload(payload)


def _print_stage3u_payload(summary: dict) -> None:
    for key in [
        "run_id",
        "experiment_id",
        "manifest_path",
        "target_cookie_count",
        "base_string_count",
        "byte_variant_count",
        "candidate_count_generated_before_dedup",
        "candidate_count_after_dedup",
        "duplicate_candidate_count",
        "comparison_count",
        "exact_match_count",
        "algorithm",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"warning_count={len(summary.get('warnings', []))}")
    console.print(f"no_solve_claim={str(summary.get('no_solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")



def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(post_discord_app, name="post-discord")
