"""Typer commands for Stage 5AE corrected bounded p56 reporting."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .archive_source_lock_deferral import build_archive_source_lock_deferral
from .doc_staleness_validation import build_doc_staleness_validation
from .formula_parity_report import build_formula_parity_report
from .full_p56_blocker import build_full_p56_blocker
from .generated_body_policy import build_generated_body_policy
from .hash_material_policy import build_hash_material_policy
from .method_status_impact import build_method_status_impact
from .models import (
    ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH,
    DOC_STALENESS_VALIDATION_PATH,
    FORMULA_PARITY_REPORT_PATH,
    FULL_P56_BLOCKER_PATH,
    GENERATED_BODY_POLICY_PATH,
    HASH_MATERIAL_POLICY_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    REFERENCE_CONTRACT_REPAIR_PATH,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SOURCE_SUMMARY_PATH,
    SUMMARY_PATH,
)
from .next_stage_decision import build_next_stage_decision
from .reference_contract_repair import build_reference_contract_repair
from .result_store_integration import build_result_store_integration
from .score_summary_integration import build_score_summary_integration
from .scored_experiment_deferral import build_scored_experiment_deferral
from .summary import build_summary
from .validation import validate_stage5ae_results

console = Console()
app = typer.Typer(help="Stage 5AE corrected bounded p56 reporting commands.", no_args_is_help=True)


@app.command("build-formula-parity-report")
def build_formula_parity_report_command(
    stage5ad_fix_summary: Path = typer.Option(SOURCE_SUMMARY_PATH),
    formula_parity_report_out: Path = typer.Option(FORMULA_PARITY_REPORT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_formula_parity_report(
        stage5ad_fix_summary=stage5ad_fix_summary,
        formula_parity_report_out=formula_parity_report_out,
        out_dir=out_dir,
    )
    console.print(f"corrected_formula_parity_report_records={len(records)}")
    console.print(f"corrected_formula_parity_status={records[0]['corrected_formula_parity_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-reference-contract-repair")
def build_reference_contract_repair_command(
    reference_contract_repair_out: Path = typer.Option(REFERENCE_CONTRACT_REPAIR_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_reference_contract_repair(reference_contract_repair_out=reference_contract_repair_out, out_dir=out_dir)
    console.print(f"reference_contract_repair_records={len(records)}")
    console.print("reference_contract_repair_complete=true")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-hash-material-policy")
def build_hash_material_policy_command(
    hash_material_policy_out: Path = typer.Option(HASH_MATERIAL_POLICY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_hash_material_policy(hash_material_policy_out=hash_material_policy_out, out_dir=out_dir)
    console.print(f"hash_material_policy_records={len(records)}")
    console.print("hash_material_policy_repair_complete=true")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-result-store-integration")
def build_result_store_integration_command(
    result_store_integration_out: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_result_store_integration(result_store_integration_out=result_store_integration_out, out_dir=out_dir)
    console.print(f"result_store_integration_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-score-summary-integration")
def build_score_summary_integration_command(
    score_summary_integration_out: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_score_summary_integration(score_summary_integration_out=score_summary_integration_out, out_dir=out_dir)
    console.print(f"score_summary_integration_records={len(records)}")
    console.print(f"confidence_label={records[0]['confidence_label']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-method-status-impact")
def build_method_status_impact_command(
    method_status_impact_out: Path = typer.Option(METHOD_STATUS_IMPACT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_method_status_impact(method_status_impact_out=method_status_impact_out, out_dir=out_dir)
    console.print(f"method_status_impact_records={len(records)}")
    console.print(f"method_status_impact_status={records[0]['method_status_impact_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-generated-body-policy")
def build_generated_body_policy_command(
    generated_body_policy_out: Path = typer.Option(GENERATED_BODY_POLICY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_generated_body_policy(generated_body_policy_out=generated_body_policy_out, out_dir=out_dir)
    console.print(f"generated_body_policy_records={len(records)}")
    console.print(f"generated_body_policy_status={records[0]['generated_body_policy_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-full-p56-blocker")
def build_full_p56_blocker_command(
    full_p56_blocker_out: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_full_p56_blocker(full_p56_blocker_out=full_p56_blocker_out, out_dir=out_dir)
    console.print(f"full_p56_blocker_records={len(records)}")
    console.print(f"full_p56_status={records[0]['full_p56_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-scored-experiment-deferral")
def build_scored_experiment_deferral_command(
    scored_experiment_deferral_out: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_scored_experiment_deferral(scored_experiment_deferral_out=scored_experiment_deferral_out, out_dir=out_dir)
    console.print(f"scored_experiment_deferral_records={len(records)}")
    console.print(f"deferral_status={records[0]['deferral_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-archive-source-lock-deferral")
def build_archive_source_lock_deferral_command(
    archive_source_lock_deferral_out: Path = typer.Option(ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_archive_source_lock_deferral(
        archive_source_lock_deferral_out=archive_source_lock_deferral_out,
        out_dir=out_dir,
    )
    console.print(f"archive_source_lock_deferral_records={len(records)}")
    console.print(f"archive_source_lock_ready_next={any(record['archive_source_lock_ready_next'] for record in records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-doc-staleness-validation")
def build_doc_staleness_validation_command(
    doc_staleness_validation_out: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_doc_staleness_validation(doc_staleness_validation_out=doc_staleness_validation_out, out_dir=out_dir)
    console.print(f"doc_staleness_validation_records={len(records)}")
    console.print(f"doc_staleness_validation_status={records[0]['doc_staleness_validation_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_next_stage_decision_command(
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_next_stage_decision(next_stage_decision_out=next_stage_decision_out, out_dir=out_dir)
    selected = next(record for record in records if record["selected"] is True)
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-summary")
def build_summary_command(
    formula_parity_report: Path = typer.Option(FORMULA_PARITY_REPORT_PATH),
    reference_contract_repair: Path = typer.Option(REFERENCE_CONTRACT_REPAIR_PATH),
    hash_material_policy: Path = typer.Option(HASH_MATERIAL_POLICY_PATH),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    archive_source_lock_deferral: Path = typer.Option(ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    summary = build_summary(
        formula_parity_report=formula_parity_report,
        reference_contract_repair=reference_contract_repair,
        hash_material_policy=hash_material_policy,
        result_store_integration=result_store_integration,
        score_summary_integration=score_summary_integration,
        method_status_impact=method_status_impact,
        generated_body_policy=generated_body_policy,
        full_p56_blocker=full_p56_blocker,
        scored_experiment_deferral=scored_experiment_deferral,
        archive_source_lock_deferral=archive_source_lock_deferral,
        doc_staleness_validation=doc_staleness_validation,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"corrected_formula_parity_status={summary['corrected_formula_parity_status']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5ae")
def validate_stage5ae(
    formula_parity_report: Path = typer.Option(FORMULA_PARITY_REPORT_PATH),
    reference_contract_repair: Path = typer.Option(REFERENCE_CONTRACT_REPAIR_PATH),
    hash_material_policy: Path = typer.Option(HASH_MATERIAL_POLICY_PATH),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH),
    full_p56_blocker: Path = typer.Option(FULL_P56_BLOCKER_PATH),
    scored_experiment_deferral: Path = typer.Option(SCORED_EXPERIMENT_DEFERRAL_PATH),
    archive_source_lock_deferral: Path = typer.Option(ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH),
    doc_staleness_validation: Path = typer.Option(DOC_STALENESS_VALIDATION_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5ae_results(
        formula_parity_report_path=formula_parity_report,
        reference_contract_repair_path=reference_contract_repair,
        hash_material_policy_path=hash_material_policy,
        result_store_integration_path=result_store_integration,
        score_summary_integration_path=score_summary_integration,
        method_status_impact_path=method_status_impact,
        generated_body_policy_path=generated_body_policy,
        full_p56_blocker_path=full_p56_blocker,
        scored_experiment_deferral_path=scored_experiment_deferral,
        archive_source_lock_deferral_path=archive_source_lock_deferral,
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
    console.print("corrected_bounded_p56_reporting_stage5ae_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from .export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "historical_stage5ad_failure_preserved",
        "corrected_formula_parity_status",
        "corrected_formula_expected_hash",
        "corrected_formula_computed_hash",
        "reference_contract_repair_complete",
        "hash_material_policy_repair_complete",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="corrected-bounded-p56-reporting")
