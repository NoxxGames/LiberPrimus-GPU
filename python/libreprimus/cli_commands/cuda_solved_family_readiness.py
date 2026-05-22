"""Stage 5T CUDA solved-family readiness CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_solved_family_readiness.batch_abi_gaps import build_batch_abi_gaps
from libreprimus.cuda_solved_family_readiness.benchmark_readiness import build_benchmark_readiness
from libreprimus.cuda_solved_family_readiness.kernel_readiness import build_kernel_readiness
from libreprimus.cuda_solved_family_readiness.models import (
    BATCH_ABI_GAPS_PATH,
    BENCHMARK_READINESS_PATH,
    FIXTURE_ROOT,
    INVENTORY_PATH,
    KERNEL_READINESS_PATH,
    NEXT_STAGE_DECISION_PATH,
    NO_UNSOLVED_GUARDRAIL_PATH,
    OUTPUT_DIR,
    PARITY_MATRIX_PATH,
    STAGE5M_SUMMARY,
    STAGE5R_SUMMARY,
    STAGE5S_SUMMARY,
    SUMMARY_PATH,
)
from libreprimus.cuda_solved_family_readiness.next_stage_decision import build_next_stage_decision
from libreprimus.cuda_solved_family_readiness.no_unsolved_guardrail import build_no_unsolved_guardrail
from libreprimus.cuda_solved_family_readiness.parity_matrix import build_parity_matrix
from libreprimus.cuda_solved_family_readiness.solved_family_inventory import build_solved_family_inventory
from libreprimus.cuda_solved_family_readiness.summary import build_summary, load_summary
from libreprimus.cuda_solved_family_readiness.validation import validate_stage5t_results
from libreprimus.paths import repo_root

cuda_solved_family_readiness_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_solved_family_readiness_app.command("build-solved-family-inventory")
def build_solved_family_inventory_command(
    fixture_root: Path = typer.Option(FIXTURE_ROOT, "--fixture-root"),
    solved_family_inventory_out: Path = typer.Option(INVENTORY_PATH, "--solved-family-inventory-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build solved-family inventory records."""

    _require_dir(fixture_root)
    records = build_solved_family_inventory(
        fixture_root=_resolve(fixture_root),
        inventory_out=_resolve(solved_family_inventory_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"solved_family_inventory_records={len(records)}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("build-parity-matrix")
def build_parity_matrix_command(
    solved_family_inventory: Path = typer.Option(INVENTORY_PATH, "--solved-family-inventory"),
    stage5m_summary: Path = typer.Option(STAGE5M_SUMMARY, "--stage5m-summary"),
    stage5r_summary: Path = typer.Option(STAGE5R_SUMMARY, "--stage5r-summary"),
    parity_matrix_out: Path = typer.Option(PARITY_MATRIX_PATH, "--parity-matrix-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build CUDA parity/readiness matrix records."""

    for path in (solved_family_inventory, stage5m_summary, stage5r_summary):
        _require_file(path)
    records = build_parity_matrix(
        inventory=_resolve(solved_family_inventory),
        stage5m_summary=_resolve(stage5m_summary),
        stage5r_summary=_resolve(stage5r_summary),
        parity_matrix_out=_resolve(parity_matrix_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"cuda_parity_matrix_records={len(records)}")
    console.print(f"verified_current_kernel_parity_count={sum(1 for record in records if record['readiness_status'] == 'cuda_parity_verified_existing_kernel')}")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("build-kernel-readiness")
def build_kernel_readiness_command(
    parity_matrix: Path = typer.Option(PARITY_MATRIX_PATH, "--parity-matrix"),
    kernel_readiness_out: Path = typer.Option(KERNEL_READINESS_PATH, "--kernel-readiness-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build kernel-readiness ranking records."""

    _require_file(parity_matrix)
    records = build_kernel_readiness(
        parity_matrix=_resolve(parity_matrix),
        kernel_readiness_out=_resolve(kernel_readiness_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"kernel_readiness_records={len(records)}")
    console.print("implementation_allowed_now=false")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("build-batch-abi-gaps")
def build_batch_abi_gaps_command(
    batch_abi_gaps_out: Path = typer.Option(BATCH_ABI_GAPS_PATH, "--batch-abi-gaps-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build candidate batch ABI gap records."""

    records = build_batch_abi_gaps(batch_abi_gaps_out=_resolve(batch_abi_gaps_out), out_dir=_resolve(out_dir))
    console.print(f"batch_abi_gap_records={len(records)}")
    console.print(f"needs_batch_abi_count={sum(1 for record in records if record['blocking'])}")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("build-benchmark-readiness")
def build_benchmark_readiness_command(
    benchmark_readiness_out: Path = typer.Option(BENCHMARK_READINESS_PATH, "--benchmark-readiness-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build benchmark planning-only readiness records."""

    records = build_benchmark_readiness(benchmark_readiness_out=_resolve(benchmark_readiness_out), out_dir=_resolve(out_dir))
    console.print(f"benchmark_readiness_records={len(records)}")
    console.print("benchmark_execution_allowed=false")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("build-no-unsolved-guardrail")
def build_no_unsolved_guardrail_command(
    no_unsolved_guardrail_out: Path = typer.Option(NO_UNSOLVED_GUARDRAIL_PATH, "--no-unsolved-guardrail-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build no-unsolved guardrail review records."""

    records = build_no_unsolved_guardrail(
        no_unsolved_guardrail_out=_resolve(no_unsolved_guardrail_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"no_unsolved_guardrail_records={len(records)}")
    console.print("unsolved_page_cuda_allowed=false")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("build-next-stage-decision")
def build_next_stage_decision_command(
    batch_abi_gaps: Path = typer.Option(BATCH_ABI_GAPS_PATH, "--batch-abi-gaps"),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build controlled next-stage decision records."""

    _require_file(batch_abi_gaps)
    records = build_next_stage_decision(
        batch_abi_gaps=_resolve(batch_abi_gaps),
        next_stage_decision_out=_resolve(next_stage_decision_out),
        out_dir=_resolve(out_dir),
    )
    selected = next(record for record in records if record["selected"])
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("build-summary")
def build_summary_command(
    solved_family_inventory: Path = typer.Option(INVENTORY_PATH, "--solved-family-inventory"),
    parity_matrix: Path = typer.Option(PARITY_MATRIX_PATH, "--parity-matrix"),
    kernel_readiness: Path = typer.Option(KERNEL_READINESS_PATH, "--kernel-readiness"),
    batch_abi_gaps: Path = typer.Option(BATCH_ABI_GAPS_PATH, "--batch-abi-gaps"),
    benchmark_readiness: Path = typer.Option(BENCHMARK_READINESS_PATH, "--benchmark-readiness"),
    no_unsolved_guardrail: Path = typer.Option(NO_UNSOLVED_GUARDRAIL_PATH, "--no-unsolved-guardrail"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    stage5s_summary: Path = typer.Option(STAGE5S_SUMMARY, "--stage5s-summary"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5T aggregate summary."""

    for path in (
        solved_family_inventory,
        parity_matrix,
        kernel_readiness,
        batch_abi_gaps,
        benchmark_readiness,
        no_unsolved_guardrail,
        next_stage_decision,
        stage5s_summary,
    ):
        _require_file(path)
    payload = build_summary(
        solved_family_inventory=_resolve(solved_family_inventory),
        parity_matrix=_resolve(parity_matrix),
        kernel_readiness=_resolve(kernel_readiness),
        batch_abi_gaps=_resolve(batch_abi_gaps),
        benchmark_readiness=_resolve(benchmark_readiness),
        no_unsolved_guardrail=_resolve(no_unsolved_guardrail),
        next_stage_decision=_resolve(next_stage_decision),
        stage5s_summary=_resolve(stage5s_summary),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in ("solved_family_inventory_records", "cuda_parity_matrix_records", "kernel_readiness_records", "recommended_next_stage_title"):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@cuda_solved_family_readiness_app.command("validate-stage5t")
def validate_stage5t_command(
    solved_family_inventory: Path = typer.Option(INVENTORY_PATH, "--solved-family-inventory"),
    parity_matrix: Path = typer.Option(PARITY_MATRIX_PATH, "--parity-matrix"),
    kernel_readiness: Path = typer.Option(KERNEL_READINESS_PATH, "--kernel-readiness"),
    batch_abi_gaps: Path = typer.Option(BATCH_ABI_GAPS_PATH, "--batch-abi-gaps"),
    benchmark_readiness: Path = typer.Option(BENCHMARK_READINESS_PATH, "--benchmark-readiness"),
    no_unsolved_guardrail: Path = typer.Option(NO_UNSOLVED_GUARDRAIL_PATH, "--no-unsolved-guardrail"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    """Validate Stage 5T committed records and ignored reports."""

    try:
        counts, errors = validate_stage5t_results(
            solved_family_inventory_path=_resolve(solved_family_inventory),
            parity_matrix_path=_resolve(parity_matrix),
            kernel_readiness_path=_resolve(kernel_readiness),
            batch_abi_gaps_path=_resolve(batch_abi_gaps),
            benchmark_readiness_path=_resolve(benchmark_readiness),
            no_unsolved_guardrail_path=_resolve(no_unsolved_guardrail),
            next_stage_decision_path=_resolve(next_stage_decision),
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
    console.print("cuda_solved_family_readiness_stage5t_valid=true")


@cuda_solved_family_readiness_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    """Print Stage 5T summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "solved_family_inventory_records",
        "cuda_parity_matrix_records",
        "kernel_readiness_records",
        "batch_abi_gap_records",
        "benchmark_readiness_records",
        "no_unsolved_guardrail_records",
        "next_stage_decision_records",
        "verified_existing_cuda_parity_count",
        "ready_for_contract_review_count",
        "needs_batch_abi_count",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload[key]}")


def register(root_app: typer.Typer) -> None:
    """Register the Stage 5T command group."""

    root_app.add_typer(cuda_solved_family_readiness_app, name="cuda-solved-family-readiness")


def _resolve(path: Path) -> Path:
    if path.is_absolute():
        return path
    return repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]missing_file={path}[/red]")
        raise typer.Exit(1)


def _require_dir(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_dir():
        console.print(f"[red]missing_dir={path}[/red]")
        raise typer.Exit(1)
