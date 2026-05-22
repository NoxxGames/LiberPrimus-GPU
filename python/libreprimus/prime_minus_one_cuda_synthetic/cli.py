"""Typer commands for Stage 5AA prime-minus-one CUDA synthetic parity."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.prime_minus_one_cuda_synthetic.device_subset_audit import build_device_subset_audit
from libreprimus.prime_minus_one_cuda_synthetic.kernel_implementation import build_kernel_implementation_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    CUDA_RUN_PATH,
    DEVICE_SUBSET_AUDIT_PATH,
    KERNEL_IMPLEMENTATION_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    P56_BLOCKER_PATH,
    PARITY_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SUMMARY_PATH,
)
from libreprimus.prime_minus_one_cuda_synthetic.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_cuda_synthetic.p56_blocker import build_p56_blocker
from libreprimus.prime_minus_one_cuda_synthetic.parity_records import build_parity_records
from libreprimus.prime_minus_one_cuda_synthetic.result_store_preflight import build_result_store_preflight
from libreprimus.prime_minus_one_cuda_synthetic.run_records import build_run_records, run_synthetic_cuda_parity
from libreprimus.prime_minus_one_cuda_synthetic.scored_experiment_deferral import build_scored_experiment_deferral
from libreprimus.prime_minus_one_cuda_synthetic.summary import build_summary
from libreprimus.prime_minus_one_cuda_synthetic.validation import validate_stage5aa_results

console = Console()
app = typer.Typer(help="Stage 5AA prime-minus-one CUDA synthetic commands.", no_args_is_help=True)


@app.command("build-kernel-implementation-records")
def build_kernel_command(
    kernel_implementation_out: Path = typer.Option(KERNEL_IMPLEMENTATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_kernel_implementation_records(kernel_implementation_out=kernel_implementation_out, out_dir=out_dir)
    console.print(f"kernel_implementation_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-run-records")
def build_run_command(
    cuda_run_out: Path = typer.Option(CUDA_RUN_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_run_records(cuda_run_out=cuda_run_out, out_dir=out_dir)
    console.print(f"cuda_run_records={len(records)}")
    console.print(f"cuda_run_status={records[0]['cuda_run_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("run-synthetic-cuda-parity")
def run_synthetic_cuda_parity_command(
    cuda_run_out: Path = typer.Option(CUDA_RUN_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    build_dir: Path = typer.Option(Path("build/stage5aa-prime-minus-one-cuda-synthetic")),
    skip_cuda: bool = typer.Option(False),
    require_cuda: bool = typer.Option(False),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = run_synthetic_cuda_parity(
        cuda_run_out=cuda_run_out,
        out_dir=out_dir,
        build_dir=build_dir,
        skip_cuda=skip_cuda,
        require_cuda=require_cuda,
    )
    record = records[0]
    console.print(f"cuda_run_records={len(records)}")
    console.print(f"cuda_run_status={record['cuda_run_status']}")
    console.print(f"cuda_pass_count={record['cuda_pass_count']}")
    console.print(f"cuda_fail_count={record['cuda_fail_count']}")
    console.print(f"cuda_skip_count={record['cuda_skip_count']}")
    console.print(f"computed_output_token_hash={record.get('computed_output_token_hash') or ''}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-parity-records")
def build_parity_command(
    cuda_run: Path = typer.Option(CUDA_RUN_PATH),
    parity_out: Path = typer.Option(PARITY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_parity_records(cuda_run=cuda_run, parity_out=parity_out, out_dir=out_dir)
    console.print(f"parity_records={len(records)}")
    console.print(f"parity_status={records[0]['parity_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-device-subset-audit")
def build_device_subset_command(
    device_subset_audit_out: Path = typer.Option(DEVICE_SUBSET_AUDIT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_device_subset_audit(device_subset_audit_out=device_subset_audit_out, out_dir=out_dir)
    console.print(f"device_subset_audit_records={len(records)}")
    console.print(f"forbidden_finding_count={records[0]['forbidden_finding_count']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-result-store-preflight")
def build_result_store_command(
    result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_result_store_preflight(result_store_preflight_out=result_store_preflight_out, out_dir=out_dir)
    console.print(f"result_store_preflight_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-p56-blocker")
def build_p56_blocker_command(
    p56_blocker_out: Path = typer.Option(P56_BLOCKER_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_p56_blocker(p56_blocker_out=p56_blocker_out, out_dir=out_dir)
    console.print(f"p56_blocker_records={len(records)}")
    console.print(f"full_p56_cuda_blocked={str(any(record['blocker_status'] == 'blocked_full_p56_token_buffer_missing' for record in records)).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-scored-experiment-deferral")
def build_scored_deferral_command(
    scored_experiment_deferral_out: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_scored_experiment_deferral(scored_experiment_deferral_out=scored_experiment_deferral_out, out_dir=out_dir)
    console.print(f"scored_experiment_deferral_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_next_stage_command(
    parity: Path = typer.Option(PARITY_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_next_stage_decision(parity=parity, next_stage_decision_out=next_stage_decision_out, out_dir=out_dir)
    selected = next(record for record in records if record.get("selected") is True)
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-summary")
def build_summary_command(
    kernel_implementation: Path = typer.Option(KERNEL_IMPLEMENTATION_PATH),
    cuda_run: Path = typer.Option(CUDA_RUN_PATH),
    parity: Path = typer.Option(PARITY_PATH),
    device_subset_audit: Path = typer.Option(DEVICE_SUBSET_AUDIT_PATH),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    p56_blocker: Path = typer.Option(P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    summary = build_summary(
        kernel_implementation=kernel_implementation,
        cuda_run=cuda_run,
        parity=parity,
        device_subset_audit=device_subset_audit,
        result_store_preflight=result_store_preflight,
        p56_blocker=p56_blocker,
        scored_experiment_deferral=scored_experiment_deferral,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"parity_status={summary['parity_status']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5aa")
def validate_stage5aa(
    kernel_implementation: Path = typer.Option(KERNEL_IMPLEMENTATION_PATH),
    cuda_run: Path = typer.Option(CUDA_RUN_PATH),
    parity: Path = typer.Option(PARITY_PATH),
    device_subset_audit: Path = typer.Option(DEVICE_SUBSET_AUDIT_PATH),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    p56_blocker: Path = typer.Option(P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5aa_results(
        kernel_implementation_path=kernel_implementation,
        cuda_run_path=cuda_run,
        parity_path=parity,
        device_subset_audit_path=device_subset_audit,
        result_store_preflight_path=result_store_preflight,
        p56_blocker_path=p56_blocker,
        scored_experiment_deferral_path=scored_experiment_deferral,
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
    console.print("prime_minus_one_cuda_synthetic_stage5aa_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from libreprimus.prime_minus_one_cuda_synthetic.export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "parity_status",
        "cuda_attempted",
        "cuda_pass_count",
        "cuda_fail_count",
        "cuda_skip_count",
        "computed_output_token_hash",
        "p56_cuda_blocked",
        "full_p56_cuda_blocked",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="prime-minus-one-cuda-synthetic")


__all__ = ["register"]
