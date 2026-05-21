"""Stage 5R expanded solved-fixture-safe Gematria CUDA parity CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_expanded_solved_fixture_cuda.boundary_records import build_boundary_records
from libreprimus.gematria_expanded_solved_fixture_cuda.cuda_parity import run_cuda_parity
from libreprimus.gematria_expanded_solved_fixture_cuda.models import (
    BOUNDARY_RECORDS_PATH,
    BUILD_DIR,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    RUN_RECORDS_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    STAGE4I_CONFIDENCE_LABELS,
    STAGE4P_SUMMARY,
    STAGE5Q_CANDIDATE_INVENTORY,
    STAGE5Q_NATIVE_PARITY,
    STAGE5Q_SUMMARY,
    STAGE5Q_TOKEN_MAPPING,
    SUMMARY_PATH,
)
from libreprimus.gematria_expanded_solved_fixture_cuda.parity_records import build_parity_records
from libreprimus.gematria_expanded_solved_fixture_cuda.result_store_preflight import build_result_store_preflight
from libreprimus.gematria_expanded_solved_fixture_cuda.run_records import build_run_records
from libreprimus.gematria_expanded_solved_fixture_cuda.score_summary_preflight import build_score_summary_preflight
from libreprimus.gematria_expanded_solved_fixture_cuda.summary import build_summary, load_summary
from libreprimus.gematria_expanded_solved_fixture_cuda.validation import validate_stage5r_results
from libreprimus.paths import repo_root

gematria_expanded_solved_fixture_cuda_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_expanded_solved_fixture_cuda_app.command("build-run-records")
def build_run_records_command(
    candidate_inventory: Path = typer.Option(STAGE5Q_CANDIDATE_INVENTORY, "--candidate-inventory"),
    token_mapping: Path = typer.Option(STAGE5Q_TOKEN_MAPPING, "--token-mapping"),
    native_parity: Path = typer.Option(STAGE5Q_NATIVE_PARITY, "--native-parity"),
    run_records_out: Path = typer.Option(RUN_RECORDS_PATH, "--run-records-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build pending Stage 5R CUDA run records from Stage 5Q mappings."""

    for path in (candidate_inventory, token_mapping, native_parity):
        _require_file(path)
    records = build_run_records(
        candidate_inventory=_resolve(candidate_inventory),
        token_mapping=_resolve(token_mapping),
        native_parity=_resolve(native_parity),
        run_records_out=_resolve(run_records_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"run_records={len(records)}")
    console.print("exact_stage5q_mapped_candidate_scope=true")
    if not allow_warnings:
        return


@gematria_expanded_solved_fixture_cuda_app.command("run-cuda-parity")
def run_cuda_parity_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records"),
    run_records_out: Path = typer.Option(RUN_RECORDS_PATH, "--run-records-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    build_dir: Path = typer.Option(BUILD_DIR, "--build-dir"),
    skip_run: bool = typer.Option(False, "--skip-run"),
    require_cuda: bool = typer.Option(False, "--require-cuda"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Attempt the exact Stage 5R CUDA run, or record a no-GPU-safe skip."""

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
    failed = sum(1 for record in records if str(record["cuda_run_status"]).startswith("failed"))
    skipped = len(records) - passed - failed
    console.print(f"cuda_attempted_count={attempted}")
    console.print(f"cuda_pass_count={passed}")
    console.print(f"cuda_fail_count={failed}")
    console.print(f"cuda_skip_count={skipped}")
    if failed and not allow_warnings:
        raise typer.Exit(1)


@gematria_expanded_solved_fixture_cuda_app.command("build-parity-records")
def build_parity_records_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records"),
    parity_records_out: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5R CUDA/native parity records."""

    _require_file(run_records)
    records = build_parity_records(run_records=_resolve(run_records), parity_records_out=_resolve(parity_records_out), out_dir=_resolve(out_dir))
    passed = sum(1 for record in records if record["parity_status"] == "passed")
    failed = sum(1 for record in records if str(record["parity_status"]).startswith("failed"))
    console.print(f"parity_records={len(records)}")
    console.print(f"parity_pass_count={passed}")
    console.print(f"parity_fail_count={failed}")
    console.print(f"parity_skip_count={len(records) - passed - failed}")
    if not allow_warnings:
        return


@gematria_expanded_solved_fixture_cuda_app.command("build-boundary-records")
def build_boundary_records_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records"),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records"),
    boundaries_out: Path = typer.Option(BOUNDARY_RECORDS_PATH, "--boundaries-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5R safety boundary records."""

    for path in (run_records, parity_records):
        _require_file(path)
    records = build_boundary_records(
        run_records=_resolve(run_records),
        parity_records=_resolve(parity_records),
        boundaries_out=_resolve(boundaries_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"boundary_records={len(records)}")
    console.print(f"cuda_attempted_count={records[0]['cuda_attempted_count']}")
    if not allow_warnings:
        return


@gematria_expanded_solved_fixture_cuda_app.command("build-result-store-preflight")
def build_result_store_preflight_command(
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records"),
    stage4p_summary: Path = typer.Option(STAGE4P_SUMMARY, "--stage4p-summary"),
    result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5R result-store preflight records."""

    _require_file(parity_records)
    _require_file(stage4p_summary)
    records = build_result_store_preflight(
        parity_records=_resolve(parity_records),
        stage4p_summary=_resolve(stage4p_summary),
        result_store_preflight_out=_resolve(result_store_preflight_out),
        out_dir=_resolve(out_dir),
    )
    ready = sum(1 for record in records if record.get("stage5s_ready") is True)
    console.print(f"result_store_preflight_records={len(records)}")
    console.print(f"result_store_preflight_ready_count={ready}")
    if ready == 0 and not allow_warnings:
        raise typer.Exit(1)


@gematria_expanded_solved_fixture_cuda_app.command("build-score-summary-preflight")
def build_score_summary_preflight_command(
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records"),
    confidence_labels: Path = typer.Option(STAGE4I_CONFIDENCE_LABELS, "--confidence-labels"),
    score_summary_preflight_out: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH, "--score-summary-preflight-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5R score-summary preflight records."""

    _require_file(parity_records)
    _require_file(confidence_labels)
    records = build_score_summary_preflight(
        parity_records=_resolve(parity_records),
        confidence_labels=_resolve(confidence_labels),
        score_summary_preflight_out=_resolve(score_summary_preflight_out),
        out_dir=_resolve(out_dir),
    )
    ready = sum(1 for record in records if record.get("stage5s_ready") is True)
    console.print(f"score_summary_preflight_records={len(records)}")
    console.print(f"score_summary_preflight_ready_count={ready}")
    if ready == 0 and not allow_warnings:
        raise typer.Exit(1)


@gematria_expanded_solved_fixture_cuda_app.command("build-summary")
def build_summary_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records"),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records"),
    boundaries: Path = typer.Option(BOUNDARY_RECORDS_PATH, "--boundaries"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH, "--score-summary-preflight"),
    stage5q_summary: Path = typer.Option(STAGE5Q_SUMMARY, "--stage5q-summary"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build the committed Stage 5R summary."""

    for path in (run_records, parity_records, boundaries, result_store_preflight, score_summary_preflight, stage5q_summary):
        _require_file(path)
    payload = build_summary(
        run_records=_resolve(run_records),
        parity_records=_resolve(parity_records),
        boundaries=_resolve(boundaries),
        result_store_preflight=_resolve(result_store_preflight),
        score_summary_preflight=_resolve(score_summary_preflight),
        stage5q_summary=_resolve(stage5q_summary),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in ("run_records", "cuda_attempted_count", "parity_pass_count", "stage5s_ready", "selected_next_stage"):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@gematria_expanded_solved_fixture_cuda_app.command("validate-stage5r")
def validate_stage5r_command(
    run_records: Path = typer.Option(RUN_RECORDS_PATH, "--run-records"),
    parity_records: Path = typer.Option(PARITY_RECORDS_PATH, "--parity-records"),
    boundaries: Path = typer.Option(BOUNDARY_RECORDS_PATH, "--boundaries"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH, "--score-summary-preflight"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    """Validate Stage 5R expanded CUDA parity records."""

    try:
        counts, errors = validate_stage5r_results(
            run_records_path=_resolve(run_records),
            parity_records_path=_resolve(parity_records),
            boundaries_path=_resolve(boundaries),
            result_store_preflight_path=_resolve(result_store_preflight),
            score_summary_preflight_path=_resolve(score_summary_preflight),
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
    console.print("gematria_expanded_solved_fixture_cuda_stage5r_valid=true")


@gematria_expanded_solved_fixture_cuda_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    """Print the committed Stage 5R summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "input_stage5q_mapped_candidates",
        "run_records",
        "cuda_attempted_count",
        "cuda_pass_count",
        "cuda_fail_count",
        "cuda_skip_count",
        "parity_records",
        "parity_pass_count",
        "parity_fail_count",
        "parity_skip_count",
        "stage5s_ready",
        "selected_next_stage",
        "cuda_source_modified",
        "new_cuda_kernels_added",
        "device_kernel_arithmetic_modified",
        "gpu_benchmark_performed",
        "speedup_claim",
        "unsolved_page_cuda_used",
        "real_liber_primus_cuda_data_used",
        "solve_claim",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_expanded_solved_fixture_cuda_app, name="gematria-expanded-solved-fixture-cuda")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
