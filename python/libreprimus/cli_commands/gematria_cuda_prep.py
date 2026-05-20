"""Stage 5I Gematria CUDA preparation CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_cuda_prep.abi_plan import build_abi_plan_records
from libreprimus.gematria_cuda_prep.implementation_checklist import build_implementation_checklist_records
from libreprimus.gematria_cuda_prep.kernel_preparation import build_kernel_preparation_records
from libreprimus.gematria_cuda_prep.models import (
    ABI_PLAN_PATH,
    CHECKLIST_PATH,
    OUTPUT_DIR,
    PREPARATION_PATH,
    SUMMARY_PATH,
    VALIDATION_VECTORS_PATH,
)
from libreprimus.gematria_cuda_prep.summary import build_summary, load_summary
from libreprimus.gematria_cuda_prep.validation import validate_stage5i_results
from libreprimus.gematria_cuda_prep.validation_vectors import build_validation_vector_records
from libreprimus.paths import repo_root

gematria_cuda_prep_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_cuda_prep_app.command("build-kernel-preparation")
def gematria_cuda_build_kernel_preparation(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5I kernel-preparation manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5I output directory."),
    preparation_out: Path = typer.Option(PREPARATION_PATH, "--preparation-out", help="Committed preparation YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5I kernel-preparation records."""

    _require_file(manifest)
    records = build_kernel_preparation_records(preparation_out=_resolve(preparation_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"preparation_id={record['preparation_id']}")
    console.print(f"source_contract_id={record['source_contract_id']}")
    console.print(f"target_future_kernel_name={record['target_future_kernel_name']}")
    if not allow_warnings:
        return


@gematria_cuda_prep_app.command("build-abi-plan")
def gematria_cuda_build_abi_plan(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5I ABI plan manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5I output directory."),
    abi_plan_out: Path = typer.Option(ABI_PLAN_PATH, "--abi-plan-out", help="Committed ABI plan YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5I CUDA-C ABI plan records."""

    _require_file(manifest)
    records = build_abi_plan_records(abi_plan_out=_resolve(abi_plan_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"abi_plan_records={len(records)}")
    console.print(f"c_compatible_kernel_boundary={str(record['c_compatible_kernel_boundary']).lower()}")
    console.print(f"future_kernel_header_expected={record['future_kernel_header_expected']}")
    if not allow_warnings:
        return


@gematria_cuda_prep_app.command("build-validation-vectors")
def gematria_cuda_build_validation_vectors(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5I validation-vector manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5I output directory."),
    validation_vectors_out: Path = typer.Option(VALIDATION_VECTORS_PATH, "--validation-vectors-out", help="Committed validation vectors YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5I validation-vector records."""

    _require_file(manifest)
    records = build_validation_vector_records(
        validation_vectors_out=_resolve(validation_vectors_out),
        out_dir=_resolve(out_dir),
    )
    record = records[0]
    console.print(f"validation_vector_records={len(records)}")
    console.print(f"native_fixture_hash={record['expected_fixture_hash']}")
    console.print(f"stage5f_hash_is_gematria_fixture_hash={str(record['stage5f_hash_is_gematria_fixture_hash']).lower()}")
    if not allow_warnings:
        return


@gematria_cuda_prep_app.command("build-implementation-checklist")
def gematria_cuda_build_implementation_checklist(
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5I output directory."),
    implementation_checklist_out: Path = typer.Option(CHECKLIST_PATH, "--implementation-checklist-out", help="Committed checklist YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5J implementation checklist records."""

    records = build_implementation_checklist_records(
        checklist_out=_resolve(implementation_checklist_out),
        out_dir=_resolve(out_dir),
    )
    record = records[0]
    console.print(f"implementation_checklist_records={len(records)}")
    console.print(f"stage5j_ready_for_synthetic_implementation={str(record['stage5j_ready_for_synthetic_implementation']).lower()}")
    if not allow_warnings:
        return


@gematria_cuda_prep_app.command("build-summary")
def gematria_cuda_build_summary(
    preparation: Path = typer.Option(PREPARATION_PATH, "--preparation", help="Committed preparation YAML."),
    abi_plan: Path = typer.Option(ABI_PLAN_PATH, "--abi-plan", help="Committed ABI plan YAML."),
    validation_vectors: Path = typer.Option(VALIDATION_VECTORS_PATH, "--validation-vectors", help="Committed validation vectors YAML."),
    implementation_checklist: Path = typer.Option(CHECKLIST_PATH, "--implementation-checklist", help="Committed checklist YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5I summary YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5I output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5I aggregate summary."""

    for path in (preparation, abi_plan, validation_vectors, implementation_checklist):
        _require_file(path)
    summary = build_summary(
        preparation_path=_resolve(preparation),
        abi_plan_path=_resolve(abi_plan),
        validation_vectors_path=_resolve(validation_vectors),
        implementation_checklist_path=_resolve(implementation_checklist),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "preparation_id",
        "source_contract_id",
        "target_future_kernel_name",
        "token_domain",
        "native_fixture_hash",
        "stage5j_ready_for_synthetic_implementation",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@gematria_cuda_prep_app.command("validate-stage5i")
def gematria_cuda_validate_stage5i(
    preparation: Path = typer.Option(PREPARATION_PATH, "--preparation", help="Committed preparation YAML."),
    abi_plan: Path = typer.Option(ABI_PLAN_PATH, "--abi-plan", help="Committed ABI plan YAML."),
    validation_vectors: Path = typer.Option(VALIDATION_VECTORS_PATH, "--validation-vectors", help="Committed validation vectors YAML."),
    implementation_checklist: Path = typer.Option(CHECKLIST_PATH, "--implementation-checklist", help="Committed checklist YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5I summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5I output directory."),
) -> None:
    """Validate Stage 5I Gematria CUDA preparation records."""

    try:
        counts, errors = validate_stage5i_results(
            preparation_path=_resolve(preparation),
            abi_plan_path=_resolve(abi_plan),
            validation_vectors_path=_resolve(validation_vectors),
            implementation_checklist_path=_resolve(implementation_checklist),
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
    console.print("gematria_cuda_prep_stage5i_valid=true")


@gematria_cuda_prep_app.command("summary")
def gematria_cuda_summary(summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5I summary YAML.")) -> None:
    """Print the committed Stage 5I summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "preparation_id",
        "source_contract_id",
        "target_future_kernel_name",
        "token_domain",
        "arithmetic_direction",
        "separator_policy",
        "abi_plan_records",
        "validation_vector_records",
        "implementation_checklist_records",
        "native_fixture_hash",
        "stage5j_ready_for_synthetic_implementation",
        "next_stage",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_cuda_prep_app, name="gematria-cuda-prep")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
