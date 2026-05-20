"""Stage 5E CUDA kernel contract CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_kernel_contract.models import (
    ADAPTER_SELECTION_PATH,
    CONTRACT_PATH,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    READINESS_PATH,
    SUMMARY_PATH,
)
from libreprimus.cuda_kernel_contract.native_parity_mapping import build_native_parity_adapter_map
from libreprimus.cuda_kernel_contract.readiness import build_implementation_readiness
from libreprimus.cuda_kernel_contract.selection import select_first_kernel_contract
from libreprimus.cuda_kernel_contract.summary import build_summary, load_summary
from libreprimus.cuda_kernel_contract.validation import validate_stage5e_results
from libreprimus.paths import repo_root

cuda_kernel_contract_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_kernel_contract_app.command("select-first-kernel")
def cuda_kernel_contract_select_first_kernel(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5E first-kernel contract manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5E output directory."),
    contract_out: Path = typer.Option(CONTRACT_PATH, "--contract-out", help="Committed first-kernel contract YAML."),
    adapter_selection_out: Path = typer.Option(ADAPTER_SELECTION_PATH, "--adapter-selection-out", help="Committed adapter-selection YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow alternate/rejected candidate warnings."),
) -> None:
    """Select the first future CUDA kernel contract without adding a kernel."""

    _require_file(manifest)
    contract, adapter = select_first_kernel_contract(
        out_dir=_resolve(out_dir),
        contract_out=_resolve(contract_out),
        adapter_selection_out=_resolve(adapter_selection_out),
    )
    selected = contract[0]
    console.print(f"selected_kernel_id={selected['selected_kernel_id']}")
    console.print(f"selected_target_id={selected['selected_target_id']}")
    console.print(f"selected_transform_family={selected['selected_transform_family']}")
    console.print(f"selected_adapter_family={adapter[0]['selected_adapter_family']}")
    console.print(f"alternate_candidate_count={len(selected.get('alternate_candidates', []))}")
    console.print(f"blocked_rejected_candidate_count={len(selected.get('blocked_or_rejected_candidates', []))}")
    console.print("cuda_kernel_added=0")
    console.print("cuda_transform_executed=0")
    if not allow_warnings and selected.get("blocked_or_rejected_candidates"):
        raise typer.Exit(1)


@cuda_kernel_contract_app.command("build-native-parity-map")
def cuda_kernel_contract_build_native_parity_map(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5E adapter-selection manifest."),
    contract: Path = typer.Option(CONTRACT_PATH, "--contract", help="Committed first-kernel contract YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5E output directory."),
    native_parity_out: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity-out", help="Committed native parity adapter map YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for symmetry with other stage commands."),
) -> None:
    """Map the Stage 5D native parity surface onto the selected contract."""

    _require_file(manifest)
    _require_file(contract)
    records = build_native_parity_adapter_map(
        contract_path=_resolve(contract),
        out_dir=_resolve(out_dir),
        native_parity_out=_resolve(native_parity_out),
    )
    record = records[0]
    console.print(f"native_parity_mapped={str(record['native_parity_mapped']).lower()}")
    console.print(f"one_thread_hash={record['stage5d_one_thread_hash']}")
    console.print(f"multi_thread_hash={record['stage5d_multi_thread_hash']}")
    console.print(f"python_native_parity={str(record['stage5d_python_native_parity']).lower()}")
    console.print(f"thread_counts={','.join(str(item) for item in record['stage5d_thread_counts'])}")
    if not allow_warnings:
        return


@cuda_kernel_contract_app.command("build-readiness")
def cuda_kernel_contract_build_readiness(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5E implementation-readiness manifest."),
    contract: Path = typer.Option(CONTRACT_PATH, "--contract", help="Committed first-kernel contract YAML."),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity", help="Committed native parity adapter map YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5E output directory."),
    readiness_out: Path = typer.Option(READINESS_PATH, "--readiness-out", help="Committed implementation-readiness YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow blocked readiness warnings."),
) -> None:
    """Build implementation-readiness metadata for Stage 5F only."""

    for path in (manifest, contract, native_parity):
        _require_file(path)
    records = build_implementation_readiness(
        contract_path=_resolve(contract),
        native_parity_path=_resolve(native_parity),
        out_dir=_resolve(out_dir),
        readiness_out=_resolve(readiness_out),
    )
    status = records[0]["readiness_status"]
    console.print(f"implementation_readiness_status={status}")
    console.print("cuda_kernel_added=0")
    console.print("gpu_benchmark_performed=0")
    if status.startswith("blocked") and not allow_warnings:
        raise typer.Exit(1)


@cuda_kernel_contract_app.command("build-summary")
def cuda_kernel_contract_build_summary(
    contract: Path = typer.Option(CONTRACT_PATH, "--contract", help="Committed first-kernel contract YAML."),
    adapter_selection: Path = typer.Option(ADAPTER_SELECTION_PATH, "--adapter-selection", help="Committed adapter-selection YAML."),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity", help="Committed native parity adapter map YAML."),
    readiness: Path = typer.Option(READINESS_PATH, "--readiness", help="Committed implementation-readiness YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5E output directory."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5E summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command consistency."),
) -> None:
    """Build the committed Stage 5E aggregate summary."""

    for path in (contract, adapter_selection, native_parity, readiness):
        _require_file(path)
    summary = build_summary(
        contract_path=_resolve(contract),
        adapter_selection_path=_resolve(adapter_selection),
        native_parity_path=_resolve(native_parity),
        readiness_path=_resolve(readiness),
        out_dir=_resolve(out_dir),
        summary_out=_resolve(summary_out),
    )
    for key in (
        "selected_kernel_id",
        "selected_transform_family",
        "selected_adapter_family",
        "alternate_candidate_count",
        "blocked_rejected_candidate_count",
        "native_parity_mapped",
        "implementation_readiness_status",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@cuda_kernel_contract_app.command("validate-stage5e")
def cuda_kernel_contract_validate_stage5e(
    contract: Path = typer.Option(CONTRACT_PATH, "--contract", help="Committed first-kernel contract YAML."),
    adapter_selection: Path = typer.Option(ADAPTER_SELECTION_PATH, "--adapter-selection", help="Committed adapter-selection YAML."),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity", help="Committed native parity adapter YAML."),
    readiness: Path = typer.Option(READINESS_PATH, "--readiness", help="Committed implementation-readiness YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5E summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5E output directory."),
) -> None:
    """Validate Stage 5E contract records and generated summary parity."""

    try:
        counts, errors = validate_stage5e_results(
            contract_path=_resolve(contract),
            adapter_selection_path=_resolve(adapter_selection),
            native_parity_path=_resolve(native_parity),
            readiness_path=_resolve(readiness),
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
    console.print("cuda_kernel_contract_stage5e_valid=true")


@cuda_kernel_contract_app.command("summary")
def cuda_kernel_contract_summary(
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5E summary YAML."),
) -> None:
    """Print the committed Stage 5E summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "selected_kernel_id",
        "selected_target_id",
        "selected_transform_family",
        "selected_adapter_family",
        "alternate_candidate_count",
        "blocked_rejected_candidate_count",
        "native_parity_mapped",
        "one_thread_hash",
        "multi_thread_hash",
        "python_native_parity",
        "implementation_readiness_status",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(cuda_kernel_contract_app, name="cuda-kernel-contract")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
