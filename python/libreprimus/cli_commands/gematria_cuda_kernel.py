"""Stage 5J Gematria CUDA kernel CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_cuda_kernel.build_records import build_records
from libreprimus.gematria_cuda_kernel.implementation_records import build_implementation_records
from libreprimus.gematria_cuda_kernel.models import (
    BUILD_DIR,
    BUILD_RECORDS_PATH,
    IMPLEMENTATION_PATH,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    SUMMARY_PATH,
)
from libreprimus.gematria_cuda_kernel.summary import build_summary, load_summary
from libreprimus.gematria_cuda_kernel.synthetic_parity import build_parity_records
from libreprimus.gematria_cuda_kernel.validation import validate_stage5j_results
from libreprimus.paths import repo_root

gematria_cuda_kernel_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_cuda_kernel_app.command("build-implementation-records")
def build_implementation_command(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5J implementation manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5J output directory."),
    implementation_out: Path = typer.Option(IMPLEMENTATION_PATH, "--implementation-out", help="Committed implementation YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5J kernel implementation metadata."""

    _require_file(manifest)
    records = build_implementation_records(implementation_out=_resolve(implementation_out), out_dir=_resolve(out_dir))
    record = records[0]
    for key in (
        "implemented_kernel_name",
        "source_contract_id",
        "native_fixture_hash",
        "cuda_kernel_added",
        "new_cuda_kernels_added",
        "cuda_source_modified",
    ):
        console.print(f"{key}={record[key]}")
    if not allow_warnings:
        return


@gematria_cuda_kernel_app.command("attempt-build")
def attempt_build_command(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5J local optional/no-GPU build manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5J output directory."),
    build_records_out: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records-out", help="Committed CUDA build records YAML."),
    build_dir: Path = typer.Option(BUILD_DIR, "--build-dir", help="Ignored local CUDA build directory."),
    skip_build: bool = typer.Option(False, "--skip-build", help="Record a no-GPU-safe skipped build."),
    require_cuda: bool = typer.Option(False, "--require-cuda", help="Fail unless CUDA build passes."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow skipped/failed CUDA build records."),
) -> None:
    """Attempt the optional local Stage 5J CUDA build."""

    _require_file(manifest)
    try:
        records = build_records(
            build_records_out=_resolve(build_records_out),
            out_dir=_resolve(out_dir),
            build_dir=_resolve(build_dir),
            require_cuda=require_cuda,
            run_build=not skip_build,
        )
    except RuntimeError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    record = records[0]
    for key in ("cuda_build_attempted", "build_status", "cmake_detected", "nvcc_detected", "nvcc_path", "toolkit_root"):
        console.print(f"{key}={record.get(key)}")
    if record["build_status"] not in {"passed", "skipped_not_requested", "skipped_missing_cuda"} and not allow_warnings:
        raise typer.Exit(1)


@gematria_cuda_kernel_app.command("run-synthetic-parity")
def run_synthetic_parity_command(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5J synthetic parity manifest."),
    build_records: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records", help="Committed CUDA build records YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5J output directory."),
    parity_records_out: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records-out", help="Committed parity records YAML."),
    build_dir: Path = typer.Option(BUILD_DIR, "--build-dir", help="Ignored local CUDA build directory."),
    require_cuda: bool = typer.Option(False, "--require-cuda", help="Fail unless synthetic parity passes."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow skipped/failed CUDA parity records."),
) -> None:
    """Run synthetic Gematria CUDA parity when the optional build passed."""

    _require_file(manifest)
    _require_file(build_records)
    try:
        records = build_parity_records(
            build_records_path=_resolve(build_records),
            parity_records_out=_resolve(parity_records_out),
            out_dir=_resolve(out_dir),
            build_dir=_resolve(build_dir),
            require_cuda=require_cuda,
        )
    except RuntimeError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    record = records[0]
    for key in (
        "cuda_synthetic_parity_attempted",
        "parity_status",
        "cuda_output_hash",
        "cuda_native_hash_match",
        "gematria_cuda_synthetic_parity_verified",
        "stage5k_ready",
    ):
        console.print(f"{key}={record.get(key)}")
    if record["parity_status"] == "failed" and not allow_warnings:
        raise typer.Exit(1)


@gematria_cuda_kernel_app.command("build-summary")
def build_summary_command(
    implementation: Path = typer.Option(IMPLEMENTATION_PATH, "--implementation", help="Committed implementation YAML."),
    build_records: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records", help="Committed build records YAML."),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records", help="Committed parity records YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5J summary YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5J output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5J aggregate summary."""

    for path in (implementation, build_records, parity_records):
        _require_file(path)
    summary = build_summary(
        implementation_path=_resolve(implementation),
        build_records_path=_resolve(build_records),
        parity_records_path=_resolve(parity_records),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "implemented_kernel_name",
        "source_contract_id",
        "native_fixture_hash",
        "cuda_build_status",
        "cuda_synthetic_parity_status",
        "gematria_cuda_synthetic_parity_verified",
        "stage5k_ready",
        "recommended_next_prompt",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@gematria_cuda_kernel_app.command("validate-stage5j")
def validate_stage5j_command(
    implementation: Path = typer.Option(IMPLEMENTATION_PATH, "--implementation", help="Committed implementation YAML."),
    build_records: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records", help="Committed build records YAML."),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records", help="Committed parity records YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5J summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5J output directory."),
) -> None:
    """Validate Stage 5J Gematria CUDA records."""

    try:
        counts, errors = validate_stage5j_results(
            implementation_path=_resolve(implementation),
            build_records_path=_resolve(build_records),
            parity_records_path=_resolve(parity_records),
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
    console.print("gematria_cuda_kernel_stage5j_valid=true")


@gematria_cuda_kernel_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5J summary YAML.")) -> None:
    """Print the committed Stage 5J summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "implemented_kernel_name",
        "source_contract_id",
        "native_fixture_hash",
        "cuda_build_attempted",
        "cuda_build_status",
        "cuda_synthetic_parity_attempted",
        "cuda_synthetic_parity_status",
        "cuda_output_hash",
        "cuda_native_hash_match",
        "gematria_cuda_synthetic_parity_verified",
        "stage5k_ready",
        "recommended_next_prompt",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_cuda_kernel_app, name="gematria-cuda-kernel")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
