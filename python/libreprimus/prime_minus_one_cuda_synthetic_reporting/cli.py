"""Typer commands for Stage 5AC prime-minus-one CUDA synthetic reporting."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.prime_minus_one_cuda_synthetic_reporting.bounded_p56_preflight import build_bounded_p56_preflight
from libreprimus.prime_minus_one_cuda_synthetic_reporting.doc_staleness_validation import build_doc_staleness_validation
from libreprimus.prime_minus_one_cuda_synthetic_reporting.full_p56_blocker import build_full_p56_blocker
from libreprimus.prime_minus_one_cuda_synthetic_reporting.generated_body_policy import build_generated_body_policy
from libreprimus.prime_minus_one_cuda_synthetic_reporting.method_status_impact import build_method_status_impact
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import (
    BOUNDED_P56_PREFLIGHT_PATH,
    DOC_STALENESS_VALIDATION_PATH,
    FULL_P56_BLOCKER_PATH,
    GENERATED_BODY_POLICY_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SUMMARY_PATH,
)
from libreprimus.prime_minus_one_cuda_synthetic_reporting.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_cuda_synthetic_reporting.parity_report import build_parity_report
from libreprimus.prime_minus_one_cuda_synthetic_reporting.result_store_integration import build_result_store_integration
from libreprimus.prime_minus_one_cuda_synthetic_reporting.score_summary_integration import build_score_summary_integration
from libreprimus.prime_minus_one_cuda_synthetic_reporting.scored_experiment_deferral import build_scored_experiment_deferral
from libreprimus.prime_minus_one_cuda_synthetic_reporting.summary import build_summary
from libreprimus.prime_minus_one_cuda_synthetic_reporting.validation import validate_stage5ac_results

console = Console()
app = typer.Typer(help="Stage 5AC prime-minus-one CUDA synthetic reporting commands.", no_args_is_help=True)


@app.command("build-parity-report")
def build_parity_report_command(
    parity_report_out: Path = typer.Option(PARITY_REPORT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_parity_report(parity_report_out=parity_report_out, out_dir=out_dir)
    record = records[0]
    console.print(f"synthetic_parity_report_records={len(records)}")
    console.print(f"parity_status={record['parity_status']}")
    console.print(f"expected_output_token_hash={record['expected_output_token_hash']}")
    console.print(f"computed_output_token_hash={record['computed_output_token_hash']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-result-store-integration")
def build_result_store_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    result_store_integration_out: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_result_store_integration(parity_report=parity_report, result_store_integration_out=result_store_integration_out, out_dir=out_dir)
    console.print(f"result_store_integration_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-score-summary-integration")
def build_score_summary_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    score_summary_integration_out: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_score_summary_integration(parity_report=parity_report, score_summary_integration_out=score_summary_integration_out, out_dir=out_dir)
    console.print(f"score_summary_integration_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-method-status-impact")
def build_method_status_command(
    method_status_impact_out: Path = typer.Option(METHOD_STATUS_IMPACT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_method_status_impact(method_status_impact_out=method_status_impact_out, out_dir=out_dir)
    console.print(f"method_status_impact_records={len(records)}")
    console.print(f"method_status_upgraded_count={sum(1 for record in records if record.get('method_status_upgraded') is True)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-generated-body-policy")
def build_generated_body_policy_command(
    generated_body_policy_out: Path = typer.Option(GENERATED_BODY_POLICY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_generated_body_policy(generated_body_policy_out=generated_body_policy_out, out_dir=out_dir)
    console.print(f"generated_body_policy_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-bounded-p56-preflight")
def build_bounded_p56_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    bounded_p56_preflight_out: Path = typer.Option(BOUNDED_P56_PREFLIGHT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_bounded_p56_preflight(
        parity_report=parity_report,
        doc_staleness_validation=doc_staleness_validation,
        bounded_p56_preflight_out=bounded_p56_preflight_out,
        out_dir=out_dir,
    )
    console.print(f"bounded_p56_preflight_records={len(records)}")
    console.print(f"bounded_p56_preflight_status={records[0]['preflight_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-full-p56-blocker")
def build_full_p56_command(
    full_p56_blocker_out: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_full_p56_blocker(full_p56_blocker_out=full_p56_blocker_out, out_dir=out_dir)
    console.print(f"full_p56_blocker_records={len(records)}")
    console.print(f"full_p56_status={records[0]['full_p56_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-scored-experiment-deferral")
def build_scored_deferral_command(
    scored_experiment_deferral_out: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_scored_experiment_deferral(scored_experiment_deferral_out=scored_experiment_deferral_out, out_dir=out_dir)
    console.print(f"scored_experiment_deferral_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-doc-staleness-validation")
def build_doc_staleness_command(
    doc_staleness_validation_out: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_doc_staleness_validation(doc_staleness_validation_out=doc_staleness_validation_out, out_dir=out_dir)
    console.print(f"doc_staleness_validation_records={len(records)}")
    console.print(f"doc_staleness_strict_check_passed={str(records[0]['doc_staleness_strict_check_passed']).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_next_stage_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    bounded_p56_preflight: Path = typer.Option(BOUNDED_P56_PREFLIGHT_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_next_stage_decision(
        parity_report=parity_report,
        bounded_p56_preflight=bounded_p56_preflight,
        doc_staleness_validation=doc_staleness_validation,
        next_stage_decision_out=next_stage_decision_out,
        out_dir=out_dir,
    )
    selected = next(record for record in records if record.get("selected") is True)
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-summary")
def build_summary_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH),
    bounded_p56_preflight: Path = typer.Option(BOUNDED_P56_PREFLIGHT_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    summary = build_summary(
        parity_report=parity_report,
        result_store_integration=result_store_integration,
        score_summary_integration=score_summary_integration,
        method_status_impact=method_status_impact,
        generated_body_policy=generated_body_policy,
        bounded_p56_preflight=bounded_p56_preflight,
        full_p56_blocker=full_p56_blocker,
        scored_experiment_deferral=scored_experiment_deferral,
        doc_staleness_validation=doc_staleness_validation,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"synthetic_parity_report_records={summary['synthetic_parity_report_records']}")
    console.print(f"bounded_p56_preflight_status={summary['bounded_p56_preflight_status']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5ac")
def validate_stage5ac(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH),
    bounded_p56_preflight: Path = typer.Option(BOUNDED_P56_PREFLIGHT_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5ac_results(
        parity_report_path=parity_report,
        result_store_integration_path=result_store_integration,
        score_summary_integration_path=score_summary_integration,
        method_status_impact_path=method_status_impact,
        generated_body_policy_path=generated_body_policy,
        bounded_p56_preflight_path=bounded_p56_preflight,
        full_p56_blocker_path=full_p56_blocker,
        scored_experiment_deferral_path=scored_experiment_deferral,
        doc_staleness_validation_path=doc_staleness_validation,
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
    console.print("prime_minus_one_cuda_synthetic_reporting_stage5ac_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "synthetic_parity_report_records",
        "source_stage5aa_expected_hash",
        "source_stage5aa_computed_hash",
        "bounded_p56_preflight_status",
        "full_p56_status",
        "stage5ab_doc_staleness_strict_pass",
        "recommended_next_stage_title",
        "deep_research_recommended_next",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="prime-minus-one-cuda-synthetic-reporting")


__all__ = ["register"]
