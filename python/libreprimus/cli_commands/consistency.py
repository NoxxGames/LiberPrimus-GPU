"""Consistency CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

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




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(consistency_app, name="consistency")
