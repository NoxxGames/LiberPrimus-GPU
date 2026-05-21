"""Stage 5L solved-fixture-safe Gematria mapping CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_solved_fixture_mapping.models import (
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    OUTPUT_HASH_CONTRACT_PATH,
    SCORE_SUMMARY_SHAPE_PATH,
    STAGE4O_SOLVED_FIXTURE_MANIFEST,
    STAGE5K_PREFLIGHT_PATH,
    SUMMARY_PATH,
    TOKEN_MAPPING_PATH,
)
from libreprimus.gematria_solved_fixture_mapping.native_parity import build_native_parity_records
from libreprimus.gematria_solved_fixture_mapping.output_hash_contract import (
    build_output_hash_contract_records,
)
from libreprimus.gematria_solved_fixture_mapping.score_summary_shape import (
    build_score_summary_shape_records,
)
from libreprimus.gematria_solved_fixture_mapping.summary import build_summary, load_summary
from libreprimus.gematria_solved_fixture_mapping.token_mapping import build_token_mapping_records
from libreprimus.gematria_solved_fixture_mapping.validation import validate_stage5l_results
from libreprimus.paths import repo_root

gematria_solved_fixture_mapping_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_solved_fixture_mapping_app.command("build-token-mapping")
def build_token_mapping_command(
    manifest: Path = typer.Option(
        STAGE4O_SOLVED_FIXTURE_MANIFEST,
        "--manifest",
        help="Stage 4O solved-fixture-safe CPU batch manifest.",
    ),
    preflight: Path = typer.Option(
        STAGE5K_PREFLIGHT_PATH,
        "--preflight",
        help="Stage 5K solved-fixture-safe preflight records.",
    ),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5L output directory."),
    token_mapping_out: Path = typer.Option(
        TOKEN_MAPPING_PATH,
        "--token-mapping-out",
        help="Committed Stage 5L token mapping YAML.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build source-backed solved-fixture Gematria token mappings."""

    _require_file(manifest)
    _require_file(preflight)
    records = build_token_mapping_records(
        source_manifest=_resolve(manifest),
        preflight=_resolve(preflight),
        token_mapping_out=_resolve(token_mapping_out),
        out_dir=_resolve(out_dir),
    )
    mapped = sum(1 for record in records if record["mapping_status"] == "mapped")
    console.print(f"token_mapping_records={len(records)}")
    console.print(f"mapped_count={mapped}")
    console.print(f"blocked_count={len(records) - mapped}")
    if not allow_warnings:
        return


