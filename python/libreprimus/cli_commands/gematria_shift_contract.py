"""Stage 5H Gematria mod-29 shift contract CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_shift_contract.contract_records import build_contract_records
from libreprimus.gematria_shift_contract.models import (
    CONTRACT_PATH,
    FIXTURES_PATH,
    MAPPING_PATH,
    OUTPUT_DIR,
    SCORE_PLAN_PATH,
    STAGE4O_SOLVED_FIXTURE_MANIFEST,
    SUMMARY_PATH,
)
from libreprimus.gematria_shift_contract.native_fixture_records import build_native_fixture_records
from libreprimus.gematria_shift_contract.score_summary_parity_plan import build_score_summary_parity_plan_records
from libreprimus.gematria_shift_contract.solved_fixture_mapping import build_solved_fixture_mapping_records
from libreprimus.gematria_shift_contract.summary import build_summary, load_summary
from libreprimus.gematria_shift_contract.validation import validate_stage5h_results
from libreprimus.paths import repo_root

gematria_shift_contract_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_shift_contract_app.command("build-contract")
def gematria_shift_build_contract(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5H contract manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5H output directory."),
    contract_out: Path = typer.Option(CONTRACT_PATH, "--contract-out", help="Committed contract YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the Stage 5H Gematria mod-29 shift contract."""

    _require_file(manifest)
    records = build_contract_records(contract_out=_resolve(contract_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"contract_id={record['contract_id']}")
    console.print(f"selected_future_kernel_id={record['selected_future_kernel_id']}")
    console.print(f"token_domain={record['token_domain']}")
    console.print(f"arithmetic_direction={record['arithmetic_direction']}")
    if not allow_warnings:
        return


@gematria_shift_contract_app.command("build-native-fixtures")
def gematria_shift_build_native_fixtures(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5H native fixture manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5H output directory."),
    fixtures_out: Path = typer.Option(FIXTURES_PATH, "--fixtures-out", help="Committed native fixture YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build synthetic numeric Gematria native fixture records."""

    _require_file(manifest)
    records = build_native_fixture_records(fixtures_out=_resolve(fixtures_out), out_dir=_resolve(out_dir))
    record = records[0]
    console.print(f"native_fixture_id={record['fixture_id']}")
    console.print(f"native_fixture_hash={record['expected_output_hash']}")
    console.print(f"stage5f_hash_is_gematria_fixture_hash={str(record['stage5f_hash_is_gematria_fixture_hash']).lower()}")
    if not allow_warnings:
        return


@gematria_shift_contract_app.command("build-solved-fixture-mapping")
def gematria_shift_build_solved_fixture_mapping(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5H solved-fixture mapping manifest."),
    source_manifest: Path = typer.Option(STAGE4O_SOLVED_FIXTURE_MANIFEST, "--source-manifest", help="Stage 4O fixture-safe source manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5H output directory."),
    mapping_out: Path = typer.Option(MAPPING_PATH, "--mapping-out", help="Committed solved fixture mapping YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build solved-fixture-safe mapping records without execution."""

    _require_file(manifest)
    _require_file(source_manifest)
    records = build_solved_fixture_mapping_records(
        manifest=_resolve(source_manifest),
        mapping_out=_resolve(mapping_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"solved_fixture_safe_mappings={len(records)}")
    console.print("solved_fixture_cuda_execution_allowed=false")
    if not allow_warnings:
        return


@gematria_shift_contract_app.command("build-score-summary-plan")
def gematria_shift_build_score_summary_plan(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5H score-summary planning manifest."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5H output directory."),
    score_summary_plan_out: Path = typer.Option(SCORE_PLAN_PATH, "--score-summary-plan-out", help="Committed score-summary parity plan YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build Stage 5H score-summary parity planning records."""

    _require_file(manifest)
    records = build_score_summary_parity_plan_records(
        score_summary_plan_out=_resolve(score_summary_plan_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"score_summary_parity_plan_records={len(records)}")
    console.print("confidence_labels_triage_only=true")
    if not allow_warnings:
        return


@gematria_shift_contract_app.command("build-summary")
def gematria_shift_build_summary(
    contract: Path = typer.Option(CONTRACT_PATH, "--contract", help="Committed contract YAML."),
    fixtures: Path = typer.Option(FIXTURES_PATH, "--fixtures", help="Committed native fixtures YAML."),
    mapping: Path = typer.Option(MAPPING_PATH, "--mapping", help="Committed solved-fixture mapping YAML."),
    score_summary_plan: Path = typer.Option(SCORE_PLAN_PATH, "--score-summary-plan", help="Committed score-summary plan YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5H summary YAML."),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir", help="Generated Stage 5H output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for command symmetry."),
) -> None:
    """Build the committed Stage 5H aggregate summary."""

    for path in (contract, fixtures, mapping, score_summary_plan):
        _require_file(path)
    summary = build_summary(
        contract_path=_resolve(contract),
        fixtures_path=_resolve(fixtures),
        mapping_path=_resolve(mapping),
        score_summary_plan_path=_resolve(score_summary_plan),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "contract_id",
        "selected_future_kernel_id",
        "token_domain",
        "arithmetic_direction",
        "native_fixture_hash",
        "preflight_blocker_count",
    ):
        console.print(f"{key}={summary[key]}")
    if not allow_warnings:
        return


@gematria_shift_contract_app.command("validate-stage5h")
def gematria_shift_validate_stage5h(
    contract: Path = typer.Option(CONTRACT_PATH, "--contract", help="Committed contract YAML."),
    fixtures: Path = typer.Option(FIXTURES_PATH, "--fixtures", help="Committed native fixtures YAML."),
    mapping: Path = typer.Option(MAPPING_PATH, "--mapping", help="Committed solved-fixture mapping YAML."),
    score_summary_plan: Path = typer.Option(SCORE_PLAN_PATH, "--score-summary-plan", help="Committed score-summary plan YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5H summary YAML."),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir", help="Generated Stage 5H output directory."),
) -> None:
    """Validate Stage 5H Gematria shift contract records."""

    try:
        counts, errors = validate_stage5h_results(
            contract_path=_resolve(contract),
            fixtures_path=_resolve(fixtures),
            mapping_path=_resolve(mapping),
            score_summary_plan_path=_resolve(score_summary_plan),
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
    console.print("gematria_shift_contract_stage5h_valid=true")


@gematria_shift_contract_app.command("summary")
def gematria_shift_summary(summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5H summary YAML.")) -> None:
    """Print the committed Stage 5H summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "contract_id",
        "selected_future_kernel_id",
        "token_domain",
        "arithmetic_direction",
        "separator_policy",
        "native_fixture_id",
        "native_fixture_hash",
        "solved_fixture_safe_mapping_records",
        "score_summary_parity_plan_records",
        "production_gematria_mod29_cuda_ready",
        "next_stage",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_shift_contract_app, name="gematria-shift-contract")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
