"""Typer commands for Stage 5AD bounded p56 CUDA parity."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .device_subset_audit import build_device_subset_audit
from .doc_staleness_validation import build_doc_staleness_validation
from .full_p56_blocker import build_full_p56_blocker
from .models import (
    CUDA_PARITY_PATH,
    CUDA_RUN_PATH,
    DEVICE_SUBSET_AUDIT_PATH,
    DOC_STALENESS_VALIDATION_PATH,
    FULL_P56_BLOCKER_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SUMMARY_PATH,
)
from .next_stage_decision import build_next_stage_decision
from .parity_records import build_parity_records
from .result_store_preflight import build_result_store_preflight
from .run_records import build_run_records, run_bounded_p56_cuda
from .score_summary_preflight import build_score_summary_preflight
from .scored_experiment_deferral import build_scored_experiment_deferral
from .summary import build_summary
from .validation import validate_stage5ad_results

console = Console()
app = typer.Typer(help="Stage 5AD bounded p56 CUDA parity commands.", no_args_is_help=True)


@app.command("build-run-records")
def build_run_records_command(cuda_run_out: Path = typer.Option(CUDA_RUN_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_run_records(cuda_run_out=cuda_run_out, out_dir=out_dir)
    console.print(f"cuda_run_records={len(records)}")
    console.print(f"cuda_execution_status={records[0]['cuda_execution_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("run-bounded-p56-cuda")
def run_bounded_p56_cuda_command(
    cuda_run_out: Path = typer.Option(CUDA_RUN_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    build_dir: Path = typer.Option(Path("build/stage5ad-bounded-p56-cuda")),
    skip_cuda: bool = typer.Option(False),
    require_cuda: bool = typer.Option(False),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = run_bounded_p56_cuda(cuda_run_out=cuda_run_out, out_dir=out_dir, build_dir=build_dir, skip_cuda=skip_cuda, require_cuda=require_cuda)
    record = records[0]
    console.print(f"cuda_run_records={len(records)}")
    console.print(f"cuda_execution_status={record['cuda_execution_status']}")
    console.print(f"cuda_attempted_count={record['cuda_attempted_count']}")
    console.print(f"cuda_pass_count={record['cuda_pass_count']}")
    console.print(f"cuda_fail_count={record['cuda_fail_count']}")
    console.print(f"cuda_skip_count={record['cuda_skip_count']}")
    console.print(f"computed_cuda_output_token_hash={record.get('computed_cuda_output_token_hash') or ''}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-parity-records")
def build_parity_records_command(cuda_run: Path = typer.Option(CUDA_RUN_PATH), cuda_parity_out: Path = typer.Option(CUDA_PARITY_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_parity_records(cuda_run=cuda_run, cuda_parity_out=cuda_parity_out, out_dir=out_dir)
    console.print(f"cuda_parity_records={len(records)}")
    console.print(f"parity_status={records[0]['parity_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-result-store-preflight")
def build_result_store_command(cuda_parity: Path = typer.Option(CUDA_PARITY_PATH), result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_result_store_preflight(cuda_parity=cuda_parity, result_store_preflight_out=result_store_preflight_out, out_dir=out_dir)
    console.print(f"result_store_preflight_records={len(records)}")
    console.print(f"preflight_status={records[0]['preflight_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-score-summary-preflight")
def build_score_summary_command(cuda_parity: Path = typer.Option(CUDA_PARITY_PATH), score_summary_preflight_out: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_score_summary_preflight(cuda_parity=cuda_parity, score_summary_preflight_out=score_summary_preflight_out, out_dir=out_dir)
    console.print(f"score_summary_preflight_records={len(records)}")
    console.print(f"confidence_interpretation={records[0]['confidence_interpretation']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-full-p56-blocker")
def build_full_p56_command(full_p56_blocker_out: Path = typer.Option(FULL_P56_BLOCKER_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_full_p56_blocker(full_p56_blocker_out=full_p56_blocker_out, out_dir=out_dir)
    console.print(f"full_p56_blocker_records={len(records)}")
    console.print(f"full_p56_status={records[0]['full_p56_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-scored-experiment-deferral")
def build_scored_deferral_command(scored_experiment_deferral_out: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_scored_experiment_deferral(scored_experiment_deferral_out=scored_experiment_deferral_out, out_dir=out_dir)
    console.print(f"scored_experiment_deferral_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-doc-staleness-validation")
def build_doc_staleness_command(doc_staleness_validation_out: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_doc_staleness_validation(doc_staleness_validation_out=doc_staleness_validation_out, out_dir=out_dir)
    console.print(f"doc_staleness_validation_records={len(records)}")
    console.print(f"doc_staleness_strict_check_passed={str(records[0]['doc_staleness_strict_check_passed']).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-device-subset-audit")
def build_device_audit_command(device_subset_audit_out: Path = typer.Option(DEVICE_SUBSET_AUDIT_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_device_subset_audit(device_subset_audit_out=device_subset_audit_out, out_dir=out_dir)
    console.print(f"device_subset_audit_records={len(records)}")
    console.print(f"cuda_source_modified={str(records[0]['cuda_source_modified']).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_next_stage_command(cuda_parity: Path = typer.Option(CUDA_PARITY_PATH), next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH), out_dir: Path = typer.Option(OUTPUT_DIR), allow_warnings: bool = typer.Option(False)) -> None:
    records = build_next_stage_decision(cuda_parity=cuda_parity, next_stage_decision_out=next_stage_decision_out, out_dir=out_dir)
    selected = next(record for record in records if record.get("selected") is True)
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-summary")
def build_summary_command(
    cuda_run: Path = typer.Option(CUDA_RUN_PATH),
    cuda_parity: Path = typer.Option(CUDA_PARITY_PATH),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    device_subset_audit: Path = typer.Option(DEVICE_SUBSET_AUDIT_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    summary = build_summary(
        cuda_run=cuda_run,
        cuda_parity=cuda_parity,
        result_store_preflight=result_store_preflight,
        score_summary_preflight=score_summary_preflight,
        full_p56_blocker=full_p56_blocker,
        scored_experiment_deferral=scored_experiment_deferral,
        doc_staleness_validation=doc_staleness_validation,
        device_subset_audit=device_subset_audit,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"stage5ad_parity_status={summary['stage5ad_parity_status']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5ad")
def validate_stage5ad(
    cuda_run: Path = typer.Option(CUDA_RUN_PATH),
    cuda_parity: Path = typer.Option(CUDA_PARITY_PATH),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    device_subset_audit: Path = typer.Option(DEVICE_SUBSET_AUDIT_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5ad_results(
        cuda_run_path=cuda_run,
        cuda_parity_path=cuda_parity,
        result_store_preflight_path=result_store_preflight,
        score_summary_preflight_path=score_summary_preflight,
        full_p56_blocker_path=full_p56_blocker,
        scored_experiment_deferral_path=scored_experiment_deferral,
        doc_staleness_validation_path=doc_staleness_validation,
        device_subset_audit_path=device_subset_audit,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("bounded_p56_cuda_parity_stage5ad_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from .export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "stage5ad_parity_status",
        "expected_output_token_hash",
        "computed_cuda_output_token_hash",
        "cuda_attempted_count",
        "cuda_pass_count",
        "cuda_fail_count",
        "cuda_skip_count",
        "full_p56_status",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="bounded-p56-cuda-parity")
