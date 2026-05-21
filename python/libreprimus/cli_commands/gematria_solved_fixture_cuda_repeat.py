"""Stage 5O Gematria CUDA repeat-verification CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_solved_fixture_cuda_repeat.expansion_decision import build_expansion_decision
from libreprimus.gematria_solved_fixture_cuda_repeat.models import (
    BUILD_DIR,
    EXPANSION_DECISION_PATH,
    OUTPUT_DIR,
    REPEAT_PARITY_PATH,
    REPEAT_RUN_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    STAGE4P_SUMMARY,
    STAGE5L_NATIVE_PARITY,
    STAGE5M_PARITY_RECORDS,
    STAGE5M_RUN_RECORDS,
    STAGE5M_SUMMARY,
    STAGE5N_SUMMARY,
    SUMMARY_PATH,
)
from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_parity import build_repeat_parity_records
from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_run_records import build_repeat_run_records
from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_verification import run_repeat_verification
from libreprimus.gematria_solved_fixture_cuda_repeat.result_store_preflight import build_result_store_preflight
from libreprimus.gematria_solved_fixture_cuda_repeat.score_summary_preflight import build_score_summary_preflight
from libreprimus.gematria_solved_fixture_cuda_repeat.summary import build_summary, load_summary
from libreprimus.gematria_solved_fixture_cuda_repeat.validation import validate_stage5o_results
from libreprimus.paths import repo_root

gematria_solved_fixture_cuda_repeat_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_solved_fixture_cuda_repeat_app.command("build-repeat-run-records")
def build_repeat_run_records_command(
    stage5m_run_records: Path = typer.Option(STAGE5M_RUN_RECORDS, "--stage5m-run-records"),
    stage5m_parity_records: Path = typer.Option(STAGE5M_PARITY_RECORDS, "--stage5m-parity-records"),
    stage5l_native_parity: Path = typer.Option(STAGE5L_NATIVE_PARITY, "--stage5l-native-parity"),
    repeat_run_out: Path = typer.Option(REPEAT_RUN_PATH, "--repeat-run-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build pending Stage 5O repeat run records from Stage 5M/5L records."""

    for path in (stage5m_run_records, stage5m_parity_records, stage5l_native_parity):
        _require_file(path)
    records = build_repeat_run_records(
        stage5m_run_records=_resolve(stage5m_run_records),
        stage5m_parity_records=_resolve(stage5m_parity_records),
        stage5l_native_parity=_resolve(stage5l_native_parity),
        repeat_run_out=_resolve(repeat_run_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"repeat_run_records={len(records)}")
    console.print("exact_stage5m_repeat_scope=true")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_repeat_app.command("run-repeat-verification")
def run_repeat_verification_command(
    repeat_run: Path = typer.Option(REPEAT_RUN_PATH, "--repeat-run", "--repeat-run-records"),
    repeat_run_out: Path = typer.Option(REPEAT_RUN_PATH, "--repeat-run-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    build_dir: Path = typer.Option(BUILD_DIR, "--build-dir"),
    skip_run: bool = typer.Option(False, "--skip-run"),
    require_cuda: bool = typer.Option(False, "--require-cuda"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Attempt the exact Stage 5M CUDA repeat, or record a no-GPU-safe skip."""

    _require_file(repeat_run)
    try:
        records = run_repeat_verification(
            repeat_run_records=_resolve(repeat_run),
            repeat_run_out=_resolve(repeat_run_out),
            out_dir=_resolve(out_dir),
            build_dir=_resolve(build_dir),
            skip_run=skip_run,
            require_cuda=require_cuda,
        )
    except RuntimeError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    attempted = sum(1 for record in records if record["repeat_cuda_attempted"])
    passed = sum(1 for record in records if record["repeat_cuda_status"] == "passed")
    failed = sum(1 for record in records if str(record["repeat_cuda_status"]).startswith("failed"))
    skipped = len(records) - passed - failed
    console.print(f"repeat_cuda_attempted_count={attempted}")
    console.print(f"repeat_cuda_pass_count={passed}")
    console.print(f"repeat_cuda_fail_count={failed}")
    console.print(f"repeat_cuda_skip_count={skipped}")
    if failed and not allow_warnings:
        raise typer.Exit(1)


@gematria_solved_fixture_cuda_repeat_app.command("build-repeat-parity-records")
def build_repeat_parity_records_command(
    repeat_run: Path = typer.Option(REPEAT_RUN_PATH, "--repeat-run", "--repeat-run-records"),
    repeat_parity_out: Path = typer.Option(REPEAT_PARITY_PATH, "--repeat-parity-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5O repeat parity records."""

    _require_file(repeat_run)
    records = build_repeat_parity_records(
        repeat_run_records=_resolve(repeat_run),
        repeat_parity_out=_resolve(repeat_parity_out),
        out_dir=_resolve(out_dir),
    )
    passed = sum(1 for record in records if record["repeat_parity_status"] == "passed")
    failed = sum(1 for record in records if str(record["repeat_parity_status"]).startswith("failed"))
    console.print(f"repeat_parity_records={len(records)}")
    console.print(f"repeat_parity_pass_count={passed}")
    console.print(f"repeat_parity_fail_count={failed}")
    console.print(f"repeat_parity_skip_count={len(records) - passed - failed}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_repeat_app.command("build-result-store-preflight")
def build_result_store_preflight_command(
    repeat_parity: Path = typer.Option(REPEAT_PARITY_PATH, "--repeat-parity"),
    stage4p_summary: Path = typer.Option(STAGE4P_SUMMARY, "--stage4p-summary"),
    result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5O result-store preflight records."""

    _require_file(repeat_parity)
    records = build_result_store_preflight(
        repeat_parity=_resolve(repeat_parity),
        stage4p_summary=stage4p_summary,
        result_store_preflight_out=_resolve(result_store_preflight_out),
        out_dir=_resolve(out_dir),
    )
    ready = sum(1 for record in records if record.get("stage5p_ready") is True)
    console.print(f"result_store_preflight_records={len(records)}")
    console.print(f"result_store_preflight_ready_count={ready}")
    if ready == 0 and not allow_warnings:
        raise typer.Exit(1)


@gematria_solved_fixture_cuda_repeat_app.command("build-score-summary-preflight")
def build_score_summary_preflight_command(
    repeat_parity: Path = typer.Option(REPEAT_PARITY_PATH, "--repeat-parity"),
    score_summary_preflight_out: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH, "--score-summary-preflight-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5O score-summary preflight records."""

    _require_file(repeat_parity)
    records = build_score_summary_preflight(
        repeat_parity=_resolve(repeat_parity),
        score_summary_preflight_out=_resolve(score_summary_preflight_out),
        out_dir=_resolve(out_dir),
    )
    ready = sum(1 for record in records if record.get("stage5p_ready") is True)
    console.print(f"score_summary_preflight_records={len(records)}")
    console.print(f"score_summary_preflight_ready_count={ready}")
    if ready == 0 and not allow_warnings:
        raise typer.Exit(1)


@gematria_solved_fixture_cuda_repeat_app.command("build-expansion-decision")
def build_expansion_decision_command(
    repeat_parity: Path = typer.Option(REPEAT_PARITY_PATH, "--repeat-parity"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH, "--score-summary-preflight"),
    expansion_decision_out: Path = typer.Option(EXPANSION_DECISION_PATH, "--expansion-decision-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build the Stage 5O expansion decision record."""

    for path in (repeat_parity, result_store_preflight, score_summary_preflight):
        _require_file(path)
    records = build_expansion_decision(
        repeat_parity=_resolve(repeat_parity),
        result_store_preflight=_resolve(result_store_preflight),
        score_summary_preflight=_resolve(score_summary_preflight),
        expansion_decision_out=_resolve(expansion_decision_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"expansion_decision_records={len(records)}")
    console.print(f"decision_status={records[0]['decision_status']}")
    console.print(f"selected_next_stage={records[0]['selected_next_stage']}")
    if records[0]["decision_status"] != "stage5p_ready" and not allow_warnings:
        raise typer.Exit(1)


@gematria_solved_fixture_cuda_repeat_app.command("build-summary")
def build_summary_command(
    repeat_run: Path = typer.Option(REPEAT_RUN_PATH, "--repeat-run", "--repeat-run-records"),
    repeat_parity: Path = typer.Option(REPEAT_PARITY_PATH, "--repeat-parity", "--repeat-parity-records"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH, "--score-summary-preflight"),
    expansion_decision: Path = typer.Option(EXPANSION_DECISION_PATH, "--expansion-decision"),
    stage5m_summary: Path = typer.Option(STAGE5M_SUMMARY, "--stage5m-summary"),
    stage5n_summary: Path = typer.Option(STAGE5N_SUMMARY, "--stage5n-summary"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build the committed Stage 5O summary."""

    for path in (
        repeat_run,
        repeat_parity,
        result_store_preflight,
        score_summary_preflight,
        expansion_decision,
        stage5m_summary,
        stage5n_summary,
    ):
        _require_file(path)
    payload = build_summary(
        repeat_run_records=_resolve(repeat_run),
        repeat_parity_records=_resolve(repeat_parity),
        result_store_preflight=_resolve(result_store_preflight),
        score_summary_preflight=_resolve(score_summary_preflight),
        expansion_decision=_resolve(expansion_decision),
        stage5m_summary=_resolve(stage5m_summary),
        stage5n_summary=_resolve(stage5n_summary),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in ("repeat_run_records", "repeat_parity_pass_count", "stage5p_ready", "selected_next_stage"):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_repeat_app.command("validate-stage5o")
def validate_stage5o_command(
    repeat_run: Path = typer.Option(REPEAT_RUN_PATH, "--repeat-run", "--repeat-run-records"),
    repeat_parity: Path = typer.Option(REPEAT_PARITY_PATH, "--repeat-parity", "--repeat-parity-records"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH, "--score-summary-preflight"),
    expansion_decision: Path = typer.Option(EXPANSION_DECISION_PATH, "--expansion-decision"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    """Validate Stage 5O repeat verification records."""

    try:
        counts, errors = validate_stage5o_results(
            repeat_run_path=_resolve(repeat_run),
            repeat_parity_path=_resolve(repeat_parity),
            result_store_preflight_path=_resolve(result_store_preflight),
            score_summary_preflight_path=_resolve(score_summary_preflight),
            expansion_decision_path=_resolve(expansion_decision),
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
    console.print("gematria_solved_fixture_cuda_repeat_stage5o_valid=true")


@gematria_solved_fixture_cuda_repeat_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    """Print the committed Stage 5O summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "repeat_run_records",
        "repeat_cuda_attempted_count",
        "repeat_cuda_pass_count",
        "repeat_cuda_fail_count",
        "repeat_cuda_skip_count",
        "repeat_parity_records",
        "result_store_preflight_ready_count",
        "score_summary_preflight_ready_count",
        "stage5p_ready",
        "selected_next_stage",
        "cuda_source_modified",
        "new_cuda_kernels_added",
        "gpu_benchmark_performed",
        "speedup_claim",
        "unsolved_page_cuda_used",
        "solve_claim",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_solved_fixture_cuda_repeat_app, name="gematria-solved-fixture-cuda-repeat")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
