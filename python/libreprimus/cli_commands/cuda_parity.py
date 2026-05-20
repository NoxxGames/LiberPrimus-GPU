"""Stage 5B CUDA parity harness CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_parity.backend_capability import build_backend_capability
from libreprimus.cuda_parity.future_kernel_matrix import build_future_kernel_matrix
from libreprimus.cuda_parity.harness_plan import build_harness_plan
from libreprimus.cuda_parity.models import (
    BACKEND_CAPABILITY_PATH,
    FUTURE_KERNEL_MATRIX_PATH,
    HARNESS_PLAN_PATH,
    PARITY_FIXTURES_PATH,
    STAGE4O_SUMMARY_PATH,
    STAGE4P_SUMMARY_PATH,
    STAGE4Q_READINESS_PATH,
    STAGE4Q_SUMMARY_PATH,
    STAGE5A_IMPLEMENTATION_GATES_PATH,
    STAGE5A_NON_TARGETS_PATH,
    STAGE5A_PARITY_SCAFFOLD_PATH,
    STAGE5A_SUMMARY_PATH,
    STAGE5A_TARGET_PLAN_PATH,
    STAGE5B_OUTPUT_DIR,
    SUMMARY_PATH,
)
from libreprimus.cuda_parity.summary import build_summary, load_summary
from libreprimus.cuda_parity.validation import validate_stage5b_results
from libreprimus.paths import repo_root

cuda_parity_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_parity_app.command("build-harness-plan")
def cuda_parity_build_harness_plan(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5B harness manifest."),
    target_plan: Path = typer.Option(STAGE5A_TARGET_PLAN_PATH, "--target-plan", help="Stage 5A target plan."),
    parity_scaffold: Path = typer.Option(STAGE5A_PARITY_SCAFFOLD_PATH, "--parity-scaffold", help="Stage 5A parity scaffold."),
    implementation_gates: Path = typer.Option(STAGE5A_IMPLEMENTATION_GATES_PATH, "--implementation-gates", help="Stage 5A implementation gates."),
    non_targets: Path = typer.Option(STAGE5A_NON_TARGETS_PATH, "--non-targets", help="Stage 5A non-target records."),
    stage5a_summary: Path = typer.Option(STAGE5A_SUMMARY_PATH, "--stage5a-summary", help="Stage 5A summary."),
    stage4q_readiness: Path = typer.Option(STAGE4Q_READINESS_PATH, "--stage4q-readiness", help="Stage 4Q readiness records."),
    stage4q_summary: Path = typer.Option(STAGE4Q_SUMMARY_PATH, "--stage4q-summary", help="Stage 4Q summary."),
    stage4o_summary: Path = typer.Option(STAGE4O_SUMMARY_PATH, "--stage4o-summary", help="Stage 4O summary."),
    stage4p_summary: Path = typer.Option(STAGE4P_SUMMARY_PATH, "--stage4p-summary", help="Stage 4P summary."),
    out_dir: Path = typer.Option(STAGE5B_OUTPUT_DIR, "--out-dir", help="Generated Stage 5B output directory."),
    harness_plan_out: Path = typer.Option(HARNESS_PLAN_PATH, "--harness-plan-out", help="Committed harness plan YAML."),
    parity_fixtures_out: Path = typer.Option(PARITY_FIXTURES_PATH, "--parity-fixtures-out", help="Committed fixture YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5B summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow blocked/skipped planning records."),
) -> None:
    """Build planning-only CUDA parity harness and fixture records."""

    for path in (
        manifest,
        target_plan,
        parity_scaffold,
        implementation_gates,
        non_targets,
        stage5a_summary,
        stage4q_readiness,
        stage4q_summary,
        stage4o_summary,
        stage4p_summary,
    ):
        _require_file(path)
    harness, fixtures = build_harness_plan(
        target_plan_path=_resolve(target_plan),
        parity_scaffold_path=_resolve(parity_scaffold),
        out_dir=_resolve(out_dir),
        harness_plan_out=_resolve(harness_plan_out),
        parity_fixtures_out=_resolve(parity_fixtures_out),
    )
    ready = sum(1 for record in harness if record["harness_status"] == "ready_for_future_kernel")
    skipped = sum(1 for record in harness if record["harness_status"] == "skipped_non_target")
    blocked = sum(1 for record in harness if record["harness_status"] == "blocked")
    console.print(f"harness_plan_records={len(harness)}")
    console.print(f"parity_fixture_records={len(fixtures)}")
    console.print(f"ready_for_future_kernel={ready}")
    console.print(f"blocked_harness_records={blocked}")
    console.print(f"skipped_non_targets={skipped}")
    console.print("cuda_kernel_added=false")
    console.print("gpu_benchmark_performed=false")
    if (blocked or skipped) and not allow_warnings:
        raise typer.Exit(1)


@cuda_parity_app.command("build-backend-capability")
def cuda_parity_build_backend_capability(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5B backend manifest."),
    out_dir: Path = typer.Option(STAGE5B_OUTPUT_DIR, "--out-dir", help="Generated Stage 5B output directory."),
    backend_capability_out: Path = typer.Option(BACKEND_CAPABILITY_PATH, "--backend-capability-out", help="Committed backend capability YAML."),
    local_gpu_model: str = typer.Option("NVIDIA RTX 4060 Ti", "--local-gpu-model", help="Optional local planning GPU model."),
    local_vram_gb: int = typer.Option(16, "--local-vram-gb", help="Optional local planning VRAM GB."),
    allow_missing_cuda: bool = typer.Option(False, "--allow-missing-cuda", help="Allow machines without CUDA hardware/toolkit."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow backend probe warnings."),
) -> None:
    """Record CUDA backend capabilities without requiring CUDA."""

    _require_file(manifest)
    records = build_backend_capability(
        out_dir=_resolve(out_dir),
        backend_capability_out=_resolve(backend_capability_out),
        local_gpu_model=local_gpu_model,
        local_vram_gb=local_vram_gb,
    )
    console.print(f"backend_capability_records={len(records)}")
    console.print(f"local_16gb_profile_recorded={str(any(record['vram_profile'] == 'local_16gb' for record in records)).lower()}")
    console.print("local_16gb_profile_required=false")
    console.print("cuda_hardware_required=false")
    if not allow_missing_cuda and not allow_warnings:
        missing = all(record["backend_status"] == "cuda_hardware_not_required" for record in records)
        if missing:
            raise typer.Exit(1)


@cuda_parity_app.command("build-future-kernel-matrix")
def cuda_parity_build_future_kernel_matrix(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5B future-kernel matrix manifest."),
    target_plan: Path = typer.Option(STAGE5A_TARGET_PLAN_PATH, "--target-plan", help="Stage 5A target plan."),
    harness_plan: Path = typer.Option(HARNESS_PLAN_PATH, "--harness-plan", help="Stage 5B harness plan."),
    parity_fixtures: Path = typer.Option(PARITY_FIXTURES_PATH, "--parity-fixtures", help="Stage 5B fixtures."),
    backend_capability: Path = typer.Option(BACKEND_CAPABILITY_PATH, "--backend-capability", help="Stage 5B backend capability."),
    out_dir: Path = typer.Option(STAGE5B_OUTPUT_DIR, "--out-dir", help="Generated Stage 5B output directory."),
    future_kernel_matrix_out: Path = typer.Option(FUTURE_KERNEL_MATRIX_PATH, "--future-kernel-matrix-out", help="Committed future-kernel matrix YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5B summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow blocked future kernel rows."),
) -> None:
    """Build future-kernel parity matrix rows and aggregate summary."""

    for path in (manifest, target_plan, harness_plan, parity_fixtures, backend_capability):
        _require_file(path)
    matrix = build_future_kernel_matrix(
        harness_plan_path=_resolve(harness_plan),
        parity_fixtures_path=_resolve(parity_fixtures),
        out_dir=_resolve(out_dir),
        future_kernel_matrix_out=_resolve(future_kernel_matrix_out),
    )
    summary = build_summary(
        harness_plan_path=_resolve(harness_plan),
        parity_fixtures_path=_resolve(parity_fixtures),
        backend_capability_path=_resolve(backend_capability),
        future_kernel_matrix_path=_resolve(future_kernel_matrix_out),
        target_plan_path=_resolve(target_plan),
        out_dir=_resolve(out_dir),
        summary_out=_resolve(summary_out),
    )
    blocked = sum(1 for record in matrix if record["future_kernel_status"] == "blocked")
    console.print(f"future_kernel_matrix_records={len(matrix)}")
    console.print(f"blocked_future_kernels={blocked}")
    console.print(f"ready_for_future_kernel={summary['ready_for_future_kernel']}")
    console.print("cuda_kernel_added=false")
    console.print("gpu_benchmark_performed=false")
    if blocked and not allow_warnings:
        raise typer.Exit(1)


@cuda_parity_app.command("validate-stage5b")
def cuda_parity_validate_stage5b(
    harness_plan: Path = typer.Option(HARNESS_PLAN_PATH, "--harness-plan", help="Stage 5B harness plan."),
    parity_fixtures: Path = typer.Option(PARITY_FIXTURES_PATH, "--parity-fixtures", help="Stage 5B fixtures."),
    backend_capability: Path = typer.Option(BACKEND_CAPABILITY_PATH, "--backend-capability", help="Stage 5B backend capability."),
    future_kernel_matrix: Path = typer.Option(FUTURE_KERNEL_MATRIX_PATH, "--future-kernel-matrix", help="Stage 5B future-kernel matrix."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Stage 5B summary."),
    results_dir: Path = typer.Option(STAGE5B_OUTPUT_DIR, "--results-dir", help="Generated Stage 5B output directory."),
) -> None:
    """Validate Stage 5B CUDA parity harness records."""

    try:
        counts, errors = validate_stage5b_results(
            harness_plan_path=_resolve(harness_plan),
            parity_fixtures_path=_resolve(parity_fixtures),
            backend_capability_path=_resolve(backend_capability),
            future_kernel_matrix_path=_resolve(future_kernel_matrix),
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
    console.print("cuda_parity_stage5b_valid=true")


@cuda_parity_app.command("summary")
def cuda_parity_summary(
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5B summary YAML."),
) -> None:
    """Print the committed Stage 5B summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "harness_plan_records",
        "parity_fixture_records",
        "backend_capability_records",
        "future_kernel_matrix_records",
        "ready_targets_loaded",
        "blocked_targets_loaded",
        "non_targets_loaded",
        "ready_for_future_kernel",
        "blocked_future_kernels",
        "skipped_non_targets",
        "stage4o_parity_references_used",
        "stage4p_unified_result_references_used",
    ):
        console.print(f"{key}={payload.get(key)}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]required file missing: {path}[/red]")
        raise typer.Exit(1)


def register(root_app: typer.Typer) -> None:
    """Register the Stage 5B CUDA parity command group."""

    root_app.add_typer(cuda_parity_app, name="cuda-parity")
