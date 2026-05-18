"""Stego and OutGuess CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

stego_app = typer.Typer(no_args_is_help=True)


@stego_app.command("outguess-detect")
def stego_outguess_detect(
    outguess_path: Path | None = typer.Option(None, "--outguess-path", help="Explicit OutGuess executable path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE3V_OUTPUT_DIR,
        "--out-dir",
        help="Generated Stage 3V output directory.",
    ),
    allow_missing_tool: bool = typer.Option(
        False,
        "--allow-missing-tool",
        help="Return success when OutGuess is unavailable.",
    ),
) -> None:
    """Detect OutGuess and write a generated tool record."""
    explicit = outguess_path if outguess_path else None
    tool = detect_outguess(explicit)
    record = tool_record(tool)
    write_stego_json(_resolve_output_path(out_dir) / "outguess_tool_record.json", record)
    console.print(f"tool_available={str(tool.available).lower()}")
    console.print(f"tool_path={tool.path}")
    console.print(f"help_output_sha256={tool.help_output_sha256}")
    if not tool.available and not allow_missing_tool:
        raise typer.Exit(1)


@stego_app.command("outguess-validate-manifest")
def stego_outguess_validate_manifest(
    manifest: Path = typer.Option(DEFAULT_STAGE3V_MANIFEST, "--manifest", help="OutGuess regression manifest."),
    artifacts: Path = typer.Option(DEFAULT_STAGE3V_ARTIFACTS, "--artifacts", help="OutGuess artifact records."),
) -> None:
    """Validate the Stage 3V OutGuess manifest and artifact records."""
    payload, errors = validate_outguess_manifest(
        _resolve_existing_path(manifest, "OutGuess manifest"),
        _resolve_existing_path(artifacts, "OutGuess artifact records"),
    )
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("outguess_manifest_valid=true")
    for key in [
        "manifest_id",
        "case_count",
        "enabled_case_count",
        "artifact_count",
        "historical_positive_placeholder_count",
        "synthetic_control_count",
        "allow_missing_tool",
        "allow_missing_assets",
        "cuda_enabled",
        "no_solve_claim",
    ]:
        value = payload.get(key)
        if isinstance(value, bool):
            value = str(value).lower()
        console.print(f"{key}={value}")


@stego_app.command("outguess-run")
def stego_outguess_run(
    manifest: Path = typer.Option(DEFAULT_STAGE3V_MANIFEST, "--manifest", help="OutGuess regression manifest."),
    artifacts: Path = typer.Option(DEFAULT_STAGE3V_ARTIFACTS, "--artifacts", help="OutGuess artifact records."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE3V_OUTPUT_DIR,
        "--out-dir",
        help="Generated Stage 3V output directory.",
    ),
    outguess_path: Path | None = typer.Option(None, "--outguess-path", help="Explicit OutGuess executable path."),
    allow_missing_tool: bool = typer.Option(False, "--allow-missing-tool", help="Skip cases when tool is missing."),
    allow_missing_assets: bool = typer.Option(False, "--allow-missing-assets", help="Skip cases when assets are missing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run explicit Stage 3V OutGuess regression cases."""
    explicit = outguess_path if outguess_path else None
    try:
        summary = run_outguess_regression(
            manifest_path=_resolve_existing_path(manifest, "OutGuess manifest"),
            artifacts_path=_resolve_existing_path(artifacts, "OutGuess artifact records"),
            out_dir=_resolve_output_path(out_dir),
            outguess_path=explicit,
            allow_missing_tool=allow_missing_tool,
            allow_missing_assets=allow_missing_assets,
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3v_payload(summary)


@stego_app.command("outguess-summary")
def stego_outguess_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE3V_OUTPUT_DIR,
        "--results-dir",
        help="Generated Stage 3V result directory.",
    ),
) -> None:
    """Print a concise Stage 3V OutGuess regression summary."""
    try:
        payload = load_outguess_summary(_resolve_output_path(results_dir))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3v_payload(payload)


def _print_stage3v_payload(summary: dict) -> None:
    for key in [
        "run_id",
        "manifest_path",
        "tool_available",
        "tool_path",
        "case_count",
        "attempted_count",
        "passed_count",
        "failed_count",
        "skipped_tool_missing_count",
        "skipped_asset_missing_count",
        "skipped_case_disabled_count",
        "extraction_error_count",
        "unexpected_payload_count",
        "no_payload_count",
        "reference_extraction_recorded_count",
    ]:
        value = summary.get(key)
        if isinstance(value, bool):
            value = str(value).lower()
        console.print(f"{key}={value}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    console.print(f"cuda_used={str(summary.get('cuda_used')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")



def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(stego_app, name="stego")
