"""Stage 5G CUDA parity-reporting CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_parity_reporting.device_code_audit import build_device_code_subset_audit
from libreprimus.cuda_parity_reporting.models import DEVICE_AUDIT_PATH, OUTPUT_DIR, PARITY_REPORT_PATH, PREFLIGHT_PATH, SUMMARY_PATH
from libreprimus.cuda_parity_reporting.parity_report import build_parity_report
from libreprimus.cuda_parity_reporting.solved_fixture_preflight import build_solved_fixture_preflight
from libreprimus.cuda_parity_reporting.summary import build_summary, load_summary
from libreprimus.cuda_parity_reporting.validation import validate_stage5g_results
from libreprimus.paths import repo_root

cuda_parity_reporting_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_parity_reporting_app.command("build-parity-report")
def cuda_parity_reporting_build_parity_report(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5G parity-reporting manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5G output directory."),
    parity_report_out: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report-out", help="Committed parity-report YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5G shift_score parity-reporting records."""

    _require_file(manifest)
    records = build_parity_report(parity_report_out=_resolve(parity_report_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"selected_kernel_id={record['selected_kernel_id']}")
    console.print(f"stage5f_cuda_output_hash={record['stage5f_cuda_output_hash']}")
    console.print(f"stage5f_cuda_native_hash_match={str(record['stage5f_cuda_native_hash_match']).lower()}")
    if not allow_warnings:
        return


@cuda_parity_reporting_app.command("audit-device-code-subset")
def cuda_parity_reporting_audit_device_code_subset(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5G device-code audit manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5G output directory."),
    device_code_audit_out: Path = typer.Option(DEVICE_AUDIT_PATH, "--device-code-audit-out", help="Committed device-code audit YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow non-compliant audit records."),
) -> None:
    """Audit CUDA-facing .cu/.cuh files for conservative CUDA-C subset compliance."""

    _require_file(manifest)
    records = build_device_code_subset_audit(device_code_audit_out=_resolve(device_code_audit_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"device_code_subset_compliant={str(record['device_code_subset_compliant']).lower()}")
    console.print(f"stl_used_in_cuda_device_path={str(record['stl_used_in_cuda_device_path']).lower()}")
    console.print(f"std_array_used_in_cuda_device_path={str(record['std_array_used_in_cuda_device_path']).lower()}")
    console.print(f"cxx_exceptions_in_cuda_device_path={str(record['cxx_exceptions_in_cuda_device_path']).lower()}")
    if not record["device_code_subset_compliant"] and not allow_warnings:
        raise typer.Exit(1)


@cuda_parity_reporting_app.command("build-solved-fixture-preflight")
def cuda_parity_reporting_build_solved_fixture_preflight(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5G solved-fixture-safe preflight manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5G output directory."),
    preflight_out: Path = typer.Option(PREFLIGHT_PATH, "--preflight-out", help="Committed preflight YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build solved-fixture-safe adapter preflight records."""

    _require_file(manifest)
    records = build_solved_fixture_preflight(preflight_out=_resolve(preflight_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"solved_fixture_cuda_execution_allowed={str(record['solved_fixture_cuda_execution_allowed']).lower()}")
    console.print(f"production_gematria_mod29_cuda_ready={str(record['production_gematria_mod29_cuda_ready']).lower()}")
    console.print(f"preflight_blocker_count={record['preflight_blocker_count']}")
    if not allow_warnings:
        return


@cuda_parity_reporting_app.command("build-summary")
def cuda_parity_reporting_build_summary(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report", help="Committed parity-report YAML."),
    device_code_audit: Path = typer.Option(DEVICE_AUDIT_PATH, "--device-code-audit", help="Committed device-code audit YAML."),
    preflight: Path = typer.Option(PREFLIGHT_PATH, "--preflight", help="Committed preflight YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5G summary YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5G output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5G aggregate summary."""

    for path in (parity_report, device_code_audit, preflight):
        _require_file(path)
    summary = build_summary(
        parity_report_path=_resolve(parity_report),
        device_code_audit_path=_resolve(device_code_audit),
        preflight_path=_resolve(preflight),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "selected_kernel_id",
        "native_reference_hash",
        "stage5f_cuda_output_hash",
        "stage5f_cuda_native_hash_match",
        "device_code_subset_compliant",
        "preflight_blocker_count",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@cuda_parity_reporting_app.command("validate-stage5g")
def cuda_parity_reporting_validate_stage5g(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report", help="Committed parity-report YAML."),
    device_code_audit: Path = typer.Option(DEVICE_AUDIT_PATH, "--device-code-audit", help="Committed device-code audit YAML."),
    preflight: Path = typer.Option(PREFLIGHT_PATH, "--preflight", help="Committed preflight YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5G summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5G output directory."),
) -> None:
    """Validate Stage 5G CUDA parity-reporting records."""

    try:
        counts, errors = validate_stage5g_results(
            parity_report_path=_resolve(parity_report),
            device_code_audit_path=_resolve(device_code_audit),
            preflight_path=_resolve(preflight),
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
    console.print("cuda_parity_reporting_stage5g_valid=true")


@cuda_parity_reporting_app.command("summary")
def cuda_parity_reporting_summary(
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5G summary YAML."),
) -> None:
    """Print the committed Stage 5G summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "selected_kernel_id",
        "native_reference_hash",
        "stage5f_cuda_output_hash",
        "stage5f_cuda_native_hash_match",
        "device_code_subset_compliant",
        "stl_used_in_cuda_device_path",
        "std_array_used_in_cuda_device_path",
        "cxx_exceptions_in_cuda_device_path",
        "solved_fixture_cuda_execution_allowed",
        "production_gematria_mod29_cuda_ready",
        "next_stage",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(cuda_parity_reporting_app, name="cuda-parity-reporting")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
