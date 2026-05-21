"""Stage 5S expanded CUDA parity result-store integration CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_expanded_cuda_result_store.boundary_review import build_boundary_review
from libreprimus.gematria_expanded_cuda_result_store.generated_body_policy import build_generated_body_policy
from libreprimus.gematria_expanded_cuda_result_store.method_status_impact import build_method_status_impact
from libreprimus.gematria_expanded_cuda_result_store.models import (
    BOUNDARY_REVIEW_PATH,
    GENERATED_BODY_POLICY_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STEP_DECISION_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    STAGE4I_CONFIDENCE_LABELS,
    STAGE5R_PARITY,
    STAGE5R_RUN,
    STAGE5R_SUMMARY,
    SUMMARY_PATH,
)
from libreprimus.gematria_expanded_cuda_result_store.next_step_decision import build_next_step_decision
from libreprimus.gematria_expanded_cuda_result_store.parity_report import build_parity_report
from libreprimus.gematria_expanded_cuda_result_store.result_store_integration import build_result_store_integration
from libreprimus.gematria_expanded_cuda_result_store.score_summary_integration import build_score_summary_integration
from libreprimus.gematria_expanded_cuda_result_store.summary import build_summary, load_summary
from libreprimus.gematria_expanded_cuda_result_store.validation import validate_stage5s_results
from libreprimus.paths import repo_root

gematria_expanded_cuda_result_store_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_expanded_cuda_result_store_app.command("build-parity-report")
def build_parity_report_command(
    stage5r_parity: Path = typer.Option(STAGE5R_PARITY, "--stage5r-parity"),
    stage5r_run: Path = typer.Option(STAGE5R_RUN, "--stage5r-run"),
    parity_report_out: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build compact Stage 5S parity-report records from Stage 5R parity."""

    _require_file(stage5r_parity)
    _require_file(stage5r_run)
    records = build_parity_report(
        stage5r_parity=_resolve(stage5r_parity),
        stage5r_run=_resolve(stage5r_run),
        parity_report_out=_resolve(parity_report_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"parity_report_records={len(records)}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("build-result-store-integration")
def build_result_store_integration_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report"),
    result_store_integration_out: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build compact Stage 4P-compatible result-store integration records."""

    _require_file(parity_report)
    records = build_result_store_integration(
        parity_report=_resolve(parity_report),
        result_store_integration_out=_resolve(result_store_integration_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"result_store_integration_records={len(records)}")
    console.print("stage4p_compatibility=true")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("build-score-summary-integration")
def build_score_summary_integration_command(
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration"),
    confidence_labels: Path = typer.Option(STAGE4I_CONFIDENCE_LABELS, "--confidence-labels"),
    score_summary_integration_out: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH, "--score-summary-integration-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 4I-compatible score-summary integration records."""

    _require_file(result_store_integration)
    _require_file(confidence_labels)
    records = build_score_summary_integration(
        result_store_integration=_resolve(result_store_integration),
        confidence_labels=_resolve(confidence_labels),
        score_summary_integration_out=_resolve(score_summary_integration_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"score_summary_integration_records={len(records)}")
    console.print("stage4i_compatibility=true")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("build-method-status-impact")
def build_method_status_impact_command(
    method_status_impact_out: Path = typer.Option(METHOD_STATUS_IMPACT_PATH, "--method-status-impact-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build method-status impact records without solved upgrades."""

    records = build_method_status_impact(method_status_impact_out=_resolve(method_status_impact_out), out_dir=_resolve(out_dir))
    console.print(f"method_status_impact_records={len(records)}")
    console.print("method_status_upgrade_allowed=false")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("build-generated-body-policy")
def build_generated_body_policy_command(
    generated_body_policy_out: Path = typer.Option(GENERATED_BODY_POLICY_PATH, "--generated-body-policy-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build generated-body policy records."""

    records = build_generated_body_policy(generated_body_policy_out=_resolve(generated_body_policy_out), out_dir=_resolve(out_dir))
    console.print(f"generated_body_policy_records={len(records)}")
    console.print("generated_body_publication_allowed=false")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("build-boundary-review")
def build_boundary_review_command(
    boundary_review_out: Path = typer.Option(BOUNDARY_REVIEW_PATH, "--boundary-review-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5R boundary review records."""

    records = build_boundary_review(boundary_review_out=_resolve(boundary_review_out), out_dir=_resolve(out_dir))
    console.print(f"boundary_review_records={len(records)}")
    console.print("unsolved_page_cuda_used=false")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("build-next-step-decision")
def build_next_step_decision_command(
    next_step_decision_out: Path = typer.Option(NEXT_STEP_DECISION_PATH, "--next-step-decision-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build controlled next-step decision records."""

    records = build_next_step_decision(next_step_decision_out=_resolve(next_step_decision_out), out_dir=_resolve(out_dir))
    selected = next(record for record in records if record["selected"])
    console.print(f"controlled_next_step_decision_records={len(records)}")
    console.print(f"selected_next_prompt={selected['selected_next_prompt']}")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("build-summary")
def build_summary_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report"),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration"),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH, "--score-summary-integration"),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH, "--method-status-impact"),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH, "--generated-body-policy"),
    boundary_review: Path = typer.Option(BOUNDARY_REVIEW_PATH, "--boundary-review"),
    next_step_decision: Path = typer.Option(NEXT_STEP_DECISION_PATH, "--next-step-decision"),
    stage5r_summary: Path = typer.Option(STAGE5R_SUMMARY, "--stage5r-summary"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5S aggregate summary."""

    for path in (parity_report, result_store_integration, score_summary_integration, method_status_impact, generated_body_policy, boundary_review, next_step_decision, stage5r_summary):
        _require_file(path)
    payload = build_summary(
        parity_report=_resolve(parity_report),
        result_store_integration=_resolve(result_store_integration),
        score_summary_integration=_resolve(score_summary_integration),
        method_status_impact=_resolve(method_status_impact),
        generated_body_policy=_resolve(generated_body_policy),
        boundary_review=_resolve(boundary_review),
        next_step_decision=_resolve(next_step_decision),
        stage5r_summary=_resolve(stage5r_summary),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in ("parity_report_records", "result_store_integration_records", "score_summary_integration_records", "deep_research_recommended", "selected_next_prompt"):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@gematria_expanded_cuda_result_store_app.command("validate-stage5s")
def validate_stage5s_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report"),
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration"),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH, "--score-summary-integration"),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH, "--method-status-impact"),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH, "--generated-body-policy"),
    boundary_review: Path = typer.Option(BOUNDARY_REVIEW_PATH, "--boundary-review"),
    next_step_decision: Path = typer.Option(NEXT_STEP_DECISION_PATH, "--next-step-decision"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    """Validate Stage 5S records and generated summary presence."""

    try:
        counts, errors = validate_stage5s_results(
            parity_report_path=_resolve(parity_report),
            result_store_integration_path=_resolve(result_store_integration),
            score_summary_integration_path=_resolve(score_summary_integration),
            method_status_impact_path=_resolve(method_status_impact),
            generated_body_policy_path=_resolve(generated_body_policy),
            boundary_review_path=_resolve(boundary_review),
            next_step_decision_path=_resolve(next_step_decision),
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
    console.print("gematria_expanded_cuda_result_store_stage5s_valid=true")


@gematria_expanded_cuda_result_store_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    """Print Stage 5S summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "source_stage5r_records_consumed",
        "parity_report_records",
        "result_store_integration_records",
        "score_summary_integration_records",
        "method_status_impact_records",
        "generated_body_policy_records",
        "boundary_review_records",
        "controlled_next_step_decision_records",
        "stage4p_compatibility",
        "stage4i_compatibility",
        "deep_research_recommended",
        "selected_next_prompt",
        "cuda_execution_performed",
        "cuda_source_modified",
        "new_cuda_kernels_added",
        "gpu_benchmark_performed",
        "speedup_claim",
        "solve_claim",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_expanded_cuda_result_store_app, name="gematria-expanded-cuda-result-store")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
