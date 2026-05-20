"""Stage 5F synthetic CUDA kernel CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_kernel.build_records import build_records
from libreprimus.cuda_kernel.implementation_records import build_implementation_records
from libreprimus.cuda_kernel.models import (
    BUILD_DIR,
    BUILD_RECORDS_PATH,
    IMPLEMENTATION_PATH,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    SUMMARY_PATH,
)
from libreprimus.cuda_kernel.run_records import build_parity_records
from libreprimus.cuda_kernel.summary import build_summary, load_summary
from libreprimus.cuda_kernel.validation import validate_stage5f_results
from libreprimus.paths import repo_root

cuda_kernel_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_kernel_app.command("build-implementation-records")
def cuda_kernel_build_implementation_records(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5F implementation manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5F output directory."),
    implementation_out: Path = typer.Option(IMPLEMENTATION_PATH, "--implementation-out", help="Committed implementation YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5F synthetic kernel implementation metadata."""

    _require_file(manifest)
    records = build_implementation_records(implementation_out=_resolve(implementation_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"selected_kernel_id={record['selected_kernel_id']}")
    console.print(f"selected_target_id={record['selected_target_id']}")
    console.print(f"selected_adapter_family={record['selected_adapter_family']}")
    console.print(f"cuda_kernel_added={str(record['cuda_kernel_added']).lower()}")
    console.print(f"cuda_source_modified={str(record['cuda_source_modified']).lower()}")
    if not allow_warnings:
        return


@cuda_kernel_app.command("attempt-build")
def cuda_kernel_attempt_build(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5F no-GPU/local optional build manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5F output directory."),
    build_records_out: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records-out", help="Committed CUDA build records YAML."),
    build_dir: Path = typer.Option(BUILD_DIR, "--build-dir", help="Ignored local CUDA build directory."),
    skip_build: bool = typer.Option(False, "--skip-build", help="Record a no-GPU-safe skipped build instead of attempting local CUDA."),
    require_cuda: bool = typer.Option(False, "--require-cuda", help="Fail if CUDA build does not pass."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow failed/skipped CUDA build records."),
) -> None:
    """Attempt an optional local CUDA build, or record an explicit no-GPU-safe skip."""

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
    console.print(f"cuda_build_attempted={str(record['cuda_build_attempted']).lower()}")
    console.print(f"cuda_build_status={record['build_status']}")
    console.print(f"cmake_detected={str(record['cmake_detected']).lower()}")
    console.print(f"nvcc_detected={str(record['nvcc_detected']).lower()}")
    if record["build_status"] == "failed" and not allow_warnings:
        raise typer.Exit(1)


@cuda_kernel_app.command("run-synthetic-parity")
def cuda_kernel_run_synthetic_parity(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5F synthetic parity manifest."),
    build_records: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records", help="Committed CUDA build records YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5F output directory."),
    parity_records_out: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records-out", help="Committed CUDA parity records YAML."),
    build_dir: Path = typer.Option(BUILD_DIR, "--build-dir", help="Ignored local CUDA build directory."),
    require_cuda: bool = typer.Option(False, "--require-cuda", help="Fail if synthetic parity does not pass."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow skipped/failed CUDA parity records."),
) -> None:
    """Run synthetic CUDA parity when the optional local CUDA build passed."""

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
    console.print(f"cuda_synthetic_parity_attempted={str(record['cuda_synthetic_parity_attempted']).lower()}")
    console.print(f"cuda_synthetic_parity_status={record['parity_status']}")
    console.print(f"cuda_output_hash={record['cuda_output_hash']}")
    console.print(f"cuda_native_hash_match={record['cuda_native_hash_match']}")
    if record["parity_status"] == "failed" and not allow_warnings:
        raise typer.Exit(1)


@cuda_kernel_app.command("build-summary")
def cuda_kernel_build_summary(
    implementation: Path = typer.Option(IMPLEMENTATION_PATH, "--implementation", help="Committed implementation YAML."),
    build_records: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records", help="Committed CUDA build records YAML."),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records", help="Committed CUDA parity records YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5F summary YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5F output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5F aggregate summary."""

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
        "selected_kernel_id",
        "selected_target_id",
        "selected_adapter_family",
        "native_reference_hash",
        "cuda_build_status",
        "cuda_synthetic_parity_status",
        "cuda_native_hash_match",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@cuda_kernel_app.command("validate-stage5f")
def cuda_kernel_validate_stage5f(
    implementation: Path = typer.Option(IMPLEMENTATION_PATH, "--implementation", help="Committed implementation YAML."),
    build_records: Path = typer.Option(BUILD_RECORDS_PATH, "--build-records", help="Committed CUDA build records YAML."),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records", help="Committed CUDA parity records YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5F summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5F output directory."),
) -> None:
    """Validate Stage 5F synthetic CUDA kernel records."""

    try:
        counts, errors = validate_stage5f_results(
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
    console.print("cuda_kernel_stage5f_valid=true")


@cuda_kernel_app.command("summary")
def cuda_kernel_summary(
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5F summary YAML."),
) -> None:
    """Print the committed Stage 5F summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "selected_kernel_id",
        "selected_target_id",
        "selected_adapter_family",
        "native_reference_hash",
        "cuda_kernel_added",
        "cuda_source_modified",
        "cuda_build_attempted",
        "cuda_build_status",
        "cuda_synthetic_parity_attempted",
        "cuda_synthetic_parity_status",
        "cuda_output_hash",
        "cuda_native_hash_match",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(cuda_kernel_app, name="cuda-kernel")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
