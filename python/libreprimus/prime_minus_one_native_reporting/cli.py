"""Typer commands for Stage 5Y prime-minus-one native reporting."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.prime_minus_one_native_reporting.cuda_contract_readiness import build_cuda_contract_readiness_gate
from libreprimus.prime_minus_one_native_reporting.full_p56_blocker import build_full_p56_blocker_preservation
from libreprimus.prime_minus_one_native_reporting.generated_body_policy import build_generated_body_policy
from libreprimus.prime_minus_one_native_reporting.guardrails import build_guardrails
from libreprimus.prime_minus_one_native_reporting.method_status_impact import build_method_status_impact
from libreprimus.prime_minus_one_native_reporting.models import (
    CUDA_CONTRACT_READINESS_PATH,
    FULL_P56_BLOCKER_PRESERVATION_PATH,
    GENERATED_BODY_POLICY_PATH,
    GUARDRAIL_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_READINESS_PATH,
    SUMMARY_PATH,
)
from libreprimus.prime_minus_one_native_reporting.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_reporting.parity_report import build_parity_report
from libreprimus.prime_minus_one_native_reporting.result_store_integration import build_result_store_integration
from libreprimus.prime_minus_one_native_reporting.score_summary_integration import build_score_summary_integration
from libreprimus.prime_minus_one_native_reporting.scored_experiment_readiness import build_scored_experiment_readiness
from libreprimus.prime_minus_one_native_reporting.summary import build_summary
from libreprimus.prime_minus_one_native_reporting.validation import validate_stage5y_results

console = Console()
app = typer.Typer(help="Stage 5Y prime-minus-one native reporting commands.", no_args_is_help=True)


@app.command("build-parity-report")
def build_parity_report_command(
    parity_report_out: Path = typer.Option(PARITY_REPORT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_parity_report(parity_report_out=parity_report_out, out_dir=out_dir)
    console.print(f"parity_report_records={len(records)}")
    console.print(f"hash_match_count={sum(1 for record in records if record.get('hash_match') is True)}")
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


@app.command("build-full-p56-blocker-preservation")
def build_full_p56_command(
    full_p56_blocker_preservation_out: Path = typer.Option(FULL_P56_BLOCKER_PRESERVATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_full_p56_blocker_preservation(full_p56_blocker_preservation_out=full_p56_blocker_preservation_out, out_dir=out_dir)
    console.print(f"full_p56_blocker_preservation_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-cuda-contract-readiness-gate")
def build_cuda_gate_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    cuda_contract_readiness_gate_out: Path = typer.Option(CUDA_CONTRACT_READINESS_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_cuda_contract_readiness_gate(
        parity_report=parity_report,
        result_store_integration=result_store_integration,
        score_summary_integration=score_summary_integration,
        cuda_contract_readiness_gate_out=cuda_contract_readiness_gate_out,
        out_dir=out_dir,
    )
    console.print(f"cuda_contract_readiness_gate_records={len(records)}")
    console.print(f"prime_minus_one_cuda_contract_preparation_ready={str(records[0]['prime_minus_one_cuda_contract_preparation_ready']).lower()}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-scored-experiment-readiness")
def build_scored_readiness_command(
    scored_experiment_readiness_out: Path = typer.Option(SCORED_EXPERIMENT_READINESS_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_scored_experiment_readiness(scored_experiment_readiness_out=scored_experiment_readiness_out, out_dir=out_dir)
    console.print(f"bounded_scored_experiment_readiness_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-guardrails")
def build_guardrails_command(
    guardrail_out: Path = typer.Option(GUARDRAIL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_guardrails(guardrail_out=guardrail_out, out_dir=out_dir)
    console.print(f"guardrail_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_decision_command(
    cuda_contract_readiness_gate: Path = typer.Option(CUDA_CONTRACT_READINESS_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_next_stage_decision(
        cuda_contract_readiness_gate=cuda_contract_readiness_gate,
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
    full_p56_blocker_preservation: Path = typer.Option(FULL_P56_BLOCKER_PRESERVATION_PATH),
    cuda_contract_readiness_gate: Path = typer.Option(CUDA_CONTRACT_READINESS_PATH),
    scored_experiment_readiness: Path = typer.Option(SCORED_EXPERIMENT_READINESS_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
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
        full_p56_blocker_preservation=full_p56_blocker_preservation,
        cuda_contract_readiness_gate=cuda_contract_readiness_gate,
        scored_experiment_readiness=scored_experiment_readiness,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"native_parity_report_records={summary['native_parity_report_records']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5y")
def validate_stage5y(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH),
    full_p56_blocker_preservation: Path = typer.Option(FULL_P56_BLOCKER_PRESERVATION_PATH),
    cuda_contract_readiness_gate: Path = typer.Option(CUDA_CONTRACT_READINESS_PATH),
    scored_experiment_readiness: Path = typer.Option(SCORED_EXPERIMENT_READINESS_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5y_results(
        parity_report_path=parity_report,
        result_store_integration_path=result_store_integration,
        score_summary_integration_path=score_summary_integration,
        method_status_impact_path=method_status_impact,
        generated_body_policy_path=generated_body_policy,
        full_p56_blocker_preservation_path=full_p56_blocker_preservation,
        cuda_contract_readiness_gate_path=cuda_contract_readiness_gate,
        scored_experiment_readiness_path=scored_experiment_readiness,
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
    console.print("prime_minus_one_native_reporting_stage5y_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from libreprimus.prime_minus_one_native_reporting.export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "native_parity_report_records",
        "result_store_integration_records",
        "score_summary_integration_records",
        "prime_minus_one_cuda_contract_preparation_ready",
        "bounded_cpu_native_scored_experiment_ready",
        "recommended_next_stage_title",
        "deep_research_recommended_next",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="prime-minus-one-native-reporting")
