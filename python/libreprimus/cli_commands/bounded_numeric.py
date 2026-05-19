"""Stage 4D bounded numeric verifier CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.bounded_numeric.export import run_bounded_numeric_pack
from libreprimus.bounded_numeric.models import (
    DEFAULT_MANIFEST_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_STAGE4B_VISUAL,
    DEFAULT_STAGE4C_CUNEIFORM,
    DEFAULT_STAGE4C_DELIMITER,
    DEFAULT_STAGE4C_DOT,
    DEFAULT_STAGE4C_NEGATIVE,
    DEFAULT_STAGE4C_TASKS,
)
from libreprimus.bounded_numeric.summary import summarize_results
from libreprimus.bounded_numeric.validation import validate_bounded_numeric_results
from libreprimus.paths import repo_root

bounded_numeric_app = typer.Typer(no_args_is_help=True)
console = Console()


@bounded_numeric_app.command("run")
def bounded_numeric_run(
    manifest_dir: Path = typer.Option(DEFAULT_MANIFEST_DIR, "--manifest-dir", help="Stage 4B disabled manifest directory."),
    stage4b_visual: Path = typer.Option(DEFAULT_STAGE4B_VISUAL, "--stage4b-visual", help="Stage 4B visual observation records."),
    stage4c_tasks: Path = typer.Option(DEFAULT_STAGE4C_TASKS, "--stage4c-tasks", help="Stage 4C visual annotation task records."),
    stage4c_cuneiform: Path = typer.Option(DEFAULT_STAGE4C_CUNEIFORM, "--stage4c-cuneiform", help="Stage 4C cuneiform candidates."),
    stage4c_dot: Path = typer.Option(DEFAULT_STAGE4C_DOT, "--stage4c-dot", help="Stage 4C dot-pattern annotation tasks."),
    stage4c_delimiter: Path = typer.Option(DEFAULT_STAGE4C_DELIMITER, "--stage4c-delimiter", help="Stage 4C delimiter annotation tasks."),
    stage4c_negative: Path = typer.Option(DEFAULT_STAGE4C_NEGATIVE, "--stage4c-negative", help="Stage 4C visual negative-control tasks."),
    out_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated Stage 4D result directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow non-fatal no-fudge validation warnings."),
) -> None:
    """Run the Stage 4D bounded numeric verifier pack."""

    try:
        summary = run_bounded_numeric_pack(
            manifest_dir=_resolve(manifest_dir),
            stage4b_visual=_resolve(stage4b_visual),
            stage4c_tasks=_resolve(stage4c_tasks),
            stage4c_cuneiform=_resolve(stage4c_cuneiform),
            stage4c_dot=_resolve(stage4c_dot),
            stage4c_delimiter=_resolve(stage4c_delimiter),
            stage4c_negative=_resolve(stage4c_negative),
            out_dir=_resolve(out_dir),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI surfaces deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@bounded_numeric_app.command("validate")
def bounded_numeric_validate(
    results_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--results-dir", help="Generated Stage 4D result directory."),
) -> None:
    """Validate generated Stage 4D bounded numeric outputs."""

    summary, errors = validate_bounded_numeric_results(_resolve(results_dir))
    if summary:
        _print_summary(summary)
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("bounded_numeric_valid=true")


@bounded_numeric_app.command("summary")
def bounded_numeric_summary(
    results_dir: Path = typer.Option(DEFAULT_OUTPUT_DIR, "--results-dir", help="Generated Stage 4D result directory."),
) -> None:
    """Print a concise Stage 4D bounded numeric summary."""

    _print_summary(summarize_results(_resolve(results_dir)))


def _print_summary(summary: dict) -> None:
    keys = [
        "run_id",
        "manifests_discovered",
        "manifests_executed",
        "manifests_deferred",
        "gp_rune_claims_verified",
        "gp_rune_claims_skipped",
        "delimiter_observations_audited",
        "number_square_candidates_executed",
        "number_square_candidates_skipped",
        "visual_negative_controls_audited",
        "dot_ambiguity_audits",
        "cuneiform_deferred",
        "cookie_pack_deferred",
        "result_records_count",
        "negative_control_records_count",
        "no_fudge_policy",
        "solve_claim",
        "cuda_used",
    ]
    for key in keys:
        if key in summary:
            value = summary[key]
            console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    if "manifest_status_counts" in summary:
        for status, count in summary["manifest_status_counts"].items():
            console.print(f"manifest_status_{status}={count}")
    for key, value in summary.get("output_paths", {}).items():
        console.print(f"{key}={value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(bounded_numeric_app, name="bounded-numeric")
