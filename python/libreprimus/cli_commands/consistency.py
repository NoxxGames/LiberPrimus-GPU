"""Consistency CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *
from libreprimus.stage_state.current import current_latest_stage_label, current_next_stage_label

consistency_app = typer.Typer(no_args_is_help=True)


def _print_consistency_suite(suite) -> None:
    console.print(f"suite_id={suite.suite_id}")
    console.print(f"check_count={suite.check_count}")
    console.print(f"pass_count={suite.pass_count}")
    console.print(f"fail_count={suite.fail_count}")
    console.print(f"warning_count={suite.warning_count}")
    console.print(f"skipped_count={suite.skipped_count}")
    for result in suite.results:
        if result.is_failure:
            console.print(f"[red]{result.check_group}:{result.check_name}: {result.message}[/red]")
        elif result.is_warning:
            console.print(f"[yellow]{result.check_group}:{result.check_name}: {result.message}[/yellow]")


def _run_consistency_cli(
    groups: list[str],
    *,
    out: Path | None = None,
    allow_warnings: bool = False,
    allow_missing_generated: bool = True,
) -> None:
    output_path = _resolve_output_path(out) if out is not None else None
    from libreprimus import cli as public_cli

    suite = public_cli.run_consistency_suite(
        groups,
        out=output_path,
        allow_missing_generated=allow_missing_generated,
    )
    _print_consistency_suite(suite)
    if output_path is not None:
        console.print(f"summary={output_path}")
    if suite.has_failures:
        raise typer.Exit(1)
    if suite.has_warnings and not allow_warnings:
        raise typer.Exit(1)
    console.print("Consistency checks OK")


@consistency_app.command("check-all")
def consistency_check_all(
    out: Path | None = typer.Option(None, "--out", help="Generated consistency summary JSON path."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run the raw-data-free consistency suite, including anti-drift checks."""
    _run_consistency_cli(
        [
            "registry",
            "manifests",
            "schemas",
            "docs",
            "ignored_outputs",
            "result_store",
            "state_drift",
        ],
        out=out,
        allow_warnings=allow_warnings,
        allow_missing_generated=True,
    )


