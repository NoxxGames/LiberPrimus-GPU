"""Stage 4A Discord full-review CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.discord_full_review.models import (
    DEFAULT_DISCORD_DIR,
    DEFAULT_LP_PAGES_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PRIVACY_MODE,
)
from libreprimus.discord_full_review.runner import build_discord_full_review, load_generated_summary
from libreprimus.discord_full_review.validation import validate_results
from libreprimus.paths import repo_root

discord_full_review_app = typer.Typer(no_args_is_help=True)
console = Console()


@discord_full_review_app.command("build")
def discord_full_review_build(
    discord_dir: Path = typer.Option(DEFAULT_DISCORD_DIR, "--discord-dir", help="Local ignored Discord HTML directory."),
    lp_pages_dir: Path = typer.Option(DEFAULT_LP_PAGES_DIR, "--lp-pages-dir", help="Local ignored LP page image directory."),
    out_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated Stage 4A output directory."),
    privacy_mode: str = typer.Option(DEFAULT_PRIVACY_MODE, "--privacy-mode", help="Privacy mode; only redacted_public is supported."),
    include_lp_page_gallery: bool = typer.Option(False, "--include-lp-page-gallery", help="Generate LP page image gallery."),
    emit_noindex: bool = typer.Option(True, "--emit-noindex/--no-emit-noindex", help="Emit noindex metadata on generated HTML pages."),
    emit_robots: bool = typer.Option(True, "--emit-robots/--no-emit-robots", help="Emit a robots.txt crawler disallow file."),
    emit_site_manifest: bool = typer.Option(True, "--emit-site-manifest/--no-emit-site-manifest", help="Emit site_manifest.json and site_manifest.md."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build the Stage 4A redacted Discord full-review bundle and static site."""

    try:
        summary = build_discord_full_review(
            discord_dir=_resolve(discord_dir),
            lp_pages_dir=_resolve(lp_pages_dir),
            out_dir=_resolve(out_dir),
            privacy_mode=privacy_mode,
            include_lp_page_gallery=include_lp_page_gallery,
            emit_noindex=emit_noindex,
            emit_robots=emit_robots,
            emit_site_manifest=emit_site_manifest,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI surfaces build failures consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@discord_full_review_app.command("validate")
def discord_full_review_validate(
    results_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--results-dir", help="Generated Stage 4A output directory."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Allow missing generated results."),
) -> None:
    """Validate generated Stage 4A full-review outputs."""

    summary, errors = validate_results(_resolve(results_dir), allow_missing=allow_missing)
    if summary:
        _print_summary(summary)
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("discord_full_review_valid=true")


@discord_full_review_app.command("summary")
def discord_full_review_summary(
    results_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--results-dir", help="Generated Stage 4A output directory."),
) -> None:
    """Print a concise Stage 4A full-review summary."""

    try:
        summary = load_generated_summary(_resolve(results_dir))
    except Exception as error:  # noqa: BLE001 - CLI surfaces summary failures consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


def _print_summary(summary: dict) -> None:
    for key in [
        "run_id",
        "privacy_mode",
        "discord_html_file_count",
        "total_bytes_processed",
        "channel_count",
        "largest_channel_name",
        "largest_channel_part_count",
        "redacted_message_count",
        "channel_shard_count",
        "topic_shard_count",
        "public_link_count",
        "image_reference_count",
        "attachment_reference_count",
        "method_claim_count",
        "numeric_claim_count",
        "visual_claim_count",
        "debunk_count",
        "lp_page_image_count",
        "lp_page_thumbnail_count",
    ]:
        if key in summary:
            console.print(_console_safe(f"{key}={summary.get(key)}"))
    for key in [
        "raw_message_committed",
        "username_committed",
        "user_id_committed",
        "message_id_committed",
        "private_url_committed",
        "raw_discord_html_committed",
        "generated_site_committed",
        "solve_claim",
        "noindex_enabled",
        "robots_disallow_all",
    ]:
        if key in summary:
            console.print(f"{key}={str(summary.get(key)).lower()}")
    for key, value in summary.get("output_paths", {}).items():
        console.print(_console_safe(f"{key}={value}"))


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _console_safe(text: str) -> str:
    return text.encode("ascii", errors="replace").decode("ascii")


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(discord_full_review_app, name="discord-full-review")
