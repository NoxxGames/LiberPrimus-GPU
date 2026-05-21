"""Stage 5P Gematria CUDA result-store integration CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_cuda_result_store.controlled_expansion_candidates import (
    build_controlled_expansion_candidates,
)
from libreprimus.gematria_cuda_result_store.generated_body_policy import build_generated_body_policy
from libreprimus.gematria_cuda_result_store.method_status_impact import build_method_status_impact
from libreprimus.gematria_cuda_result_store.models import (
    CONTROLLED_EXPANSION_CANDIDATES_PATH,
    GENERATED_BODY_POLICY_PATH,
    METHOD_STATUS_IMPACT_PATH,
    OUTPUT_DIR,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    STAGE4I_CONFIDENCE_LABELS,
    STAGE5O_REPEAT_PARITY,
    STAGE5O_SUMMARY,
    SUMMARY_PATH,
)
from libreprimus.gematria_cuda_result_store.result_store_integration import build_result_store_integration
from libreprimus.gematria_cuda_result_store.score_summary_integration import build_score_summary_integration
from libreprimus.gematria_cuda_result_store.summary import build_summary, load_summary
from libreprimus.gematria_cuda_result_store.validation import validate_stage5p_results
from libreprimus.paths import repo_root

gematria_cuda_result_store_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_cuda_result_store_app.command("build-result-store-integration")
def build_result_store_integration_command(
    repeat_parity: Path = typer.Option(STAGE5O_REPEAT_PARITY, "--repeat-parity"),
    result_store_integration_out: Path = typer.Option(
        RESULT_STORE_INTEGRATION_PATH,
        "--result-store-integration-out",
    ),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build compact Stage 4P-compatible result-store integration records."""

    _require_file(repeat_parity)
    records = build_result_store_integration(
        repeat_parity=_resolve(repeat_parity),
        result_store_integration_out=_resolve(result_store_integration_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"result_store_integration_records={len(records)}")
    console.print("cuda_execution_performed=false")
    if not allow_warnings:
        return


@gematria_cuda_result_store_app.command("build-score-summary-integration")
def build_score_summary_integration_command(
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration"),
    confidence_labels: Path = typer.Option(STAGE4I_CONFIDENCE_LABELS, "--confidence-labels"),
    score_summary_integration_out: Path = typer.Option(
        SCORE_SUMMARY_INTEGRATION_PATH,
        "--score-summary-integration-out",
    ),
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
    console.print("score_summary_contract=stage4i")
    if not allow_warnings:
        return


@gematria_cuda_result_store_app.command("build-method-status-impact")
def build_method_status_impact_command(
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration"),
    method_status_impact_out: Path = typer.Option(METHOD_STATUS_IMPACT_PATH, "--method-status-impact-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build method-status impact records without upgrading any method to solved."""

    _require_file(result_store_integration)
    records = build_method_status_impact(
        result_store_integration=_resolve(result_store_integration),
        method_status_impact_out=_resolve(method_status_impact_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"method_status_impact_records={len(records)}")
    console.print("method_status_upgrade_allowed=false")
    if not allow_warnings:
        return


@gematria_cuda_result_store_app.command("build-generated-body-policy")
def build_generated_body_policy_command(
    generated_body_policy_out: Path = typer.Option(GENERATED_BODY_POLICY_PATH, "--generated-body-policy-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build generated-body publication policy records."""

    records = build_generated_body_policy(
        generated_body_policy_out=_resolve(generated_body_policy_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"generated_body_policy_records={len(records)}")
    console.print("generated_body_publication_allowed=false")
    if not allow_warnings:
        return


@gematria_cuda_result_store_app.command("build-controlled-expansion-candidates")
def build_controlled_expansion_candidates_command(
    controlled_expansion_candidates_out: Path = typer.Option(
        CONTROLLED_EXPANSION_CANDIDATES_PATH,
        "--controlled-expansion-candidates-out",
    ),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build no-execution controlled Stage 5Q candidate records."""

    records = build_controlled_expansion_candidates(
        controlled_expansion_candidates_out=_resolve(controlled_expansion_candidates_out),
        out_dir=_resolve(out_dir),
    )
    ready = sum(1 for record in records if record["candidate_status"] == "ready_for_stage5q_candidate_mapping")
    console.print(f"controlled_expansion_candidate_records={len(records)}")
    console.print(f"controlled_expansion_ready_for_stage5q={ready}")
    if not allow_warnings:
        return


@gematria_cuda_result_store_app.command("build-summary")
def build_summary_command(
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration"),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH, "--score-summary-integration"),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH, "--method-status-impact"),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH, "--generated-body-policy"),
    controlled_expansion_candidates: Path = typer.Option(
        CONTROLLED_EXPANSION_CANDIDATES_PATH,
        "--controlled-expansion-candidates",
    ),
    stage5o_summary: Path = typer.Option(STAGE5O_SUMMARY, "--stage5o-summary"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build the committed Stage 5P summary."""

    for path in (
        result_store_integration,
        score_summary_integration,
        method_status_impact,
        generated_body_policy,
        controlled_expansion_candidates,
        stage5o_summary,
    ):
        _require_file(path)
    payload = build_summary(
        result_store_integration=_resolve(result_store_integration),
        score_summary_integration=_resolve(score_summary_integration),
        method_status_impact=_resolve(method_status_impact),
        generated_body_policy=_resolve(generated_body_policy),
        controlled_expansion_candidates=_resolve(controlled_expansion_candidates),
        stage5o_summary=_resolve(stage5o_summary),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in (
        "result_store_integration_records",
        "score_summary_integration_records",
        "stage4p_compatibility",
        "stage4i_compatibility",
        "selected_next_stage",
    ):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@gematria_cuda_result_store_app.command("validate-stage5p")
def validate_stage5p_command(
    result_store_integration: Path = typer.Option(RESULT_STORE_INTEGRATION_PATH, "--result-store-integration"),
    score_summary_integration: Path = typer.Option(SCORE_SUMMARY_INTEGRATION_PATH, "--score-summary-integration"),
    method_status_impact: Path = typer.Option(METHOD_STATUS_IMPACT_PATH, "--method-status-impact"),
    generated_body_policy: Path = typer.Option(GENERATED_BODY_POLICY_PATH, "--generated-body-policy"),
    controlled_expansion_candidates: Path = typer.Option(
        CONTROLLED_EXPANSION_CANDIDATES_PATH,
        "--controlled-expansion-candidates",
    ),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    """Validate Stage 5P records and ignored generated summary."""

    try:
        counts, errors = validate_stage5p_results(
            result_store_integration_path=_resolve(result_store_integration),
            score_summary_integration_path=_resolve(score_summary_integration),
            method_status_impact_path=_resolve(method_status_impact),
            generated_body_policy_path=_resolve(generated_body_policy),
            controlled_expansion_candidates_path=_resolve(controlled_expansion_candidates),
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
    console.print("gematria_cuda_result_store_stage5p_valid=true")


@gematria_cuda_result_store_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    """Print the committed Stage 5P summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "result_store_integration_records",
        "score_summary_integration_records",
        "method_status_impact_records",
        "generated_body_policy_records",
        "controlled_expansion_candidate_records",
        "stage4p_compatibility",
        "stage4i_compatibility",
        "generated_body_publication_allowed",
        "method_status_upgrade_allowed",
        "selected_next_stage",
        "deep_research_recommended",
        "cuda_execution_performed",
        "new_cuda_kernels_added",
        "cuda_source_modified",
        "unsolved_page_cuda_used",
        "gpu_benchmark_performed",
        "speedup_claim",
        "solve_claim",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_cuda_result_store_app, name="gematria-cuda-result-store")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)
