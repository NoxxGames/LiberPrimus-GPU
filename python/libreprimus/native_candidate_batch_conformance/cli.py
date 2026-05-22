"""Typer commands for Stage 5V native Candidate Batch ABI conformance."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.native_candidate_batch_conformance.adapter_records import build_adapter_records
from libreprimus.native_candidate_batch_conformance.fixtures import build_conformance_fixtures, run_python_reference_conformance
from libreprimus.native_candidate_batch_conformance.implementation_status import build_implementation_status
from libreprimus.native_candidate_batch_conformance.models import (
    ADAPTER_RECORDS_PATH,
    CONFORMANCE_FIXTURES_PATH,
    IMPLEMENTATION_STATUS_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESULT_STORE_CONFORMANCE_PATH,
    SCHEDULE_CONFORMANCE_PATH,
    SCORE_VECTOR_CONFORMANCE_PATH,
    SUMMARY_PATH,
    TOKEN_BUFFER_CONFORMANCE_PATH,
    TOPK_CONFORMANCE_PATH,
)
from libreprimus.native_candidate_batch_conformance.next_stage_decision import build_next_stage_decision
from libreprimus.native_candidate_batch_conformance.result_store_conformance import build_result_store_conformance
from libreprimus.native_candidate_batch_conformance.schedule_conformance import build_schedule_conformance
from libreprimus.native_candidate_batch_conformance.score_vector_conformance import build_score_vector_conformance
from libreprimus.native_candidate_batch_conformance.summary import build_summary, load_summary
from libreprimus.native_candidate_batch_conformance.token_buffer_conformance import build_token_buffer_conformance
from libreprimus.native_candidate_batch_conformance.topk_conformance import build_topk_conformance
from libreprimus.native_candidate_batch_conformance.validation import validate_stage5v_results
from libreprimus.paths import repo_root

native_candidate_batch_conformance_app = typer.Typer(no_args_is_help=True)
console = Console()


@native_candidate_batch_conformance_app.command("build-adapter-records")
def build_adapter_records_command(
    adapter_records_out: Path = typer.Option(ADAPTER_RECORDS_PATH, "--adapter-records-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_adapter_records(adapter_records_out=_resolve(adapter_records_out), out_dir=_resolve(out_dir))
    console.print(f"native_adapter_records={len(records)}")
    console.print("python_reference_adapter_implemented=true")
    console.print("cpp_reference_adapter_implemented=false")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-conformance-fixtures")
def build_conformance_fixtures_command(
    conformance_fixtures_out: Path = typer.Option(CONFORMANCE_FIXTURES_PATH, "--conformance-fixtures-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_conformance_fixtures(conformance_fixtures_out=_resolve(conformance_fixtures_out), out_dir=_resolve(out_dir))
    console.print(f"conformance_fixture_records={len(records)}")
    console.print(f"executed_conformance_fixture_count={sum(1 for record in records if record['execution_status'] == 'executed_python_reference')}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("run-native-conformance")
def run_native_conformance_command(
    conformance_fixtures: Path = typer.Option(CONFORMANCE_FIXTURES_PATH, "--conformance-fixtures"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    from libreprimus.native_candidate_batch_conformance.export import read_record_set

    _require_file(conformance_fixtures)
    report = run_python_reference_conformance(fixtures=read_record_set(_resolve(conformance_fixtures)), out_dir=_resolve(out_dir))
    console.print(f"executed_conformance_fixture_count={report['executed_conformance_fixture_count']}")
    console.print(f"passed_count={report['passed_count']}")
    console.print("native_cpu_execution_performed=false")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-token-buffer-conformance")
def build_token_buffer_conformance_command(
    conformance_fixtures: Path = typer.Option(CONFORMANCE_FIXTURES_PATH, "--conformance-fixtures"),
    token_buffer_conformance_out: Path = typer.Option(TOKEN_BUFFER_CONFORMANCE_PATH, "--token-buffer-conformance-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    from libreprimus.native_candidate_batch_conformance.export import read_record_set

    _require_file(conformance_fixtures)
    records = build_token_buffer_conformance(
        fixtures=read_record_set(_resolve(conformance_fixtures)),
        token_buffer_conformance_out=_resolve(token_buffer_conformance_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"token_buffer_conformance_records={len(records)}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-schedule-conformance")
def build_schedule_conformance_command(
    schedule_conformance_out: Path = typer.Option(SCHEDULE_CONFORMANCE_PATH, "--schedule-conformance-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_schedule_conformance(schedule_conformance_out=_resolve(schedule_conformance_out), out_dir=_resolve(out_dir))
    console.print(f"schedule_conformance_records={len(records)}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-score-vector-conformance")
def build_score_vector_conformance_command(
    score_vector_conformance_out: Path = typer.Option(SCORE_VECTOR_CONFORMANCE_PATH, "--score-vector-conformance-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_score_vector_conformance(score_vector_conformance_out=_resolve(score_vector_conformance_out), out_dir=_resolve(out_dir))
    console.print(f"score_vector_conformance_records={len(records)}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-topk-conformance")
def build_topk_conformance_command(
    topk_conformance_out: Path = typer.Option(TOPK_CONFORMANCE_PATH, "--topk-conformance-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_topk_conformance(topk_conformance_out=_resolve(topk_conformance_out), out_dir=_resolve(out_dir))
    console.print(f"topk_conformance_records={len(records)}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-result-store-conformance")
def build_result_store_conformance_command(
    result_store_conformance_out: Path = typer.Option(RESULT_STORE_CONFORMANCE_PATH, "--result-store-conformance-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_result_store_conformance(
        result_store_conformance_out=_resolve(result_store_conformance_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"result_store_conformance_records={len(records)}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-implementation-status")
def build_implementation_status_command(
    implementation_status_out: Path = typer.Option(IMPLEMENTATION_STATUS_PATH, "--implementation-status-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_implementation_status(implementation_status_out=_resolve(implementation_status_out), out_dir=_resolve(out_dir))
    console.print(f"abi_implementation_status_records={len(records)}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-next-stage-decision")
def build_next_stage_decision_command(
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_next_stage_decision(next_stage_decision_out=_resolve(next_stage_decision_out), out_dir=_resolve(out_dir))
    selected = next(record for record in records if record["selected"])
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("build-summary")
def build_summary_command(
    adapter_records: Path = typer.Option(ADAPTER_RECORDS_PATH, "--adapter-records"),
    conformance_fixtures: Path = typer.Option(CONFORMANCE_FIXTURES_PATH, "--conformance-fixtures"),
    token_buffer_conformance: Path = typer.Option(TOKEN_BUFFER_CONFORMANCE_PATH, "--token-buffer-conformance"),
    schedule_conformance: Path = typer.Option(SCHEDULE_CONFORMANCE_PATH, "--schedule-conformance"),
    score_vector_conformance: Path = typer.Option(SCORE_VECTOR_CONFORMANCE_PATH, "--score-vector-conformance"),
    topk_conformance: Path = typer.Option(TOPK_CONFORMANCE_PATH, "--topk-conformance"),
    result_store_conformance: Path = typer.Option(RESULT_STORE_CONFORMANCE_PATH, "--result-store-conformance"),
    implementation_status: Path = typer.Option(IMPLEMENTATION_STATUS_PATH, "--implementation-status"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    for path in (
        adapter_records,
        conformance_fixtures,
        token_buffer_conformance,
        schedule_conformance,
        score_vector_conformance,
        topk_conformance,
        result_store_conformance,
        implementation_status,
        next_stage_decision,
    ):
        _require_file(path)
    payload = build_summary(
        adapter_records=_resolve(adapter_records),
        conformance_fixtures=_resolve(conformance_fixtures),
        token_buffer_conformance=_resolve(token_buffer_conformance),
        schedule_conformance=_resolve(schedule_conformance),
        score_vector_conformance=_resolve(score_vector_conformance),
        topk_conformance=_resolve(topk_conformance),
        result_store_conformance=_resolve(result_store_conformance),
        implementation_status=_resolve(implementation_status),
        next_stage_decision=_resolve(next_stage_decision),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"conformance_fixture_records={payload['conformance_fixture_records']}")
    console.print(f"executed_conformance_fixture_count={payload['executed_conformance_fixture_count']}")
    console.print(f"recommended_next_stage_title={payload['recommended_next_stage_title']}")
    if not allow_warnings:
        return


@native_candidate_batch_conformance_app.command("validate-stage5v")
def validate_stage5v_command(
    adapter_records: Path = typer.Option(ADAPTER_RECORDS_PATH, "--adapter-records"),
    conformance_fixtures: Path = typer.Option(CONFORMANCE_FIXTURES_PATH, "--conformance-fixtures"),
    token_buffer_conformance: Path = typer.Option(TOKEN_BUFFER_CONFORMANCE_PATH, "--token-buffer-conformance"),
    schedule_conformance: Path = typer.Option(SCHEDULE_CONFORMANCE_PATH, "--schedule-conformance"),
    score_vector_conformance: Path = typer.Option(SCORE_VECTOR_CONFORMANCE_PATH, "--score-vector-conformance"),
    topk_conformance: Path = typer.Option(TOPK_CONFORMANCE_PATH, "--topk-conformance"),
    result_store_conformance: Path = typer.Option(RESULT_STORE_CONFORMANCE_PATH, "--result-store-conformance"),
    implementation_status: Path = typer.Option(IMPLEMENTATION_STATUS_PATH, "--implementation-status"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    counts, errors = validate_stage5v_results(
        adapter_records_path=_resolve(adapter_records),
        conformance_fixtures_path=_resolve(conformance_fixtures),
        token_buffer_conformance_path=_resolve(token_buffer_conformance),
        schedule_conformance_path=_resolve(schedule_conformance),
        score_vector_conformance_path=_resolve(score_vector_conformance),
        topk_conformance_path=_resolve(topk_conformance),
        result_store_conformance_path=_resolve(result_store_conformance),
        implementation_status_path=_resolve(implementation_status),
        next_stage_decision_path=_resolve(next_stage_decision),
        summary_path=_resolve(summary),
        results_dir=_resolve(results_dir),
    )
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("native_candidate_batch_conformance_stage5v_valid=true")


@native_candidate_batch_conformance_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    payload = load_summary(_resolve(summary))
    for key in (
        "native_adapter_records",
        "conformance_fixture_records",
        "executed_conformance_fixture_count",
        "shape_only_fixture_count",
        "token_buffer_conformance_records",
        "schedule_conformance_records",
        "score_vector_conformance_records",
        "topk_conformance_records",
        "result_store_conformance_records",
        "abi_implementation_status_records",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload[key]}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(native_candidate_batch_conformance_app, name="native-candidate-batch-conformance")


def _resolve(path: Path) -> Path:
    if path.is_absolute():
        return path
    return repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]missing_file={path}[/red]")
        raise typer.Exit(1)
