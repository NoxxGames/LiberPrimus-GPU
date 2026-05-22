"""Stage 5U Candidate Batch ABI CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_candidate_batch_abi.backend_surface_contract import build_backend_surface_contract
from libreprimus.cuda_candidate_batch_abi.candidate_batch_abi import build_candidate_batch_abi
from libreprimus.cuda_candidate_batch_abi.gap_closure import build_gap_closure
from libreprimus.cuda_candidate_batch_abi.key_schedule_contract import build_key_schedule_contract
from libreprimus.cuda_candidate_batch_abi.models import (
    ABI_GAP_CLOSURE_PATH,
    BACKEND_SURFACE_CONTRACT_PATH,
    CANDIDATE_BATCH_ABI_PATH,
    KEY_SCHEDULE_CONTRACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESULT_STORE_COMPATIBILITY_PATH,
    SCORE_VECTOR_CONTRACT_PATH,
    STAGE5T_GAPS,
    STAGE5T_SUMMARY,
    STREAM_SCHEDULE_CONTRACT_PATH,
    SUMMARY_PATH,
    TOKEN_BUFFER_CONTRACT_PATH,
    TOPK_OUTPUT_CONTRACT_PATH,
    TRANSFORM_PARAMETER_CONTRACT_PATH,
)
from libreprimus.cuda_candidate_batch_abi.next_stage_decision import build_next_stage_decision
from libreprimus.cuda_candidate_batch_abi.result_store_compatibility import build_result_store_compatibility
from libreprimus.cuda_candidate_batch_abi.score_vector_contract import build_score_vector_contract
from libreprimus.cuda_candidate_batch_abi.stream_schedule_contract import build_stream_schedule_contract
from libreprimus.cuda_candidate_batch_abi.summary import build_summary, load_summary
from libreprimus.cuda_candidate_batch_abi.token_buffer_contract import build_token_buffer_contract
from libreprimus.cuda_candidate_batch_abi.topk_output_contract import build_topk_output_contract
from libreprimus.cuda_candidate_batch_abi.transform_parameter_contract import build_transform_parameter_contract
from libreprimus.cuda_candidate_batch_abi.validation import validate_stage5u_results
from libreprimus.paths import repo_root

cuda_candidate_batch_abi_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_candidate_batch_abi_app.command("build-candidate-batch-abi")
def build_candidate_batch_abi_command(
    candidate_batch_abi_out: Path = typer.Option(CANDIDATE_BATCH_ABI_PATH, "--candidate-batch-abi-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_candidate_batch_abi(candidate_batch_abi_out=_resolve(candidate_batch_abi_out), out_dir=_resolve(out_dir))
    console.print(f"candidate_batch_abi_records={len(records)}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-token-buffer-contract")
def build_token_buffer_contract_command(
    token_buffer_contract_out: Path = typer.Option(TOKEN_BUFFER_CONTRACT_PATH, "--token-buffer-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_token_buffer_contract(token_buffer_contract_out=_resolve(token_buffer_contract_out), out_dir=_resolve(out_dir))
    console.print(f"token_buffer_contract_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-transform-parameter-contract")
def build_transform_parameter_contract_command(
    transform_parameter_contract_out: Path = typer.Option(TRANSFORM_PARAMETER_CONTRACT_PATH, "--transform-parameter-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_transform_parameter_contract(transform_parameter_contract_out=_resolve(transform_parameter_contract_out), out_dir=_resolve(out_dir))
    console.print(f"transform_parameter_contract_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-key-schedule-contract")
def build_key_schedule_contract_command(
    key_schedule_contract_out: Path = typer.Option(KEY_SCHEDULE_CONTRACT_PATH, "--key-schedule-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_key_schedule_contract(key_schedule_contract_out=_resolve(key_schedule_contract_out), out_dir=_resolve(out_dir))
    console.print(f"key_schedule_contract_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-stream-schedule-contract")
def build_stream_schedule_contract_command(
    stream_schedule_contract_out: Path = typer.Option(STREAM_SCHEDULE_CONTRACT_PATH, "--stream-schedule-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_stream_schedule_contract(stream_schedule_contract_out=_resolve(stream_schedule_contract_out), out_dir=_resolve(out_dir))
    console.print(f"stream_schedule_contract_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-score-vector-contract")
def build_score_vector_contract_command(
    score_vector_contract_out: Path = typer.Option(SCORE_VECTOR_CONTRACT_PATH, "--score-vector-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_score_vector_contract(score_vector_contract_out=_resolve(score_vector_contract_out), out_dir=_resolve(out_dir))
    console.print(f"score_vector_contract_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-topk-output-contract")
def build_topk_output_contract_command(
    topk_output_contract_out: Path = typer.Option(TOPK_OUTPUT_CONTRACT_PATH, "--topk-output-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_topk_output_contract(topk_output_contract_out=_resolve(topk_output_contract_out), out_dir=_resolve(out_dir))
    console.print(f"topk_output_contract_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-backend-surface-contract")
def build_backend_surface_contract_command(
    backend_surface_contract_out: Path = typer.Option(BACKEND_SURFACE_CONTRACT_PATH, "--backend-surface-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_backend_surface_contract(backend_surface_contract_out=_resolve(backend_surface_contract_out), out_dir=_resolve(out_dir))
    console.print(f"backend_surface_contract_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-result-store-compatibility")
def build_result_store_compatibility_command(
    result_store_compatibility_out: Path = typer.Option(RESULT_STORE_COMPATIBILITY_PATH, "--result-store-compatibility-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_result_store_compatibility(
        result_store_compatibility_out=_resolve(result_store_compatibility_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"result_store_compatibility_records={len(records)}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-gap-closure")
def build_gap_closure_command(
    stage5t_gaps: Path = typer.Option(STAGE5T_GAPS, "--stage5t-gaps"),
    gap_closure_out: Path = typer.Option(ABI_GAP_CLOSURE_PATH, "--gap-closure-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    _require_file(stage5t_gaps)
    records = build_gap_closure(stage5t_gaps=_resolve(stage5t_gaps), gap_closure_out=_resolve(gap_closure_out), out_dir=_resolve(out_dir))
    console.print(f"abi_gap_closure_records={len(records)}")
    console.print(f"stage5t_gaps_closed_by_contract_count={sum(1 for record in records if record['stage5u_closure_status'] == 'closed_by_contract')}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-next-stage-decision")
def build_next_stage_decision_command(
    gap_closure: Path = typer.Option(ABI_GAP_CLOSURE_PATH, "--gap-closure"),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    _require_file(gap_closure)
    records = build_next_stage_decision(gap_closure=_resolve(gap_closure), next_stage_decision_out=_resolve(next_stage_decision_out), out_dir=_resolve(out_dir))
    selected = next(record for record in records if record["selected"])
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("build-summary")
def build_summary_command(
    candidate_batch_abi: Path = typer.Option(CANDIDATE_BATCH_ABI_PATH, "--candidate-batch-abi"),
    token_buffer_contract: Path = typer.Option(TOKEN_BUFFER_CONTRACT_PATH, "--token-buffer-contract"),
    transform_parameter_contract: Path = typer.Option(TRANSFORM_PARAMETER_CONTRACT_PATH, "--transform-parameter-contract"),
    key_schedule_contract: Path = typer.Option(KEY_SCHEDULE_CONTRACT_PATH, "--key-schedule-contract"),
    stream_schedule_contract: Path = typer.Option(STREAM_SCHEDULE_CONTRACT_PATH, "--stream-schedule-contract"),
    score_vector_contract: Path = typer.Option(SCORE_VECTOR_CONTRACT_PATH, "--score-vector-contract"),
    topk_output_contract: Path = typer.Option(TOPK_OUTPUT_CONTRACT_PATH, "--topk-output-contract"),
    backend_surface_contract: Path = typer.Option(BACKEND_SURFACE_CONTRACT_PATH, "--backend-surface-contract"),
    result_store_compatibility: Path = typer.Option(RESULT_STORE_COMPATIBILITY_PATH, "--result-store-compatibility"),
    gap_closure: Path = typer.Option(ABI_GAP_CLOSURE_PATH, "--gap-closure"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    stage5t_gaps: Path = typer.Option(STAGE5T_GAPS, "--stage5t-gaps"),
    stage5t_summary: Path = typer.Option(STAGE5T_SUMMARY, "--stage5t-summary"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    for path in (
        candidate_batch_abi,
        token_buffer_contract,
        transform_parameter_contract,
        key_schedule_contract,
        stream_schedule_contract,
        score_vector_contract,
        topk_output_contract,
        backend_surface_contract,
        result_store_compatibility,
        gap_closure,
        next_stage_decision,
        stage5t_gaps,
        stage5t_summary,
    ):
        _require_file(path)
    payload = build_summary(
        candidate_batch_abi=_resolve(candidate_batch_abi),
        token_buffer_contract=_resolve(token_buffer_contract),
        transform_parameter_contract=_resolve(transform_parameter_contract),
        key_schedule_contract=_resolve(key_schedule_contract),
        stream_schedule_contract=_resolve(stream_schedule_contract),
        score_vector_contract=_resolve(score_vector_contract),
        topk_output_contract=_resolve(topk_output_contract),
        backend_surface_contract=_resolve(backend_surface_contract),
        result_store_compatibility=_resolve(result_store_compatibility),
        gap_closure=_resolve(gap_closure),
        next_stage_decision=_resolve(next_stage_decision),
        stage5t_gaps=_resolve(stage5t_gaps),
        stage5t_summary=_resolve(stage5t_summary),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in ("candidate_batch_abi_records", "token_buffer_contract_records", "recommended_next_stage_title"):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@cuda_candidate_batch_abi_app.command("validate-stage5u")
def validate_stage5u_command(
    candidate_batch_abi: Path = typer.Option(CANDIDATE_BATCH_ABI_PATH, "--candidate-batch-abi"),
    token_buffer_contract: Path = typer.Option(TOKEN_BUFFER_CONTRACT_PATH, "--token-buffer-contract"),
    transform_parameter_contract: Path = typer.Option(TRANSFORM_PARAMETER_CONTRACT_PATH, "--transform-parameter-contract"),
    key_schedule_contract: Path = typer.Option(KEY_SCHEDULE_CONTRACT_PATH, "--key-schedule-contract"),
    stream_schedule_contract: Path = typer.Option(STREAM_SCHEDULE_CONTRACT_PATH, "--stream-schedule-contract"),
    score_vector_contract: Path = typer.Option(SCORE_VECTOR_CONTRACT_PATH, "--score-vector-contract"),
    topk_output_contract: Path = typer.Option(TOPK_OUTPUT_CONTRACT_PATH, "--topk-output-contract"),
    backend_surface_contract: Path = typer.Option(BACKEND_SURFACE_CONTRACT_PATH, "--backend-surface-contract"),
    result_store_compatibility: Path = typer.Option(RESULT_STORE_COMPATIBILITY_PATH, "--result-store-compatibility"),
    gap_closure: Path = typer.Option(ABI_GAP_CLOSURE_PATH, "--gap-closure"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    counts, errors = validate_stage5u_results(
        candidate_batch_abi_path=_resolve(candidate_batch_abi),
        token_buffer_contract_path=_resolve(token_buffer_contract),
        transform_parameter_contract_path=_resolve(transform_parameter_contract),
        key_schedule_contract_path=_resolve(key_schedule_contract),
        stream_schedule_contract_path=_resolve(stream_schedule_contract),
        score_vector_contract_path=_resolve(score_vector_contract),
        topk_output_contract_path=_resolve(topk_output_contract),
        backend_surface_contract_path=_resolve(backend_surface_contract),
        result_store_compatibility_path=_resolve(result_store_compatibility),
        gap_closure_path=_resolve(gap_closure),
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
    console.print("cuda_candidate_batch_abi_stage5u_valid=true")


@cuda_candidate_batch_abi_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    payload = load_summary(_resolve(summary))
    for key in (
        "candidate_batch_abi_records",
        "token_buffer_contract_records",
        "transform_parameter_contract_records",
        "key_schedule_contract_records",
        "stream_schedule_contract_records",
        "score_vector_contract_records",
        "topk_output_contract_records",
        "backend_surface_contract_records",
        "result_store_compatibility_records",
        "abi_gap_closure_records",
        "next_stage_decision_records",
        "stage5t_gaps_closed_by_contract_count",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload[key]}")


def register(root_app: typer.Typer) -> None:
    """Register the Stage 5U command group."""

    root_app.add_typer(cuda_candidate_batch_abi_app, name="cuda-candidate-batch-abi")


def _resolve(path: Path) -> Path:
    if path.is_absolute():
        return path
    return repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]missing_file={path}[/red]")
        raise typer.Exit(1)
