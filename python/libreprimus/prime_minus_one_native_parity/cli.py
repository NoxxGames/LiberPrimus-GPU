"""Typer commands for Stage 5X prime-minus-one native parity."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.prime_minus_one_native_parity.full_p56_blocker import build_full_p56_blocker
from libreprimus.prime_minus_one_native_parity.guardrails import build_guardrails
from libreprimus.prime_minus_one_native_parity.models import (
    FULL_P56_BLOCKER_PATH,
    GUARDRAIL_PATH,
    NATIVE_PARITY_PATH,
    NATIVE_RUN_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    SUMMARY_PATH,
)
from libreprimus.prime_minus_one_native_parity.native_execution import build_native_run_records
from libreprimus.prime_minus_one_native_parity.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_parity.parity_records import build_parity_records
from libreprimus.prime_minus_one_native_parity.result_store_preflight import build_result_store_preflight
from libreprimus.prime_minus_one_native_parity.score_summary_preflight import build_score_summary_preflight
from libreprimus.prime_minus_one_native_parity.summary import build_summary
from libreprimus.prime_minus_one_native_parity.validation import validate_stage5x_results

console = Console()
app = typer.Typer(help="Stage 5X prime-minus-one no-GPU native parity commands.", no_args_is_help=True)


@app.command("build-run-records")
@app.command("run-native-parity")
def build_run_records(
    native_run_out: Path = typer.Option(NATIVE_RUN_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_native_run_records(native_run_out=native_run_out, out_dir=out_dir)
    console.print(f"native_run_records={len(records)}")
    console.print(f"native_execution_attempted_count={sum(1 for record in records if record.get('native_execution_performed') is True)}")
    console.print(f"native_pass_count={sum(1 for record in records if record.get('native_execution_status') == 'passed')}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-parity-records")
def build_parity(
    native_run: Path = typer.Option(NATIVE_RUN_PATH),
    native_parity_out: Path = typer.Option(NATIVE_PARITY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_parity_records(native_run=native_run, native_parity_out=native_parity_out, out_dir=out_dir)
    console.print(f"native_parity_records={len(records)}")
    console.print(f"native_pass_count={sum(1 for record in records if record.get('parity_status') == 'passed')}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-result-store-preflight")
def build_result_preflight(
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH),
    result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_result_store_preflight(native_parity=native_parity, result_store_preflight_out=result_store_preflight_out, out_dir=out_dir)
    console.print(f"result_store_preflight_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-score-summary-preflight")
def build_score_preflight(
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH),
    score_summary_preflight_out: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_score_summary_preflight(native_parity=native_parity, score_summary_preflight_out=score_summary_preflight_out, out_dir=out_dir)
    console.print(f"score_summary_preflight_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-full-p56-blocker")
def build_p56_blocker(
    full_p56_blocker_out: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_full_p56_blocker(full_p56_blocker_out=full_p56_blocker_out, out_dir=out_dir)
    console.print(f"full_p56_blocker_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-guardrails")
def build_guardrail_records(
    guardrail_out: Path = typer.Option(GUARDRAIL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_guardrails(guardrail_out=guardrail_out, out_dir=out_dir)
    console.print(f"guardrail_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_decisions(
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_next_stage_decision(native_parity=native_parity, next_stage_decision_out=next_stage_decision_out, out_dir=out_dir)
    selected = next(record for record in records if record.get("selected") is True)
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-summary")
def build_summary_command(
    native_run: Path = typer.Option(NATIVE_RUN_PATH),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    summary = build_summary(
        native_run=native_run,
        native_parity=native_parity,
        result_store_preflight=result_store_preflight,
        score_summary_preflight=score_summary_preflight,
        full_p56_blocker=full_p56_blocker,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"native_run_records={summary['native_run_records']}")
    console.print(f"native_pass_count={summary['native_pass_count']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5x")
def validate_stage5x(
    native_run: Path = typer.Option(NATIVE_RUN_PATH),
    native_parity: Path = typer.Option(NATIVE_PARITY_PATH),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH),
    score_summary_preflight: Path = typer.Option(SCORE_SUMMARY_PREFLIGHT_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5x_results(
        native_run_path=native_run,
        native_parity_path=native_parity,
        result_store_preflight_path=result_store_preflight,
        score_summary_preflight_path=score_summary_preflight,
        full_p56_blocker_path=full_p56_blocker,
        guardrail_path=guardrail,
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
    console.print("prime_minus_one_native_parity_stage5x_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from libreprimus.prime_minus_one_native_parity.export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "native_run_records",
        "native_parity_records",
        "native_execution_attempted_count",
        "native_pass_count",
        "native_fail_count",
        "native_skip_count",
        "recommended_next_stage_title",
        "deep_research_recommended_next",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="prime-minus-one-native-parity")
