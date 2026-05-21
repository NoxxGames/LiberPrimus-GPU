"""Stage 5N solved-fixture-safe Gematria CUDA reporting CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.gematria_solved_fixture_cuda_reporting.boundary_review import build_boundary_review
from libreprimus.gematria_solved_fixture_cuda_reporting.controlled_expansion_gate import (
    build_controlled_expansion_gate,
)
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    BOUNDARY_REVIEW_PATH,
    CONTROLLED_EXPANSION_GATE_PATH,
    NO_UNSOLVED_GUARDRAIL_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    STAGE4P_SUMMARY,
    STAGE5M_PARITY_RECORDS,
    STAGE5M_RUN_RECORDS,
    STAGE5M_SUMMARY,
    SUMMARY_PATH,
)
from libreprimus.gematria_solved_fixture_cuda_reporting.no_unsolved_guardrail import (
    build_no_unsolved_guardrail,
)
from libreprimus.gematria_solved_fixture_cuda_reporting.parity_report import build_parity_report
from libreprimus.gematria_solved_fixture_cuda_reporting.result_store_preflight import (
    build_result_store_preflight,
)
from libreprimus.gematria_solved_fixture_cuda_reporting.summary import build_summary, load_summary
from libreprimus.gematria_solved_fixture_cuda_reporting.validation import validate_stage5n_results
from libreprimus.paths import repo_root

gematria_solved_fixture_cuda_reporting_app = typer.Typer(no_args_is_help=True)
console = Console()


@gematria_solved_fixture_cuda_reporting_app.command("build-parity-report")
def build_parity_report_command(
    stage5m_run_records: Path = typer.Option(STAGE5M_RUN_RECORDS, "--stage5m-run-records"),
    stage5m_parity_records: Path = typer.Option(STAGE5M_PARITY_RECORDS, "--stage5m-parity-records"),
    stage5m_summary: Path = typer.Option(STAGE5M_SUMMARY, "--stage5m-summary"),
    parity_report_out: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5N parity report records from committed Stage 5M records."""

    for path in (stage5m_run_records, stage5m_parity_records, stage5m_summary):
        _require_file(path)
    records = build_parity_report(
        stage5m_run_records=_resolve(stage5m_run_records),
        stage5m_parity_records=_resolve(stage5m_parity_records),
        stage5m_summary=_resolve(stage5m_summary),
        parity_report_out=_resolve(parity_report_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"parity_report_records={len(records)}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_reporting_app.command("build-controlled-expansion-gate")
def build_controlled_expansion_gate_command(
    controlled_expansion_gate_out: Path = typer.Option(CONTROLLED_EXPANSION_GATE_PATH, "--controlled-expansion-gate-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5N controlled expansion gate records."""

    records = build_controlled_expansion_gate(
        controlled_expansion_gate_out=_resolve(controlled_expansion_gate_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"controlled_expansion_gate_records={len(records)}")
    console.print(f"gate_status_counts={_counts(records, 'gate_status')}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_reporting_app.command("build-boundary-review")
def build_boundary_review_command(
    stage5m_summary: Path = typer.Option(STAGE5M_SUMMARY, "--stage5m-summary"),
    boundary_review_out: Path = typer.Option(BOUNDARY_REVIEW_PATH, "--boundary-review-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5N boundary review records."""

    _require_file(stage5m_summary)
    records = build_boundary_review(
        stage5m_summary=_resolve(stage5m_summary),
        boundary_review_out=_resolve(boundary_review_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"boundary_review_records={len(records)}")
    console.print(f"cuda_source_modified={records[0]['cuda_source_modified']}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_reporting_app.command("build-result-store-preflight")
def build_result_store_preflight_command(
    stage4p_summary: Path = typer.Option(STAGE4P_SUMMARY, "--stage4p-summary"),
    result_store_preflight_out: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5N result-store and score-summary preflight records."""

    records = build_result_store_preflight(
        stage4p_summary=stage4p_summary,
        result_store_preflight_out=_resolve(result_store_preflight_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"result_store_preflight_records={len(records)}")
    console.print(f"stage4p_summary_present={records[0]['stage4p_summary_present']}")
    if not allow_warnings and not records[0]["stage4p_summary_present"]:
        raise typer.Exit(1)


@gematria_solved_fixture_cuda_reporting_app.command("build-no-unsolved-guardrail")
def build_no_unsolved_guardrail_command(
    no_unsolved_guardrail_out: Path = typer.Option(NO_UNSOLVED_GUARDRAIL_PATH, "--no-unsolved-guardrail-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build Stage 5N no-unsolved guardrail records."""

    records = build_no_unsolved_guardrail(
        no_unsolved_guardrail_out=_resolve(no_unsolved_guardrail_out),
        out_dir=_resolve(out_dir),
    )
    console.print(f"no_unsolved_guardrail_records={len(records)}")
    console.print(f"no_unsolved_guardrail_status_counts={_counts(records, 'guardrail_status')}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_reporting_app.command("build-summary")
def build_summary_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report"),
    controlled_expansion_gate: Path = typer.Option(CONTROLLED_EXPANSION_GATE_PATH, "--controlled-expansion-gate"),
    boundary_review: Path = typer.Option(BOUNDARY_REVIEW_PATH, "--boundary-review"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    no_unsolved_guardrail: Path = typer.Option(NO_UNSOLVED_GUARDRAIL_PATH, "--no-unsolved-guardrail"),
    stage5m_summary: Path = typer.Option(STAGE5M_SUMMARY, "--stage5m-summary"),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out"),
    out_dir: Path = typer.Option(OUTPUT_DIR, "--out-dir"),
    allow_warnings: bool = typer.Option(False, "--allow-warnings"),
) -> None:
    """Build the committed Stage 5N reporting summary."""

    for path in (parity_report, controlled_expansion_gate, boundary_review, result_store_preflight, no_unsolved_guardrail, stage5m_summary):
        _require_file(path)
    payload = build_summary(
        parity_report=_resolve(parity_report),
        controlled_expansion_gate=_resolve(controlled_expansion_gate),
        boundary_review=_resolve(boundary_review),
        result_store_preflight=_resolve(result_store_preflight),
        no_unsolved_guardrail=_resolve(no_unsolved_guardrail),
        stage5m_summary=_resolve(stage5m_summary),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in ("parity_report_records", "gate_records", "boundary_review_records", "selected_next_stage"):
        console.print(f"{key}={payload[key]}")
    if not allow_warnings:
        return


@gematria_solved_fixture_cuda_reporting_app.command("validate-stage5n")
def validate_stage5n_command(
    parity_report: Path = typer.Option(PARITY_REPORT_PATH, "--parity-report"),
    controlled_expansion_gate: Path = typer.Option(CONTROLLED_EXPANSION_GATE_PATH, "--controlled-expansion-gate"),
    boundary_review: Path = typer.Option(BOUNDARY_REVIEW_PATH, "--boundary-review"),
    result_store_preflight: Path = typer.Option(RESULT_STORE_PREFLIGHT_PATH, "--result-store-preflight"),
    no_unsolved_guardrail: Path = typer.Option(NO_UNSOLVED_GUARDRAIL_PATH, "--no-unsolved-guardrail"),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary"),
    results_dir: Path = typer.Option(OUTPUT_DIR, "--results-dir"),
) -> None:
    """Validate Stage 5N reporting records."""

    try:
        counts, errors = validate_stage5n_results(
            parity_report_path=_resolve(parity_report),
            controlled_expansion_gate_path=_resolve(controlled_expansion_gate),
            boundary_review_path=_resolve(boundary_review),
            result_store_preflight_path=_resolve(result_store_preflight),
            no_unsolved_guardrail_path=_resolve(no_unsolved_guardrail),
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
    console.print("gematria_solved_fixture_cuda_reporting_stage5n_valid=true")


@gematria_solved_fixture_cuda_reporting_app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH, "--summary")) -> None:
    """Print the Stage 5N summary."""

    payload = load_summary(_resolve(summary))
    for key in (
        "parity_report_records",
        "gate_records",
        "boundary_review_records",
        "result_store_preflight_records",
        "no_unsolved_guardrail_records",
        "controlled_expansion_gate_status_counts",
        "selected_next_stage",
        "selected_next_stage_reason",
        "unsolved_page_cuda_allowed",
        "additional_cuda_execution_performed",
        "new_cuda_kernels_added",
        "cuda_source_modified",
        "real_liber_primus_cuda_data_used",
        "solved_fixture_cuda_used",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(gematria_solved_fixture_cuda_reporting_app, name="gematria-solved-fixture-cuda-reporting")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]Missing required file: {resolved}[/red]")
        raise typer.Exit(1)


def _counts(records: list[dict[str, object]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(record[key])
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))
