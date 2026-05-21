"""Stage 5Q Gematria expansion candidate mapping CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_expansion_candidate_mapping.candidate_inventory import build_candidate_inventory
from libreprimus.gematria_expansion_candidate_mapping.expansion_gate import build_expansion_gate_records
from libreprimus.gematria_expansion_candidate_mapping.models import (
    CANDIDATE_INVENTORY_PATH,
    EXPANSION_GATE_PATH,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    RESULT_STORE_PREFLIGHT_PATH,
    STAGE4I_CONFIDENCE_LABELS,
    STAGE4P_SUMMARY,
    STAGE5L_TOKEN_MAPPING,
    SUMMARY_PATH,
    TOKEN_MAPPING_PATH,
)
from libreprimus.gematria_expansion_candidate_mapping.native_parity import build_native_parity_records
from libreprimus.gematria_expansion_candidate_mapping.result_store_preflight import (
    build_result_store_preflight_records,
)
from libreprimus.gematria_expansion_candidate_mapping.summary import build_summary, load_summary
from libreprimus.gematria_expansion_candidate_mapping.token_mapping import build_token_mapping_records
from libreprimus.gematria_expansion_candidate_mapping.validation import validate_stage5q_results
from libreprimus.paths import repo_root

gematria_expansion_candidate_mapping_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_expansion_candidate_mapping_app.command("build-candidate-inventory")
def build_candidate_inventory_command(
    stage5l_token_mapping: Path = typer.Option(STAGE5L_TOKEN_MAPPING, "--stage5l-token-mapping"),
    candidate_inventory_out: Path = typer.Option(CANDIDATE_INVENTORY_PATH, "--candidate-inventory-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build source-backed Stage 5Q candidate inventory records."""

    _require_file(stage5l_token_mapping)
    records = build_candidate_inventory(
        stage5l_token_mapping=_resolve(stage5l_token_mapping),
        candidate_inventory_out=_resolve(candidate_inventory_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"candidate_inventory_records={len(records)}")
    console.print(f"new_candidate_count={sum(1 for item in records if item['candidate_status'] == 'candidate_for_mapping')}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@gematria_expansion_candidate_mapping_app.command("build-token-mapping")
def build_token_mapping_command(
    candidate_inventory: Path = typer.Option(CANDIDATE_INVENTORY_PATH, "--candidate-inventory"),
    token_mapping_out: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5Q token mappings without CUDA execution."""

    _require_file(candidate_inventory)
    records = build_token_mapping_records(
        candidate_inventory=_resolve(candidate_inventory),
        token_mapping_out=_resolve(token_mapping_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"token_mapping_records={len(records)}")
    console.print(f"mapped_count={sum(1 for item in records if item['mapping_status'] == 'mapped')}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@gematria_expansion_candidate_mapping_app.command("build-native-parity")
def build_native_parity_command(
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping"),
    native_parity_out: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5Q native expected output hashes without CUDA execution."""

    _require_file(token_mapping)
    records = build_native_parity_records(
        token_mapping=_resolve(token_mapping),
        native_parity_out=_resolve(native_parity_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"native_parity_records={len(records)}")
    console.print(f"native_parity_prepared_count={sum(1 for item in records if item['native_parity_status'] == 'prepared')}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@gematria_expansion_candidate_mapping_app.command("build-result-store-preflight")
def build_result_store_preflight_command(
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping"),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity"),
    stage4p_summary: Path = typer.Option(STAGE4P_SUMMARY, "--stage4p-summary"),
    confidence_labels: Path = typer.Option(STAGE4I_CONFIDENCE_LABELS, "--confidence-labels"),
    result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 4P/Stage 4I-compatible preflight metadata."""

    for path in (token_mapping, native_parity, stage4p_summary, confidence_labels):
        _require_file(path)
    records = build_result_store_preflight_records(
        token_mapping=_resolve(token_mapping),
        native_parity=_resolve(native_parity),
        stage4p_summary=_resolve(stage4p_summary),
        confidence_labels=_resolve(confidence_labels),
        result_store_preflight_out=_resolve(result_store_preflight_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"result_store_preflight_records={len(records)}")
    console.print("stage4p_compatibility=true")
    console.print("stage4i_compatibility=true")
    if not allow_warnings:
        return


@gematria_expansion_candidate_mapping_app.command("build-expansion-gate")
def build_expansion_gate_command(
    candidate_inventory: Path = typer.Option(CANDIDATE_INVENTORY_PATH, "--candidate-inventory"),
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping"),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    expansion_gate_out: Path = typer.Option(EXPANSION_GATE_PATH, "--expansion-gate-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build the controlled expansion gate for Stage 5R."""

    for path in (candidate_inventory, token_mapping, native_parity, result_store_preflight):
        _require_file(path)
    records = build_expansion_gate_records(
        candidate_inventory=_resolve(candidate_inventory),
        token_mapping=_resolve(token_mapping),
        native_parity=_resolve(native_parity),
        result_store_preflight=_resolve(result_store_preflight),
        expansion_gate_out=_resolve(expansion_gate_out),
        out_dir=_resolve(out_dir),
    )
    record = records[0]
    console.print(f"stage5r_ready={str(record['stage5r_ready']).lower()}")
    console.print(f"selected_next_stage={record['selected_next_stage']}")
    if not allow_warnings:
        return


@gematria_expansion_candidate_mapping_app.command("build-summary")
def build_summary_command(
    candidate_inventory: Path = typer.Option(CANDIDATE_INVENTORY_PATH, "--candidate-inventory"),
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping"),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    expansion_gate: Path = typer.Option(EXPANSION_GATE_PATH, "--expansion-gate"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build the Stage 5Q aggregate summary."""

    for path in (candidate_inventory, token_mapping, native_parity, result_store_preflight, expansion_gate):
        _require_file(path)
    payload = build_summary(
        candidate_inventory=_resolve(candidate_inventory),
        token_mapping=_resolve(token_mapping),
        native_parity=_resolve(native_parity),
        result_store_preflight=_resolve(result_store_preflight),
        expansion_gate=_resolve(expansion_gate),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in ("candidate_inventory_records", "new_candidate_count", "mapped_count", "stage5r_ready", "selected_next_stage"):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@gematria_expansion_candidate_mapping_app.command("validate-stage5q")
def validate_stage5q_command(
    candidate_inventory: Path = typer.Option(CANDIDATE_INVENTORY_PATH, "--candidate-inventory"),
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping"),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    expansion_gate: Path = typer.Option(EXPANSION_GATE_PATH, "--expansion-gate"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    """Validate Stage 5Q records and ignored generated summary."""

    try:
        counts, errors = validate_stage5q_results(
            candidate_inventory_path=_resolve(candidate_inventory),
            token_mapping_path=_resolve(token_mapping),
            native_parity_path=_resolve(native_parity),
            result_store_preflight_path=_resolve(result_store_preflight),
            expansion_gate_path=_resolve(expansion_gate),
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
    console.print("gematria_expansion_candidate_mapping_stage5q_valid=true")


@gematria_expansion_candidate_mapping_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    """Print the committed Stage 5Q summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "candidate_inventory_records",
        "new_candidate_count",
        "mapped_count",
        "blocked_mapping_count",
        "native_parity_prepared_count",
        "stage5l_5m_5o_duplicate_exclusion_status",
        "stage4p_compatibility",
        "stage4i_compatibility",
        "stage5r_ready",
        "selected_next_stage",
        "deep_research_recommended",
        "cuda_execution_performed",
        "cuda_source_modified",
        "new_cuda_kernels_added",
        "unsolved_page_cuda_used",
        "real_liber_primus_cuda_data_used",
        "gpu_benchmark_performed",
        "speedup_claim",
        "solve_claim",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_expansion_candidate_mapping_app, name="gematria-expansion-candidate-mapping")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
