"""CPU execution CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

execution_app = typer.Typer(no_args_is_help=True)


DEFAULT_CPU_EXECUTION_MANIFEST_DIR = Path("experiments/manifests/cpu-execution")
DEFAULT_STAGE2F_EXECUTION_DIR = Path("experiments/results/cpu-execution/stage2f")


@execution_app.command("validate")
def execution_validate(
    manifest: Path = typer.Option(..., "--manifest", help="CPU execution manifest path."),
) -> None:
    """Validate a Stage 2F CPU execution manifest."""
    try:
        loaded = load_cpu_execution_manifest(_resolve_existing_path(manifest, "CPU execution manifest"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("CPU execution manifest validation OK")
    console.print(f"manifest_id={loaded.manifest_id}")
    console.print(f"manifest_sha256={loaded.sha256}")
    console.print(f"execution_scope={loaded.execution_scope}")
    console.print(f"unsolved_execution_allowed={str(loaded.payload['unsolved_execution_allowed']).lower()}")
    console.print(f"search_execution_enabled={str(loaded.payload['search_execution_enabled']).lower()}")
    console.print(f"candidate_generation_enabled={str(loaded.payload['candidate_generation_enabled']).lower()}")
    console.print(f"scoring_enabled={str(loaded.payload['scoring_enabled']).lower()}")
    console.print(f"cuda_enabled={str(loaded.payload['cuda_enabled']).lower()}")


@execution_app.command("plan")
def execution_plan(
    manifest: Path = typer.Option(..., "--manifest", help="CPU execution manifest path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--out-dir",
        help="Generated CPU execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Build a safety-checked CPU execution plan without running it."""
    try:
        plan = build_execution_plan(
            _resolve_existing_path(manifest, "CPU execution manifest"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_execution_outputs(
        _resolve_output_path(out_dir),
        plan,
        [],
        {"record_type": "cpu_execution_summary", "manifest_id": plan.manifest_id, "result_count": 0},
    )
    console.print(f"execution_plan={paths['execution_plan']}")
    _print_execution_plan_summary(plan)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)


@execution_app.command("run")
def execution_run(
    manifest: Path = typer.Option(..., "--manifest", help="CPU execution manifest path."),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--out-dir",
        help="Generated CPU execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run one safe Stage 2F CPU execution manifest."""
    try:
        plan, results, summary = run_cpu_execution_manifest(
            _resolve_existing_path(manifest, "CPU execution manifest"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = write_execution_outputs(_resolve_output_path(out_dir), plan, results, summary)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    _print_execution_run_summary(plan, summary)
    if plan.warnings and not allow_warnings:
        raise typer.Exit(1)
    if summary.get("fail_count") or summary.get("error_count"):
        raise typer.Exit(1)


@execution_app.command("stage2f-run-all")
def execution_stage2f_run_all(
    manifest_dir: Path = typer.Option(
        DEFAULT_CPU_EXECUTION_MANIFEST_DIR,
        "--manifest-dir",
        help="Directory containing Stage 2F CPU execution manifests.",
    ),
    out_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--out-dir",
        help="Generated CPU execution output directory.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run all safe Stage 2F CPU execution manifests and report blocked controls."""
    resolved_manifest_dir = _resolve_output_path(manifest_dir)
    resolved_out_dir = _resolve_output_path(out_dir)
    summaries = []
    blocked_count = 0
    safe_count = 0
    warning_count = 0
    for manifest in sorted(resolved_manifest_dir.glob("*.yaml")):
        text = manifest.read_text(encoding="utf-8")
        is_expected_failure = "expected_validation_status: fail" in text
        try:
            plan, results, summary = run_cpu_execution_manifest(manifest, out_dir=resolved_out_dir)
        except (FileNotFoundError, ValueError) as error:
            if is_expected_failure:
                blocked_count += 1
                console.print(f"{manifest.name}=blocked")
                console.print(f"{manifest.name}_reason={error}")
                continue
            console.print(f"[red]{manifest}: {error}[/red]")
            raise typer.Exit(1) from error
        if is_expected_failure:
            console.print(f"[red]{manifest}: expected failure unexpectedly ran.[/red]")
            raise typer.Exit(1)
        write_execution_outputs(resolved_out_dir, plan, results, summary)
        summaries.append(summary)
        safe_count += 1
        warning_count += len(plan.warnings)
        console.print(f"{plan.manifest_id}=pass_count:{summary.get('pass_count')}")
    summary_path = write_execution_aggregate_summary(resolved_out_dir, summaries)
    console.print(f"summary={summary_path}")
    console.print(f"safe_manifest_count={safe_count}")
    console.print(f"blocked_manifest_count={blocked_count}")
    console.print(f"execution_result_count={sum(int(item.get('result_count', 0)) for item in summaries)}")
    console.print(f"pass_count={sum(int(item.get('pass_count', 0)) for item in summaries)}")
    console.print(f"fail_count={sum(int(item.get('fail_count', 0)) for item in summaries)}")
    console.print(f"error_count={sum(int(item.get('error_count', 0)) for item in summaries)}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@execution_app.command("summary")
def execution_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2F_EXECUTION_DIR,
        "--results-dir",
        help="Generated CPU execution result directory.",
    ),
) -> None:
    """Print generated Stage 2F execution summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_execution_summary(resolved)
    records = load_execution_result_records(resolved)
    for key in [
        "manifest_count",
        "result_count",
        "pass_count",
        "fail_count",
        "error_count",
        "skipped_count",
        "search_performed_any",
        "candidate_generation_performed_any",
        "scoring_used_any",
        "cuda_used_any",
        "unsolved_execution_allowed_any",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for record in records:
        console.print(f"{record['manifest_id']}={record['match_status']}")


def _print_execution_plan_summary(plan) -> None:
    pass_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "pass")
    fail_count = sum(1 for gate in plan.safety_gate_results if gate.get("status") == "fail")
    console.print(f"plan_id={plan.plan_id}")
    console.print(f"manifest_id={plan.manifest_id}")
    console.print(f"execution_scope={plan.execution_scope}")
    console.print(f"safety_gate_pass_count={pass_count}")
    console.print(f"safety_gate_fail_count={fail_count}")
    console.print(f"search_execution_enabled={str(plan.search_execution_enabled).lower()}")
    console.print(f"candidate_generation_enabled={str(plan.candidate_generation_enabled).lower()}")
    console.print(f"scoring_enabled={str(plan.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(plan.cuda_enabled).lower()}")


def _print_execution_run_summary(plan, summary: dict) -> None:
    _print_execution_plan_summary(plan)
    console.print(f"result_count={summary.get('result_count')}")
    console.print(f"pass_count={summary.get('pass_count')}")
    console.print(f"fail_count={summary.get('fail_count')}")
    console.print(f"error_count={summary.get('error_count')}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(execution_app, name="execution")
