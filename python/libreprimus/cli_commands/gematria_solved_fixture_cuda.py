"""Stage 5M solved-fixture-safe Gematria CUDA parity CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_solved_fixture_cuda.boundaries import build_boundary_records
from libreprimus.gematria_solved_fixture_cuda.cuda_parity import run_cuda_parity
from libreprimus.gematria_solved_fixture_cuda.models import (
    BOUNDARY_RECORDS_PATH,
    BUILD_DIR,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    RUN_RECORDS_PATH,
    SUMMARY_PATH,
    TOKEN_MAPPING_PATH,
)
from libreprimus.gematria_solved_fixture_cuda.parity_records import build_parity_records
from libreprimus.gematria_solved_fixture_cuda.run_records import build_run_records
from libreprimus.gematria_solved_fixture_cuda.summary import build_summary, load_summary
from libreprimus.gematria_solved_fixture_cuda.validation import validate_stage5m_results
from libreprimus.paths import repo_root

gematria_solved_fixture_cuda_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_solved_fixture_cuda_app.command("build-run-records")
def build_run_records_command(
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping", help="Stage 5L token mappings."),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity", help="Stage 5L native parity records."),
    run_records_out: Path = typer.Option(RUN_RECORDS_PATH, "--run-records-out", help="Committed Stage 5M run records."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5M output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build pending Stage 5M CUDA run records from Stage 5L mappings."""

    _require_file(token_mapping)
    _require_file(native_parity)
    records = build_run_records(
        token_mapping=_resolve(token_mapping),
        native_parity=_resolve(native_parity),
        run_records_out=_resolve(run_records_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"run_records={len(records)}")
    console.print(f"input_mapping_records={len(records)}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_app.command("run-cuda-parity")
def run_cuda_parity_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records", help="Stage 5M run records to update."),
    run_records_out: Path = typer.Option(RUN_RECORDS_PATH, "--run-records-out", help="Updated Stage 5M run records."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5M output directory."),
    build_dir: Path = typer.Option(BUILD_DIR, "--build-dir", help="Ignored local CUDA build directory."),
    skip_run: bool = typer.Option(False, "--skip-run", help="Record an explicit no-GPU-safe skipped run."),
    require_cuda: bool = typer.Option(False, "--require-cuda", help="Fail unless all Stage 5M CUDA parity records pass."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow skipped/failed local CUDA execution records."),
) -> None:
    """Attempt the bounded Stage 5M CUDA run, or record a no-GPU-safe skip."""

    _require_file(run_records)
    try:
        records = run_cuda_parity(
            run_records_path=_resolve(run_records),
            run_records_out=_resolve(run_records_out),
            out_dir=_resolve(out_dir),
            build_dir=_resolve(build_dir),
            skip_run=skip_run,
            require_cuda=require_cuda,
        )
    except RuntimeError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    attempted = sum(1 for record in records if record["cuda_run_attempted"])
    passed = sum(1 for record in records if record["cuda_run_status"] == "passed")
    failed = sum(1 for record in records if record["cuda_run_status"] == "failed")
    skipped = len(records) - passed - failed
    console.print(f"cuda_attempted_count={attempted}")
    console.print(f"cuda_pass_count={passed}")
    console.print(f"cuda_fail_count={failed}")
    console.print(f"cuda_skip_count={skipped}")
    if failed and not allow_warnings:
        raise typer.Exit(1)


@gematria_solved_fixture_cuda_app.command("build-parity-records")
def build_parity_records_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records", help="Stage 5M run records."),
    parity_records_out: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records-out", help="Committed parity records."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5M output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5M CUDA/native parity records."""

    _require_file(run_records)
    records = build_parity_records(
        run_records=_resolve(run_records),
        parity_records_out=_resolve(parity_records_out),
        out_dir=_resolve(out_dir),
    )
    passed = sum(1 for record in records if record["parity_status"] == "passed")
    failed = sum(1 for record in records if str(record["parity_status"]).startswith("failed"))
    console.print(f"parity_records={len(records)}")
    console.print(f"parity_pass_count={passed}")
    console.print(f"parity_fail_count={failed}")
    console.print(f"parity_skip_count={len(records) - passed - failed}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_app.command("build-boundary-records")
def build_boundary_records_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records", help="Stage 5M run records."),
    boundaries_out: Path = typer.Option(BOUNDARY_RECORDS_PATH, "--boundaries-out", help="Committed boundary records."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5M output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5M safety boundary records."""

    _require_file(run_records)
    records = build_boundary_records(
        run_records=_resolve(run_records),
        boundaries_out=_resolve(boundaries_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"boundary_records={len(records)}")
    console.print(f"cuda_attempted_count={records[0]['cuda_attempted_count']}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_app.command("build-summary")
def build_summary_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records", help="Stage 5M run records."),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records", help="Stage 5M parity records."),
    boundaries: Path = typer.Option(BOUNDARY_RECORDS_PATH, "--boundaries", help="Stage 5M boundary records."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5M summary."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5M output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5M summary."""

    for path in (run_records, parity_records, boundaries):
        _require_file(path)
    summary = build_summary(
        run_records=_resolve(run_records),
        parity_records=_resolve(parity_records),
        boundaries=_resolve(boundaries),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "run_records",
        "cuda_attempted_count",
        "cuda_pass_count",
        "cuda_fail_count",
        "cuda_skip_count",
        "stage5n_ready",
        "selected_next_stage",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_app.command("validate-stage5m")
def validate_stage5m_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records", help="Stage 5M run records."),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records", help="Stage 5M parity records."),
    boundaries: Path = typer.Option(BOUNDARY_RECORDS_PATH, "--boundaries", help="Stage 5M boundary records."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Stage 5M summary."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5M output directory."),
) -> None:
    """Validate Stage 5M solved-fixture CUDA parity records."""

    try:
        counts, errors = validate_stage5m_results(
            run_records_path=_resolve(run_records),
            parity_records_path=_resolve(parity_records),
            boundaries_path=_resolve(boundaries),
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
    console.print("gematria_solved_fixture_cuda_stage5m_valid=true")


@gematria_solved_fixture_cuda_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Stage 5M summary.")) -> None:
    """Print the committed Stage 5M summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "input_mapping_records",
        "run_records",
        "cuda_attempted_count",
        "cuda_pass_count",
        "cuda_fail_count",
        "cuda_skip_count",
        "parity_records",
        "stage5n_ready",
        "selected_next_stage",
        "selected_next_stage_reason",
        "solved_fixture_cuda_execution_allowed",
        "unsolved_page_cuda_used",
        "real_liber_primus_cuda_data_used",
        "new_cuda_kernels_added",
        "cuda_source_modified",
        "gpu_benchmark_performed",
        "speedup_claim",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_solved_fixture_cuda_app, name="gematria-solved-fixture-cuda")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
