"""Stage 5D native CPU backend CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.native_cpu.models import (
    CAPABILITIES_PATH,
    DIAGNOSTICS_PATH,
    OUTPUT_DIR,
    PARITY_PATH,
    SUMMARY_PATH,
    THREADING_PATH,
    THREAD_COUNTS,
)
from libreprimus.native_cpu.summary import (
    build_capability_and_diagnostic_records,
    build_parity_records,
    build_summary,
    build_threading_records,
    load_summary,
)
from libreprimus.native_cpu.validation import validate_stage5d_results
from libreprimus.paths import repo_root

native_cpu_app = typer.Typer(no_args_is_help=True)
console = Console()


@native_cpu_app.command("run-smoke")
def native_cpu_run_smoke(
    native_executable: Path = typer.Option(..., "--native-executable", help="Native CPU backend executable."),
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5D native CPU smoke manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5D output directory."),
    capabilities_out: Path = typer.Option(CAPABILITIES_PATH, "--capabilities-out", help="Committed capability records."),
    diagnostics_out: Path = typer.Option(DIAGNOSTICS_PATH, "--diagnostics-out", help="Committed diagnostic records."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warnings."),
) -> None:
    """Run the tiny native CPU smoke fixture and write capability records."""

    _require_file(manifest)
    _require_file(native_executable)
    capabilities, diagnostics = build_capability_and_diagnostic_records(
        native_executable=_resolve(native_executable),
        out_dir=_resolve(out_dir),
        capabilities_out=_resolve(capabilities_out),
        diagnostics_out=_resolve(diagnostics_out),
    )
    console.print(f"native_backend_built={_bool(capabilities[0]['native_backend_built'])}")
    console.print(f"native_backend_executable={capabilities[0]['native_backend_executable']}")
    console.print(f"backend_capability_records={len(capabilities)}")
    console.print(f"diagnostic_records={len(diagnostics)}")
    console.print("cuda_used=false")
    console.print("gpu_benchmark_performed=false")
    if not capabilities[0]["native_backend_built"] and not allow_warnings:
        raise typer.Exit(1)


@native_cpu_app.command("check-threading-parity")
def native_cpu_check_threading_parity(
    native_executable: Path = typer.Option(..., "--native-executable", help="Native CPU backend executable."),
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5D threading parity manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5D output directory."),
    threading_out: Path = typer.Option(THREADING_PATH, "--threading-out", help="Committed threading records."),
    thread_counts: str = typer.Option("1,2,4,8,16", "--thread-counts", help="Comma-separated thread counts."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warnings."),
) -> None:
    """Check deterministic native output hashes across thread counts."""

    _require_file(manifest)
    _require_file(native_executable)
    counts = _parse_thread_counts(thread_counts)
    records = build_threading_records(
        native_executable=_resolve(native_executable),
        thread_counts=counts,
        out_dir=_resolve(out_dir),
        threading_out=_resolve(threading_out),
    )
    one = next(record for record in records if int(record["thread_count"]) == 1)
    multi = next((record for record in records if int(record["thread_count"]) > 1), one)
    all_match = all(record["matches_baseline"] is True for record in records)
    console.print(f"threading_records={len(records)}")
    console.print(f"thread_counts_tested={','.join(str(record['thread_count']) for record in records)}")
    console.print(f"one_thread_hash={one['output_hash']}")
    console.print(f"multi_thread_hash={multi['output_hash']}")
    console.print(f"one_thread_equals_multi_thread={_bool(all_match)}")
    if not all_match and not allow_warnings:
        raise typer.Exit(1)


@native_cpu_app.command("check-python-parity")
def native_cpu_check_python_parity(
    native_executable: Path = typer.Option(..., "--native-executable", help="Native CPU backend executable."),
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5D native/Python parity manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5D output directory."),
    parity_out: Path = typer.Option(PARITY_PATH, "--parity-out", help="Committed parity records."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warnings."),
) -> None:
    """Compare the native tiny fixture with the Python semantic reference."""

    _require_file(manifest)
    _require_file(native_executable)
    records = build_parity_records(
        native_executable=_resolve(native_executable),
        out_dir=_resolve(out_dir),
        parity_out=_resolve(parity_out),
    )
    passed = all(record["parity_passed"] is True for record in records)
    console.print(f"parity_records={len(records)}")
    console.print(f"python_native_parity={_bool(passed)}")
    console.print(f"native_output_hash={records[0]['native_output_hash']}")
    console.print(f"python_reference_hash={records[0]['python_reference_hash']}")
    if not passed and not allow_warnings:
        raise typer.Exit(1)


@native_cpu_app.command("build-summary")
def native_cpu_build_summary(
    capabilities: Path = typer.Option(CAPABILITIES_PATH, "--capabilities", help="Committed capability records."),
    threading: Path = typer.Option(THREADING_PATH, "--threading", help="Committed threading records."),
    parity: Path = typer.Option(PARITY_PATH, "--parity", help="Committed parity records."),
    diagnostics: Path = typer.Option(DIAGNOSTICS_PATH, "--diagnostics", help="Committed diagnostic records."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed summary record."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5D output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warnings."),
) -> None:
    """Build the Stage 5D aggregate summary."""

    for path in (capabilities, threading, parity, diagnostics):
        _require_file(path)
    summary = build_summary(
        capabilities_path=_resolve(capabilities),
        threading_path=_resolve(threading),
        parity_path=_resolve(parity),
        diagnostics_path=_resolve(diagnostics),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    _print_summary(summary)
    if not summary["one_thread_equals_multi_thread"] and not allow_warnings:
        raise typer.Exit(1)


@native_cpu_app.command("validate-stage5d")
def native_cpu_validate_stage5d(
    capabilities: Path = typer.Option(CAPABILITIES_PATH, "--capabilities", help="Committed capability records."),
    threading: Path = typer.Option(THREADING_PATH, "--threading", help="Committed threading records."),
    parity: Path = typer.Option(PARITY_PATH, "--parity", help="Committed parity records."),
    diagnostics: Path = typer.Option(DIAGNOSTICS_PATH, "--diagnostics", help="Committed diagnostic records."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5D summary."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5D output directory."),
) -> None:
    """Validate Stage 5D native CPU records and generated summary."""

    try:
        counts, errors = validate_stage5d_results(
            capabilities_path=_resolve(capabilities),
            threading_path=_resolve(threading),
            parity_path=_resolve(parity),
            diagnostics_path=_resolve(diagnostics),
            summary_path=_resolve(summary),
            results_dir=_resolve(results_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={_format(value)}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("native_cpu_stage5d_valid=true")


@native_cpu_app.command("summary")
def native_cpu_summary(
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5D summary."),
) -> None:
    """Print the committed Stage 5D summary."""

    _print_summary(load_summary(_resolve(summary)))


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]required file missing: {path}[/red]")
        raise typer.Exit(1)


def _parse_thread_counts(value: str) -> list[int]:
    counts = [int(part.strip()) for part in value.split(",") if part.strip()]
    return counts or list(THREAD_COUNTS)


def _print_summary(summary: dict[str, object]) -> None:
    for key in (
        "backend_capability_records",
        "threading_records",
        "parity_records",
        "diagnostic_records",
        "thread_counts_tested",
        "one_thread_hash",
        "multi_thread_hash",
        "one_thread_equals_multi_thread",
        "python_native_parity",
        "native_backend_built",
        "native_backend_executable",
        "cuda_used",
        "gpu_benchmark_performed",
        "timing_is_diagnostic_only",
    ):
        console.print(f"{key}={_format(summary[key])}")


def _format(value: object) -> str:
    if isinstance(value, bool):
        return _bool(value)
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    return str(value)


def _bool(value: object) -> str:
    return str(bool(value)).lower()


def register(root_app: typer.Typer) -> None:
    """Register the Stage 5D native CPU command group."""

    root_app.add_typer(native_cpu_app, name="native-cpu")
