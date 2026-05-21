"""Stage 5K Gematria CUDA parity-reporting CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_cuda_parity_reporting.device_code_audit import build_device_code_audit
from libreprimus.gematria_cuda_parity_reporting.models import (
    DEVICE_AUDIT_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    PREFLIGHT_PATH,
    SCORE_PREFLIGHT_PATH,
    SUMMARY_PATH,
)
from libreprimus.gematria_cuda_parity_reporting.parity_report import build_parity_report
from libreprimus.gematria_cuda_parity_reporting.score_summary_preflight import build_score_summary_preflight
from libreprimus.gematria_cuda_parity_reporting.solved_fixture_preflight import build_solved_fixture_preflight
from libreprimus.gematria_cuda_parity_reporting.summary import build_summary, load_summary
from libreprimus.gematria_cuda_parity_reporting.validation import validate_stage5k_results
from libreprimus.paths import repo_root

gematria_cuda_parity_reporting_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_cuda_parity_reporting_app.command("build-parity-report")
def build_parity_report_command(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5K parity-reporting manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5K output directory."),
    parity_report_out: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report-out", help="Committed parity-report YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5K Gematria CUDA parity-reporting records."""

    _require_file(manifest)
    records = build_parity_report(parity_report_out=_resolve(parity_report_out), out_dir=_resolve(out_dir))
    record = records[0]
    for key in (
        "implemented_kernel_name",
        "native_fixture_hash",
        "cuda_output_hash",
        "cuda_native_hash_match",
        "gematria_cuda_synthetic_parity_verified",
    ):
        console.print(f"{key}={record[key]}")
    if not allow_warnings:
        return


@gematria_cuda_parity_reporting_app.command("audit-device-code")
def audit_device_code_command(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5K device-code audit manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5K output directory."),
    device_code_audit_out: Path = typer.Option(DEVICE_AUDIT_PATH, "--device-code-audit-out", help="Committed audit YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow non-compliant audit records."),
) -> None:
    """Audit CUDA-facing .cu/.cuh files without executing CUDA."""

    _require_file(manifest)
    records = build_device_code_audit(device_code_audit_out=_resolve(device_code_audit_out), out_dir=_resolve(out_dir))
    record = records[0]
    for key in (
        "device_code_subset_compliant",
        "stl_used_in_cuda_device_path",
        "cxx_exceptions_in_cuda_device_path",
        "dynamic_allocation_in_device_code",
        "banned_token_finding_count",
    ):
        console.print(f"{key}={record[key]}")
    if not record["device_code_subset_compliant"] and not allow_warnings:
        raise typer.Exit(1)


@gematria_cuda_parity_reporting_app.command("build-solved-fixture-preflight")
def build_solved_fixture_preflight_command(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5K solved-fixture-safe preflight manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5K output directory."),
    preflight_out: Path = typer.Option(PREFLIGHT_PATH, "--preflight-out", help="Committed preflight YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build solved-fixture-safe preflight records without CUDA execution."""

    _require_file(manifest)
    records = build_solved_fixture_preflight(preflight_out=_resolve(preflight_out), out_dir=_resolve(out_dir))
    statuses: dict[str, int] = {}
    blocker_names: set[str] = set()
    for record in records:
        statuses[str(record["readiness_status"])] = statuses.get(str(record["readiness_status"]), 0) + 1
        blocker_names.update(str(blocker) for blocker in record.get("blockers", []))
    console.print(f"solved_fixture_safe_preflight_records={len(records)}")
    console.print(f"blocker_count={len(blocker_names)}")
    console.print(f"readiness_statuses={statuses}")
    if not allow_warnings:
        return


@gematria_cuda_parity_reporting_app.command("build-score-summary-preflight")
def build_score_summary_preflight_command(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5K score-summary preflight manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5K output directory."),
    score_summary_preflight_out: Path = typer.Option(
        SCORE_PREFLIGHT_PATH,
        "--score-summary-preflight-out",
        help="Committed score-summary preflight YAML.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build score-summary preflight records for future solved-fixture-safe CUDA output."""

    _require_file(manifest)
    records = build_score_summary_preflight(
        score_preflight_out=_resolve(score_summary_preflight_out),
        out_dir=_resolve(out_dir),
    )
    record = records[0]
    console.print(f"score_summary_preflight_records={len(records)}")
    console.print(f"score_summary_contract={record['score_summary_contract']}")
    console.print(f"score_interpretation={record['score_interpretation']}")
    if not allow_warnings:
        return


@gematria_cuda_parity_reporting_app.command("build-summary")
def build_summary_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report", help="Committed parity-report YAML."),
    device_code_audit: Path = typer.Option(DEVICE_AUDIT_PATH, "--device-code-audit", help="Committed audit YAML."),
    preflight: Path = typer.Option(PREFLIGHT_PATH, "--preflight", help="Committed preflight YAML."),
    score_summary_preflight: Path = typer.Option(
        SCORE_PREFLIGHT_PATH,
        "--score-summary-preflight",
        help="Committed score-summary preflight YAML.",
    ),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5K summary YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5K output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5K aggregate summary."""

    for path in (parity_report, device_code_audit, preflight, score_summary_preflight):
        _require_file(path)
    summary = build_summary(
        parity_report_path=_resolve(parity_report),
        device_code_audit_path=_resolve(device_code_audit),
        preflight_path=_resolve(preflight),
        score_preflight_path=_resolve(score_summary_preflight),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "implemented_kernel_name",
        "cuda_native_hash_match",
        "device_code_subset_compliant",
        "blocker_count",
        "selected_next_stage",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@gematria_cuda_parity_reporting_app.command("validate-stage5k")
def validate_stage5k_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report", help="Committed parity-report YAML."),
    device_code_audit: Path = typer.Option(DEVICE_AUDIT_PATH, "--device-code-audit", help="Committed audit YAML."),
    preflight: Path = typer.Option(PREFLIGHT_PATH, "--preflight", help="Committed preflight YAML."),
    score_summary_preflight: Path = typer.Option(
        SCORE_PREFLIGHT_PATH,
        "--score-summary-preflight",
        help="Committed score-summary preflight YAML.",
    ),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5K summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5K output directory."),
) -> None:
    """Validate Stage 5K Gematria CUDA parity-reporting records."""

    try:
        counts, errors = validate_stage5k_results(
            parity_report_path=_resolve(parity_report),
            device_code_audit_path=_resolve(device_code_audit),
            preflight_path=_resolve(preflight),
            score_preflight_path=_resolve(score_summary_preflight),
            summary_path=_resolve(summary),
            results_dir=_resolve(results_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("gematria_cuda_parity_reporting_stage5k_valid=true")


@gematria_cuda_parity_reporting_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5K summary YAML.")) -> None:
    """Print the committed Stage 5K summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "implemented_kernel_name",
        "native_fixture_hash",
        "cuda_output_hash",
        "cuda_native_hash_match",
        "gematria_cuda_synthetic_parity_verified",
        "device_code_subset_compliant",
        "solved_fixture_safe_preflight_records",
        "blocker_count",
        "readiness_status_counts",
        "score_summary_preflight_records",
        "solved_fixture_cuda_execution_allowed",
        "production_gematria_mod29_cuda_ready",
        "gpu_benchmark_performed",
        "performance_claim",
        "speedup_claim",
        "real_liber_primus_data_used",
        "selected_next_stage",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_cuda_parity_reporting_app, name="gematria-cuda-parity-reporting")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
