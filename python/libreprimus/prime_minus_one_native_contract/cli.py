"""Typer commands for Stage 5W prime-minus-one native contract preparation."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.paths import repo_root
from libreprimus.prime_minus_one_native_contract.candidate_batch_mapping import build_candidate_batch_mapping
from libreprimus.prime_minus_one_native_contract.export import write_warnings
from libreprimus.prime_minus_one_native_contract.guardrails import build_guardrails
from libreprimus.prime_minus_one_native_contract.models import (
    CANDIDATE_BATCH_MAPPING_PATH,
    GUARDRAIL_PATH,
    NATIVE_PARITY_PREPARATION_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    PRIME_SCHEDULE_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    SOURCE_INVENTORY_PATH,
    STREAM_CONTRACT_PATH,
    SUMMARY_PATH,
)
from libreprimus.prime_minus_one_native_contract.native_parity_preparation import build_native_parity_preparation
from libreprimus.prime_minus_one_native_contract.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_contract.prime_schedule import build_prime_schedule
from libreprimus.prime_minus_one_native_contract.result_store_preflight import build_result_store_preflight
from libreprimus.prime_minus_one_native_contract.source_inventory import build_source_inventory
from libreprimus.prime_minus_one_native_contract.stream_contract import build_stream_contract
from libreprimus.prime_minus_one_native_contract.summary import build_summary, load_summary
from libreprimus.prime_minus_one_native_contract.validation import validate_stage5w_results

prime_minus_one_native_contract_app = typer.Typer(no_args_is_help=True)
console = Console()


@prime_minus_one_native_contract_app.command("build-source-inventory")
def build_source_inventory_command(
    source_inventory_out: Path = typer.Option(SOURCE_INVENTORY_PATH, "--source-inventory-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_source_inventory(source_inventory_out=_resolve(source_inventory_out), out_dir=_resolve(out_dir))
    console.print(f"source_inventory_records={len(records)}")
    console.print("p56_fixture_records_found=true")
    if allow_warnings:
        write_warnings(_resolve(out_dir), ["full_p56_fixture_token_buffer_not_committed; bounded_stage4o_p56_mapping_is_available"])


@prime_minus_one_native_contract_app.command("build-stream-contract")
def build_stream_contract_command(
    stream_contract_out: Path = typer.Option(STREAM_CONTRACT_PATH, "--stream-contract-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_stream_contract(stream_contract_out=_resolve(stream_contract_out), out_dir=_resolve(out_dir))
    console.print(f"stream_contract_records={len(records)}")
    console.print("formula_direction_status=source_backed")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("build-prime-schedule")
def build_prime_schedule_command(
    prime_schedule_out: Path = typer.Option(PRIME_SCHEDULE_PATH, "--prime-schedule-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_prime_schedule(prime_schedule_out=_resolve(prime_schedule_out), out_dir=_resolve(out_dir))
    console.print(f"prime_schedule_records={len(records)}")
    console.print(f"synthetic_control_schedule_records={sum(1 for record in records if str(record['schedule_status']).startswith('synthetic'))}")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("build-candidate-batch-mapping")
def build_candidate_batch_mapping_command(
    candidate_batch_mapping_out: Path = typer.Option(CANDIDATE_BATCH_MAPPING_PATH, "--candidate-batch-mapping-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_candidate_batch_mapping(candidate_batch_mapping_out=_resolve(candidate_batch_mapping_out), out_dir=_resolve(out_dir))
    console.print(f"candidate_batch_mapping_records={len(records)}")
    console.print("p56_candidate_batch_mapping_status=p56_solved_fixture_ready_for_bounded_stage4o_mapping")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("build-native-parity-preparation")
def build_native_parity_preparation_command(
    native_parity_preparation_out: Path = typer.Option(NATIVE_PARITY_PREPARATION_PATH, "--native-parity-preparation-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_native_parity_preparation(
        native_parity_preparation_out=_resolve(native_parity_preparation_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"native_parity_preparation_records={len(records)}")
    console.print(f"preparation_hash_records={sum(1 for record in records if record.get('expected_output_token_hash'))}")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("build-result-store-preflight")
def build_result_store_preflight_command(
    result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_result_store_preflight(result_store_preflight_out=_resolve(result_store_preflight_out), out_dir=_resolve(out_dir))
    console.print(f"result_store_preflight_records={len(records)}")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("build-guardrails")
def build_guardrails_command(
    guardrail_out: Path = typer.Option(GUARDRAIL_PATH, "--guardrail-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_guardrails(guardrail_out=_resolve(guardrail_out), out_dir=_resolve(out_dir))
    console.print(f"guardrail_records={len(records)}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("build-next-stage-decision")
def build_next_stage_decision_command(
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    records = build_next_stage_decision(next_stage_decision_out=_resolve(next_stage_decision_out), out_dir=_resolve(out_dir))
    selected = next(record for record in records if record["selected"])
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("build-summary")
def build_summary_command(
    source_inventory: Path = typer.Option(SOURCE_INVENTORY_PATH, "--source-inventory"),
    stream_contract: Path = typer.Option(STREAM_CONTRACT_PATH, "--stream-contract"),
    prime_schedule: Path = typer.Option(PRIME_SCHEDULE_PATH, "--prime-schedule"),
    candidate_batch_mapping: Path = typer.Option(CANDIDATE_BATCH_MAPPING_PATH, "--candidate-batch-mapping"),
    native_parity_preparation: Path = typer.Option(NATIVE_PARITY_PREPARATION_PATH, "--native-parity-preparation"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    guardrail: Path = typer.Option(GUARDRAIL_PATH, "--guardrail"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    payload = build_summary(
        source_inventory=_resolve(source_inventory),
        stream_contract=_resolve(stream_contract),
        prime_schedule=_resolve(prime_schedule),
        candidate_batch_mapping=_resolve(candidate_batch_mapping),
        native_parity_preparation=_resolve(native_parity_preparation),
        result_store_preflight=_resolve(result_store_preflight),
        guardrail=_resolve(guardrail),
        next_stage_decision=_resolve(next_stage_decision),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"source_inventory_records={payload['source_inventory_records']}")
    console.print(f"native_parity_preparation_records={payload['native_parity_preparation_records']}")
    console.print(f"recommended_next_stage_title={payload['recommended_next_stage_title']}")
    if not allow_warnings:
        return


@prime_minus_one_native_contract_app.command("validate-stage5w")
def validate_stage5w_command(
    source_inventory: Path = typer.Option(SOURCE_INVENTORY_PATH, "--source-inventory"),
    stream_contract: Path = typer.Option(STREAM_CONTRACT_PATH, "--stream-contract"),
    prime_schedule: Path = typer.Option(PRIME_SCHEDULE_PATH, "--prime-schedule"),
    candidate_batch_mapping: Path = typer.Option(CANDIDATE_BATCH_MAPPING_PATH, "--candidate-batch-mapping"),
    native_parity_preparation: Path = typer.Option(NATIVE_PARITY_PREPARATION_PATH, "--native-parity-preparation"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    guardrail: Path = typer.Option(GUARDRAIL_PATH, "--guardrail"),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH, "--next-stage-decision"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    counts, errors = validate_stage5w_results(
        source_inventory_path=_resolve(source_inventory),
        stream_contract_path=_resolve(stream_contract),
        prime_schedule_path=_resolve(prime_schedule),
        candidate_batch_mapping_path=_resolve(candidate_batch_mapping),
        native_parity_preparation_path=_resolve(native_parity_preparation),
        result_store_preflight_path=_resolve(result_store_preflight),
        guardrail_path=_resolve(guardrail),
        next_stage_decision_path=_resolve(next_stage_decision),
        summary_path=_resolve(summary),
        results_dir=_resolve(results_dir),
    )
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("prime_minus_one_native_contract_stage5w_valid=true")


@prime_minus_one_native_contract_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    payload = load_summary(_resolve(summary))
    for key in (
        "source_inventory_records",
        "stream_contract_records",
        "prime_schedule_records",
        "candidate_batch_mapping_records",
        "native_parity_preparation_records",
        "result_store_preflight_records",
        "guardrail_records",
        "next_stage_decision_records",
        "p56_native_parity_preparation_status",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload[key]}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(prime_minus_one_native_contract_app, name="prime-minus-one-native-contract")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