@consistency_app.command("check-registry")
def consistency_check_registry(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run transform-registry consistency checks."""
    _run_consistency_cli(["registry"], allow_warnings=allow_warnings)


@consistency_app.command("check-manifests")
def consistency_check_manifests(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run solved-baseline and result-store manifest consistency checks."""
    _run_consistency_cli(["manifests"], allow_warnings=allow_warnings)


@consistency_app.command("check-schemas")
def consistency_check_schemas(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run schema consistency checks."""
    _run_consistency_cli(["schemas"], allow_warnings=allow_warnings)


@consistency_app.command("check-docs")
def consistency_check_docs(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run public documentation consistency checks."""
    _run_consistency_cli(["docs"], allow_warnings=allow_warnings)


@consistency_app.command("check-state-drift")
def consistency_check_state_drift(
    out: Path | None = typer.Option(None, "--out", help="Generated state-drift summary JSON path."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run persistent project-state anti-drift checks."""
    _run_consistency_cli(["state_drift"], out=out, allow_warnings=allow_warnings)


@consistency_app.command("check-doc-staleness")
def consistency_check_doc_staleness(
    repo_root_path: Path = typer.Option(Path("."), "--repo-root", help="Repository root to scan."),
    source_of_truth: Path = typer.Option(
        Path("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml"),
        "--source-of-truth",
        help="Document-staleness source-of-truth YAML.",
    ),
    output_format: str = typer.Option("text", "--format", help="Output format: text, json, or jsonl."),
    write_report: Path | None = typer.Option(None, "--write-report", help="Generated JSON findings report path."),
    strict: bool = typer.Option(False, "--strict", help="Return failure when findings are present."),
) -> None:
    """Run dynamic operational Markdown staleness checks."""

    from libreprimus.doc_staleness.export import write_report_bundle
    from libreprimus.doc_staleness.scanner import scan_repository

    base = repo_root_path.resolve()
    scan = scan_repository(root=base, source_of_truth_path=source_of_truth)
    if write_report is not None:
        write_report_bundle(scan, _resolve_output_path(write_report))
    payload = {
        "summary": scan.summary_dict(),
        "findings": [finding.to_dict() for finding in scan.findings],
    }
    if output_format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif output_format == "jsonl":
        for finding in scan.findings:
            print(json.dumps(finding.to_dict(), sort_keys=True))
    elif output_format == "text":
        console.print(f"doc_staleness_scanned_paths={len(scan.scanned_paths)}")
        console.print(f"doc_staleness_findings={scan.finding_count}")
        console.print(f"doc_staleness_warnings={len(scan.warnings)}")
        for finding in scan.findings:
            console.print(
                f"[red]{finding.rule_id}:{finding.path}:{finding.line}: "
                f"{finding.message}[/red]"
            )
    else:
        console.print(f"[red]Unsupported format: {output_format}[/red]")
        raise typer.Exit(2)
    if scan.finding_count and strict:
        raise typer.Exit(1)
    console.print("doc_staleness_valid=true")


@consistency_app.command("check-stage-ledger-staleness")
def consistency_check_stage_ledger_staleness(
    expected_latest_stage: str | None = typer.Option(None, "--expected-latest-stage"),
    expected_next_stage: str | None = typer.Option(None, "--expected-next-stage"),
    operational_file_map: Path = typer.Option(Path("data/project-state/operational-file-map.yaml")),
    out: Path | None = typer.Option(None, "--out"),
    strict: bool = typer.Option(True, "--strict/--no-strict"),
) -> None:
    """Check mutable operational docs for stale stage-ledger truncation."""

    from libreprimus.doc_staleness.reporting import write_json_report
    from libreprimus.doc_staleness.source_of_truth import load_operational_paths
    from libreprimus.doc_staleness.stage_ledger import scan_stage_ledgers

    expected_latest_stage = expected_latest_stage or current_latest_stage_label()
    expected_next_stage = expected_next_stage or current_next_stage_label()
    if not expected_latest_stage or not expected_next_stage:
        console.print("[red]current-stage registry is missing latest/next stage labels[/red]")
        raise typer.Exit(2)
    base = Path(".").resolve()
    paths = load_operational_paths(operational_file_map, root=base)
    report = scan_stage_ledgers(
        paths=paths,
        root=base,
        expected_latest_stage=expected_latest_stage,
    )
    report["expected_next_stage"] = expected_next_stage
    if out is not None:
        write_json_report(_resolve_output_path(out), report)
    console.print(f"stage_ledger_sections_scanned={report['sections_scanned']}")
    console.print(f"stage_ledger_findings={report['finding_count']}")
    console.print(f"stage_ledger_warnings={report['warning_count']}")
    if report["finding_count"] and strict:
        raise typer.Exit(1)
    console.print("stage_ledger_staleness_valid=true")


@consistency_app.command("check-operational-file-map-coverage")
def consistency_check_operational_file_map_coverage(
    operational_file_map: Path = typer.Option(Path("data/project-state/operational-file-map.yaml")),
    out: Path | None = typer.Option(None, "--out"),
    strict: bool = typer.Option(True, "--strict/--no-strict"),
) -> None:
    """Check operational-file-map coverage for mutable current-state files."""

    from libreprimus.doc_staleness.coverage import build_operational_file_map_coverage
    from libreprimus.doc_staleness.reporting import write_json_report

    report = build_operational_file_map_coverage(operational_file_map=operational_file_map)
    if out is not None:
        write_json_report(_resolve_output_path(out), report)
    console.print(f"operational_file_map_records={report['record_count']}")
    console.print(f"operational_file_map_coverage_findings={report['coverage_finding_count']}")
    if report["coverage_finding_count"] and strict:
        raise typer.Exit(1)
    console.print("operational_file_map_coverage_valid=true")


@consistency_app.command("check-current-next-stage-consistency")
def consistency_check_current_next_stage_consistency(
    expected_latest_stage: str | None = typer.Option(None, "--expected-latest-stage"),
    expected_next_stage: str | None = typer.Option(None, "--expected-next-stage"),
    source_of_truth: Path = typer.Option(
        Path("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml"),
        "--source-of-truth",
    ),
    out: Path | None = typer.Option(None, "--out"),
    strict: bool = typer.Option(True, "--strict/--no-strict"),
) -> None:
    """Check current/latest/next-stage claims against the active source-of-truth."""

    from libreprimus.doc_staleness.current_context import build_current_next_stage_report
    from libreprimus.doc_staleness.reporting import write_json_report

    expected_latest_stage = expected_latest_stage or current_latest_stage_label()
    expected_next_stage = expected_next_stage or current_next_stage_label()
    if not expected_latest_stage or not expected_next_stage:
        console.print("[red]current-stage registry is missing latest/next stage labels[/red]")
        raise typer.Exit(2)
    report = build_current_next_stage_report(
        root=Path(".").resolve(),
        source_of_truth=source_of_truth,
        expected_latest_stage=expected_latest_stage,
        expected_next_stage=expected_next_stage,
    )
    if out is not None:
        write_json_report(_resolve_output_path(out), report)
    console.print(f"current_next_scanned_paths={report['scanned_path_count']}")
    console.print(f"current_next_findings={report['finding_count']}")
    console.print(f"current_next_warnings={report['warning_count']}")
    if report["finding_count"] and strict:
        raise typer.Exit(1)
    console.print("current_next_stage_consistency_valid=true")


@consistency_app.command("validate-stage5ah-doc-staleness")
def consistency_validate_stage5ah_doc_staleness(
    source_of_truth: Path = typer.Option(..., "--source-of-truth"),
    findings: Path = typer.Option(..., "--findings"),
    stage_ledger_coverage: Path = typer.Option(..., "--stage-ledger-coverage"),
    operational_file_map_coverage: Path = typer.Option(..., "--operational-file-map-coverage"),
    next_stage_decision: Path = typer.Option(..., "--next-stage-decision"),
    summary: Path = typer.Option(..., "--summary"),
    results_dir: Path = typer.Option(..., "--results-dir"),
) -> None:
    """Validate Stage 5AH doc-staleness repair records."""

    from libreprimus.doc_staleness.validation import validate_stage5ah_doc_staleness_records

    errors = validate_stage5ah_doc_staleness_records(
        source_of_truth_path=source_of_truth,
        findings_path=findings,
        stage_ledger_coverage_path=stage_ledger_coverage,
        operational_file_map_coverage_path=operational_file_map_coverage,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("stage5ah_doc_staleness_valid=true")


@consistency_app.command("check-ignored-outputs")
def consistency_check_ignored_outputs(
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run ignored-output policy consistency checks."""
    _run_consistency_cli(["ignored_outputs"], allow_warnings=allow_warnings)


@consistency_app.command("check-result-store")
def consistency_check_result_store(
    allow_missing_generated: bool = typer.Option(
        False,
        "--allow-missing-generated",
        help="Return success if local generated result-store outputs are absent.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run result-store consistency checks."""
    _run_consistency_cli(
        ["result_store"],
        allow_warnings=allow_warnings,
        allow_missing_generated=allow_missing_generated,
    )




@consistency_app.command("check-current-truth-authority")
def consistency_check_current_truth_authority() -> None:
    """Run Stage 5EF current-truth authority checks."""

    from libreprimus.token_block import stage5ef

    result = stage5ef.validate_stage5ef_current_truth()
    console.print(f"current_truth_authority_error_count={len(result.errors)}")
    for error in result.errors:
        console.print(f"[red]{error}[/red]")
    if result.errors:
        raise typer.Exit(1)
    console.print("current_truth_authority_valid=true")


@consistency_app.command("check-doc-update-policy")
def consistency_check_doc_update_policy() -> None:
    """Run Stage 5EF document update-policy checks."""

    from libreprimus.token_block import stage5ef

    result = stage5ef.validate_stage5ef_doc_update_policy()
    console.print(f"doc_update_policy_error_count={len(result.errors)}")
    for error in result.errors:
        console.print(f"[red]{error}[/red]")
    if result.errors:
        raise typer.Exit(1)
    console.print("doc_update_policy_valid=true")


@consistency_app.command("generate-context-pack")
def consistency_generate_context_pack(
    pack: str = typer.Option(..., "--pack", help="Stage 5EF context-pack id."),
    out: Path | None = typer.Option(None, "--out", help="Ignored output path for the rendered context pack."),
) -> None:
    """Render a deterministic Stage 5EF context-pack template."""

    from libreprimus.token_block import stage5ef

    text = stage5ef.render_context_pack(pack)
    if out is not None:
        output_path = _resolve_output_path(out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
        console.print(f"context_pack_written={output_path}")
    else:
        console.print(text)
    console.print("context_pack_generated=true")


@consistency_app.command("audit-doc-drift")
def consistency_audit_doc_drift(
    no_fix: bool = typer.Option(True, "--no-fix", help="Report only; fixes are not supported in Stage 5EF."),
    out: Path | None = typer.Option(None, "--out", help="Ignored output path for the JSON report."),
) -> None:
    """Build a report-only Stage 5EF doc drift audit payload."""

    from libreprimus.token_block import stage5ef
    from libreprimus.token_block.models import write_json

    if not no_fix:
        console.print("[red]Stage 5EF doc drift audits are report-only; use --no-fix[/red]")
        raise typer.Exit(2)
    report = stage5ef.build_doc_drift_audit_report()
    if out is not None:
        write_json(_resolve_output_path(out), report)
        console.print(f"doc_drift_audit_report={out}")
    console.print(f"doc_drift_audit_doc_role_count={report['doc_role_count']}")
    console.print("doc_drift_audit_report_only=true")


@consistency_app.command("audit-stale-current-claims")
def consistency_audit_stale_current_claims(
    strict: bool = typer.Option(False, "--strict", help="Return failure on error-severity stale current claims."),
    report_only: bool = typer.Option(False, "--report-only", help="Report findings without failing on errors."),
    out: Path | None = typer.Option(None, "--out", help="Generated JSON report path."),
    expected_latest_stage: str | None = typer.Option(None, "--expected-latest-stage"),
    expected_next_stage: str | None = typer.Option(None, "--expected-next-stage"),
) -> None:
    """Audit tracked text-like files for stale current/latest/next-stage claims."""

    from libreprimus.doc_staleness.stale_current_claims import audit_repository, write_report

    report = audit_repository(
        expected_latest_stage=expected_latest_stage,
        expected_next_stage=expected_next_stage,
    )
    if out is not None:
        output_path = _resolve_output_path(out)
        write_report(output_path, report)
        console.print(f"stale_current_claim_report={output_path}")
    console.print(f"stale_current_scanned_paths={report.scanned_path_count}")
    console.print(f"stale_current_skipped_paths={report.skipped_path_count}")
    console.print(f"stale_current_finding_count={report.finding_count}")
    console.print(f"stale_current_error_count={report.error_count}")
    console.print(f"stale_current_warning_count={report.warning_count}")
    console.print(f"stale_current_suppression_error_count={report.suppression_error_count}")
    for finding in report.findings:
        style = "red" if finding.severity == "error" else "yellow"
        text = (
            f"{finding.severity}:{finding.claim_type}:{finding.path}:{finding.line}: "
            f"{_console_safe(finding.matched_text)}"
        )
        console.print(text, style=style, markup=False, highlight=False)
    if strict and not report_only and report.error_count:
        raise typer.Exit(1)
    console.print("stale_current_claim_audit_valid=true")


@consistency_app.command("audit-doc-drift-deep")
def consistency_audit_doc_drift_deep(
    strict: bool = typer.Option(False, "--strict", help="Return failure on error-severity stale current claims."),
    out: Path | None = typer.Option(None, "--out", help="Generated JSON report path."),
) -> None:
    """Run the Stage 5EG deep stale-current-claim audit."""

    from libreprimus.doc_staleness.stale_current_claims import audit_repository, write_report

    report = audit_repository()
    if out is not None:
        output_path = _resolve_output_path(out)
        write_report(output_path, report)
        console.print(f"stale_current_claim_report={output_path}")
    console.print(f"stale_current_finding_count={report.finding_count}")
    console.print(f"stale_current_error_count={report.error_count}")
    if strict and report.error_count:
        raise typer.Exit(1)
    console.print("doc_drift_deep_audit_valid=true")


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(consistency_app, name="consistency")


def _console_safe(text: str) -> str:
    return text.encode("ascii", "backslashreplace").decode("ascii")
