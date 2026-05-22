"""Typer commands for Stage 5Z prime-minus-one CUDA contract preparation."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.prime_minus_one_cuda_contract.buffer_contract import build_buffer_contract
from libreprimus.prime_minus_one_cuda_contract.contract_records import build_contract_records
from libreprimus.prime_minus_one_cuda_contract.full_p56_blocker import build_full_p56_blocker
from libreprimus.prime_minus_one_cuda_contract.future_parity_plan import build_future_parity_plan
from libreprimus.prime_minus_one_cuda_contract.host_runner_contract import build_host_runner_contract
from libreprimus.prime_minus_one_cuda_contract.implementation_readiness import build_implementation_readiness_gate
from libreprimus.prime_minus_one_cuda_contract.kernel_abi import build_kernel_abi
from libreprimus.prime_minus_one_cuda_contract.models import (
    BUFFER_CONTRACT_PATH,
    CUDA_CONTRACT_PATH,
    FULL_P56_BLOCKER_PATH,
    FUTURE_PARITY_PLAN_PATH,
    HOST_RUNNER_CONTRACT_PATH,
    IMPLEMENTATION_READINESS_PATH,
    KERNEL_ABI_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESULT_STORE_COMPATIBILITY_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SUMMARY_PATH,
    VALIDATION_VECTORS_PATH,
)
from libreprimus.prime_minus_one_cuda_contract.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_cuda_contract.result_store_compatibility import build_result_store_compatibility
from libreprimus.prime_minus_one_cuda_contract.scored_experiment_deferral import build_scored_experiment_deferral
from libreprimus.prime_minus_one_cuda_contract.summary import build_summary
from libreprimus.prime_minus_one_cuda_contract.validation import validate_stage5z_results
from libreprimus.prime_minus_one_cuda_contract.validation_vectors import build_validation_vectors

console = Console()
app = typer.Typer(help="Stage 5Z prime-minus-one CUDA contract preparation commands.", no_args_is_help=True)


@app.command("build-contract-records")
def build_contract_records_command(
    cuda_contract_out: Path = typer.Option(CUDA_CONTRACT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_contract_records(cuda_contract_out=cuda_contract_out, out_dir=out_dir)
    console.print(f"cuda_contract_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-kernel-abi")
def build_kernel_abi_command(
    kernel_abi_out: Path = typer.Option(KERNEL_ABI_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_kernel_abi(kernel_abi_out=kernel_abi_out, out_dir=out_dir)
    console.print(f"kernel_abi_records={len(records)}")
    console.print(f"cuda_kernel_implemented={str(records[0]['cuda_kernel_implemented']).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-host-runner-contract")
def build_host_runner_contract_command(
    host_runner_contract_out: Path = typer.Option(HOST_RUNNER_CONTRACT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_host_runner_contract(host_runner_contract_out=host_runner_contract_out, out_dir=out_dir)
    console.print(f"host_runner_contract_records={len(records)}")
    console.print(f"host_runner_implemented={str(records[0]['host_runner_implemented']).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-buffer-contract")
def build_buffer_contract_command(
    buffer_contract_out: Path = typer.Option(BUFFER_CONTRACT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_buffer_contract(buffer_contract_out=buffer_contract_out, out_dir=out_dir)
    console.print(f"buffer_contract_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-validation-vectors")
def build_validation_vectors_command(
    validation_vectors_out: Path = typer.Option(VALIDATION_VECTORS_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_validation_vectors(validation_vectors_out=validation_vectors_out, out_dir=out_dir)
    console.print(f"validation_vector_records={len(records)}")
    console.print(f"full_p56_blocked={str(any(record['validation_vector_kind'] == 'full_p56_blocker' and str(record['validation_status']).startswith('blocked') for record in records)).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-future-parity-plan")
def build_future_parity_plan_command(
    future_parity_plan_out: Path = typer.Option(FUTURE_PARITY_PLAN_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_future_parity_plan(future_parity_plan_out=future_parity_plan_out, out_dir=out_dir)
    console.print(f"future_parity_plan_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-result-store-compatibility")
def build_result_store_compatibility_command(
    result_store_compatibility_out: Path = typer.Option(RESULT_STORE_COMPATIBILITY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_result_store_compatibility(result_store_compatibility_out=result_store_compatibility_out, out_dir=out_dir)
    console.print(f"result_store_compatibility_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-full-p56-blocker")
def build_full_p56_blocker_command(
    full_p56_blocker_out: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_full_p56_blocker(full_p56_blocker_out=full_p56_blocker_out, out_dir=out_dir)
    console.print(f"full_p56_blocker_records={len(records)}")
    console.print(f"full_p56_status={records[0]['full_p56_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-scored-experiment-deferral")
def build_scored_experiment_deferral_command(
    scored_experiment_deferral_out: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_scored_experiment_deferral(scored_experiment_deferral_out=scored_experiment_deferral_out, out_dir=out_dir)
    console.print(f"scored_experiment_deferral_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-implementation-readiness-gate")
def build_implementation_readiness_gate_command(
    implementation_readiness_out: Path = typer.Option(IMPLEMENTATION_READINESS_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_implementation_readiness_gate(implementation_readiness_out=implementation_readiness_out, out_dir=out_dir)
    console.print(f"implementation_readiness_gate_records={len(records)}")
    console.print(f"future_synthetic_kernel_implementation_ready={str(records[0]['future_synthetic_kernel_implementation_ready']).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_next_stage_decision_command(
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_next_stage_decision(next_stage_decision_out=next_stage_decision_out, out_dir=out_dir)
    selected = next(record for record in records if record.get("selected") is True)
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-summary")
def build_summary_command(
    cuda_contract: Path = typer.Option(CUDA_CONTRACT_PATH),
    kernel_abi: Path = typer.Option(KERNEL_ABI_PATH),
    host_runner_contract: Path = typer.Option(HOST_RUNNER_CONTRACT_PATH),
    buffer_contract: Path = typer.Option(BUFFER_CONTRACT_PATH),
    validation_vectors: Path = typer.Option(VALIDATION_VECTORS_PATH),
    future_parity_plan: Path = typer.Option(FUTURE_PARITY_PLAN_PATH),
    result_store_compatibility: Path = typer.Option(RESULT_STORE_COMPATIBILITY_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    implementation_readiness_gate: Path = typer.Option(IMPLEMENTATION_READINESS_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    summary = build_summary(
        cuda_contract=cuda_contract,
        kernel_abi=kernel_abi,
        host_runner_contract=host_runner_contract,
        buffer_contract=buffer_contract,
        validation_vectors=validation_vectors,
        future_parity_plan=future_parity_plan,
        result_store_compatibility=result_store_compatibility,
        full_p56_blocker=full_p56_blocker,
        scored_experiment_deferral=scored_experiment_deferral,
        implementation_readiness_gate=implementation_readiness_gate,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"cuda_contract_records={summary['cuda_contract_records']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5z")
def validate_stage5z(
    cuda_contract: Path = typer.Option(CUDA_CONTRACT_PATH),
    kernel_abi: Path = typer.Option(KERNEL_ABI_PATH),
    host_runner_contract: Path = typer.Option(HOST_RUNNER_CONTRACT_PATH),
    buffer_contract: Path = typer.Option(BUFFER_CONTRACT_PATH),
    validation_vectors: Path = typer.Option(VALIDATION_VECTORS_PATH),
    future_parity_plan: Path = typer.Option(FUTURE_PARITY_PLAN_PATH),
    result_store_compatibility: Path = typer.Option(RESULT_STORE_COMPATIBILITY_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    implementation_readiness_gate: Path = typer.Option(IMPLEMENTATION_READINESS_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5z_results(
        cuda_contract_path=cuda_contract,
        kernel_abi_path=kernel_abi,
        host_runner_contract_path=host_runner_contract,
        buffer_contract_path=buffer_contract,
        validation_vectors_path=validation_vectors,
        future_parity_plan_path=future_parity_plan,
        result_store_compatibility_path=result_store_compatibility,
        full_p56_blocker_path=full_p56_blocker,
        scored_experiment_deferral_path=scored_experiment_deferral,
        implementation_readiness_gate_path=implementation_readiness_gate,
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
    console.print("prime_minus_one_cuda_contract_stage5z_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from libreprimus.prime_minus_one_cuda_contract.export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "cuda_contract_records",
        "kernel_abi_records",
        "host_runner_contract_records",
        "validation_vector_records",
        "implementation_readiness_status",
        "full_p56_blocker_status",
        "scored_experiment_deferral_status",
        "recommended_next_stage_title",
        "deep_research_recommended_next",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="prime-minus-one-cuda-contract")
