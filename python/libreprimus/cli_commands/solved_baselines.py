"""Solved baseline CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *
from libreprimus.cli_commands.transforms import transform_registry_validate

solved_baseline_app = typer.Typer(no_args_is_help=True)


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




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(solved_baseline_app, name="solved-baseline")
