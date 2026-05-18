"""Approval-gated execution CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

approval_execution_app = typer.Typer(no_args_is_help=True)


DEFAULT_STAGE2H_REQUEST_DIR = Path("experiments/proposals/stage2h")
DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR = Path("experiments/results/approval-gated-execution/stage2h")


@approval_execution_app.command("validate")
def approval_execution_validate(
    request: Path = typer.Option(..., "--request", help="Approval-gated execution request path."),
) -> None:
    """Validate a Stage 2H approval-gated execution request."""
    try:
        loaded = load_approval_execution_request(_resolve_existing_path(request, "Approval execution request"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Approval-gated execution request validation OK")
    console.print(f"request_id={loaded.request_id}")
    console.print(f"request_sha256={loaded.sha256}")
    console.print(f"execution_scope={loaded.execution_scope}")
    console.print("unsolved_execution_allowed=false")
    console.print("search_execution_enabled=false")
    console.print("candidate_generation_enabled=false")
    console.print("scoring_enabled=false")
    console.print("cuda_enabled=false")


@approval_execution_app.command("plan")
def approval_execution_plan(
    request: Path = typer.Option(..., "--request", help="Approval-gated execution request path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--out-dir",
        help="Generated approval-gated execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build an approval-gated execution plan without running it."""
    try:
        plan = build_approval_execution_plan(
            _resolve_existing_path(request, "Approval execution request"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_approval_execution_outputs(_resolve_output_path(out_dir), plan, None)
    console.print(f"plan={paths['plan']}")
    _print_approval_execution_plan_summary(plan)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)


@approval_execution_app.command("run")
def approval_execution_run(
    request: Path = typer.Option(..., "--request", help="Approval-gated execution request path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--out-dir",
        help="Generated approval-gated execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run one Stage 2H approval-gated safe request or write a blocked result."""
    try:
        plan, result = run_approval_execution_request(
            _resolve_existing_path(request, "Approval execution request"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_approval_execution_outputs(_resolve_output_path(out_dir), plan, result)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    _print_approval_execution_run_summary(plan, result)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)
    if result.execution_status in {"fail", "error"}:
        raise typer.Exit(1)


@approval_execution_app.command("stage2h-run-all")
def approval_execution_stage2h_run_all(
    request_dir: Path = typer.Option(
        DEFAULT_STAGE2H_REQUEST_DIR,
        "--request-dir",
        help="Directory containing Stage 2H approval-gated requests.",
    ),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--out-dir",
        help="Generated approval-gated execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run all Stage 2H approval-gated requests and report blocked controls."""
    resolved_request_dir = _resolve_output_path(request_dir)
    resolved_out_dir = _resolve_output_path(out_dir)
    results = []
    warning_count = 0
    for request_path in sorted(resolved_request_dir.glob("*-request.yaml")):
        try:
            plan, result = run_approval_execution_request(request_path, out_dir=resolved_out_dir)
        except (FileNotFoundError, ValueError) as error:
            console.print(f"[red]{request_path.name}: {error}[/red]")
            raise typer.Exit(1) from error
        write_approval_execution_outputs(resolved_out_dir, plan, result)
        results.append(result)
        warning_count += len(plan.warnings)
        console.print(f"{plan.request_id}={result.execution_status}")
    summary_path = write_approval_execution_summary(resolved_out_dir, results)
    console.print(f"summary={summary_path}")
    console.print(f"request_count={len(results)}")
    console.print(f"approved_synthetic_pass_count={sum(1 for item in results if item.execution_scope == 'synthetic_only' and item.execution_status == 'pass')}")
    console.print(f"approved_solved_pass_count={sum(1 for item in results if item.execution_scope == 'solved_fixture_only' and item.execution_status == 'pass')}")
    console.print(f"blocked_noop_real_count={sum(1 for item in results if item.execution_scope == 'no_op_review_only' and item.execution_status in {'blocked', 'skipped'})}")
    console.print(f"failed_count={sum(1 for item in results if item.execution_status in {'fail', 'error'})}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@approval_execution_app.command("summary")
def approval_execution_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR,
        "--results-dir",
        help="Generated approval-gated execution result directory.",
    ),
) -> None:
    """Print generated Stage 2H approval-gated execution summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_approval_execution_summary(resolved)
    records = load_approval_execution_result_records(resolved)
    for key in [
        "request_count",
        "execution_result_count",
        "pass_count",
        "fail_count",
        "blocked_count",
        "skipped_count",
        "approved_synthetic_pass_count",
        "approved_solved_pass_count",
        "search_performed_any",
        "candidate_generation_performed_any",
        "scoring_used_any",
        "cuda_used_any",
        "unsolved_execution_allowed_any",
    ]:
        value = summary.get(key, 0)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for record in records:
        console.print(f"{record['request_id']}={record['execution_status']}")


def _print_approval_execution_plan_summary(plan) -> None:
    pass_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "pass")
    fail_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "fail")
    console.print(f"plan_id={plan.plan_id}")
    console.print(f"request_id={plan.request_id}")
    console.print(f"proposal_id={plan.proposal_id}")
    console.print(f"approval_gate_status={plan.approval_gate_status}")
    console.print(f"approved_for_execution={str(plan.approved_for_execution).lower()}")
    console.print(f"execution_scope={plan.execution_scope}")
    console.print(f"safety_gate_pass_count={pass_count}")
    console.print(f"safety_gate_fail_count={fail_count}")
    console.print(f"search_execution_enabled={str(plan.search_execution_enabled).lower()}")
    console.print(f"candidate_generation_enabled={str(plan.candidate_generation_enabled).lower()}")
    console.print(f"scoring_enabled={str(plan.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(plan.cuda_enabled).lower()}")


def _print_approval_execution_run_summary(plan, result) -> None:
    _print_approval_execution_plan_summary(plan)
    console.print(f"execution_performed={str(result.execution_performed).lower()}")
    console.print(f"execution_status={result.execution_status}")
    console.print(f"underlying_execution_result_count={len(result.underlying_execution_result_ids)}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(approval_execution_app, name="approval-execution")