@gematria_solved_fixture_mapping_app.command("build-native-parity")
def build_native_parity_command(
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping", help="Stage 5L token mappings."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5L output directory."),
    native_parity_out: Path = typer.Option(
        NATIVE_PARITY_PATH,
        "--native-parity-out",
        help="Committed Stage 5L native parity YAML.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build native output-token hash records without CUDA execution."""

    _require_file(token_mapping)
    records = build_native_parity_records(
        token_mapping=_resolve(token_mapping),
        native_parity_out=_resolve(native_parity_out),
        out_dir=_resolve(out_dir),
    )
    prepared = sum(1 for record in records if record["native_parity_status"] == "prepared")
    console.print(f"native_parity_fixture_records={len(records)}")
    console.print(f"native_parity_prepared_count={prepared}")
    if not allow_warnings:
        return


@gematria_solved_fixture_mapping_app.command("build-output-hash-contract")
def build_output_hash_contract_command(
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity", help="Stage 5L native parity records."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5L output directory."),
    output_hash_contract_out: Path = typer.Option(
        OUTPUT_HASH_CONTRACT_PATH,
        "--output-hash-contract-out",
        help="Committed Stage 5L output hash contract YAML.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the solved-fixture output hash contract."""

    _require_file(native_parity)
    records = build_output_hash_contract_records(
        native_parity=_resolve(native_parity),
        output_hash_contract_out=_resolve(output_hash_contract_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"output_hash_contract_records={len(records)}")
    console.print(f"hash_algorithm={records[0]['hash_algorithm']}")
    if not allow_warnings:
        return


@gematria_solved_fixture_mapping_app.command("build-score-summary-shape")
def build_score_summary_shape_command(
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5L output directory."),
    score_summary_shape_out: Path = typer.Option(
        SCORE_SUMMARY_SHAPE_PATH,
        "--score-summary-shape-out",
        help="Committed Stage 5L score-summary shape YAML.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 4I-compatible score-summary shape records."""

    records = build_score_summary_shape_records(
        score_summary_shape_out=_resolve(score_summary_shape_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"score_summary_shape_records={len(records)}")
    console.print(f"score_summary_contract={records[0]['score_summary_contract']}")
    if not allow_warnings:
        return


@gematria_solved_fixture_mapping_app.command("build-summary")
def build_summary_command(
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping", help="Stage 5L token mappings."),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity", help="Stage 5L native parity records."),
    output_hash_contract: Path = typer.Option(
        OUTPUT_HASH_CONTRACT_PATH,
        "--output-hash-contract",
        help="Stage 5L output hash contract records.",
    ),
    score_summary_shape: Path = typer.Option(
        SCORE_SUMMARY_SHAPE_PATH,
        "--score-summary-shape",
        help="Stage 5L score-summary shape records.",
    ),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5L summary YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5L output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5L aggregate summary."""

    for path in (token_mapping, native_parity, output_hash_contract, score_summary_shape):
        _require_file(path)
    summary = build_summary(
        token_mapping=_resolve(token_mapping),
        native_parity=_resolve(native_parity),
        output_hash_contract=_resolve(output_hash_contract),
        score_summary_shape=_resolve(score_summary_shape),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "token_mapping_records",
        "mapped_count",
        "native_parity_prepared_count",
        "blocker_count_after",
        "selected_next_stage",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@gematria_solved_fixture_mapping_app.command("validate-stage5l")
def validate_stage5l_command(
    token_mapping: Path = typer.Option(TOKEN_MAPPING_PATH, "--token-mapping", help="Stage 5L token mappings."),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH, "--native-parity", help="Stage 5L native parity records."),
    output_hash_contract: Path = typer.Option(
        OUTPUT_HASH_CONTRACT_PATH,
        "--output-hash-contract",
        help="Stage 5L output hash contract records.",
    ),
    score_summary_shape: Path = typer.Option(
        SCORE_SUMMARY_SHAPE_PATH,
        "--score-summary-shape",
        help="Stage 5L score-summary shape records.",
    ),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Stage 5L summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5L output directory."),
) -> None:
    """Validate Stage 5L records and generated summary."""

    try:
        counts, errors = validate_stage5l_results(
            token_mapping_path=_resolve(token_mapping),
            native_parity_path=_resolve(native_parity),
            output_hash_contract_path=_resolve(output_hash_contract),
            score_summary_shape_path=_resolve(score_summary_shape),
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
    console.print("gematria_solved_fixture_mapping_stage5l_valid=true")


@gematria_solved_fixture_mapping_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Stage 5L summary YAML.")) -> None:
    """Print the committed Stage 5L summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "token_mapping_records",
        "mapped_count",
        "blocked_count",
        "native_parity_fixture_records",
        "native_parity_prepared_count",
        "output_hash_contract_records",
        "score_summary_shape_records",
        "blocker_count_before",
        "blocker_count_after",
        "blockers_resolved",
        "blockers_remaining",
        "readiness_status_counts",
        "selected_next_stage",
        "selected_next_stage_reason",
        "solved_fixture_cuda_execution_allowed",
        "cuda_execution_performed",
        "new_cuda_kernels_added",
        "cuda_source_modified",
        "real_liber_primus_cuda_data_used",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_solved_fixture_mapping_app, name="gematria-solved-fixture-mapping")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
