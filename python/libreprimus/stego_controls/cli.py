"""Typer CLI for Stage 5AP stego-control readiness."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .outguess_controls import GUARDRAIL_PATH, MATRIX_PATH, POLICY_PATH, RESULTS_DIR, build_guardrail, build_outguess_policy, build_positive_control_matrix
from .outguess_fixtures import HISTORICAL_PATH, build_historical_fixture_readiness
from .outguess_toolchain import detect_outguess_toolchain
from .validation import validate_stage5ap_outguess

TOOLCHAIN_PATH = Path("data/stego/stage5ap-outguess-toolchain-readiness.yaml")

console = Console()
app = typer.Typer(help="Stage 5AP stego-control readiness commands.", no_args_is_help=True)


@app.command("build-stage5ap-outguess-toolchain-readiness")
def build_stage5ap_outguess_toolchain_readiness_command(out: Path = typer.Option(TOOLCHAIN_PATH)) -> None:
    record = detect_outguess_toolchain(out=out)
    build_outguess_policy(out=POLICY_PATH)
    console.print(f"toolchain_state={record['toolchain_state']}")
    console.print(f"tool_available={str(record['tool_available']).lower()}")


@app.command("build-stage5ap-outguess-positive-control-matrix")
def build_stage5ap_outguess_positive_control_matrix_command(
    toolchain: Path = typer.Option(TOOLCHAIN_PATH),
    out: Path = typer.Option(MATRIX_PATH),
    historical_out: Path = typer.Option(HISTORICAL_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    matrix = build_positive_control_matrix(toolchain=toolchain, out=out, results_dir=results_dir)
    historical = build_historical_fixture_readiness(out=historical_out, results_dir=results_dir)
    console.print(f"matrix_record_count={matrix['matrix_record_count']}")
    console.print(f"historical_fixture_count={historical['historical_fixture_count']}")


@app.command("build-stage5ap-outguess-historical-fixture-readiness")
def build_stage5ap_outguess_historical_fixture_readiness_command(
    out: Path = typer.Option(HISTORICAL_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    record = build_historical_fixture_readiness(out=out, results_dir=results_dir)
    console.print(f"historical_fixture_ready_count={record['historical_fixture_ready_count']}")


@app.command("build-stage5ap-outguess-guardrail")
def build_stage5ap_outguess_guardrail_command(out: Path = typer.Option(GUARDRAIL_PATH)) -> None:
    record = build_guardrail(out=out)
    console.print(f"guardrail_status={record['guardrail_status']}")


@app.command("validate-stage5ap-outguess")
def validate_stage5ap_outguess_command(
    policy: Path = typer.Option(POLICY_PATH),
    toolchain: Path = typer.Option(TOOLCHAIN_PATH),
    matrix: Path = typer.Option(MATRIX_PATH),
    historical: Path = typer.Option(HISTORICAL_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
) -> None:
    counts, errors = validate_stage5ap_outguess(
        policy=policy,
        toolchain=toolchain,
        matrix=matrix,
        historical=historical,
        guardrail=guardrail,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("stego_controls_stage5ap_outguess_valid=true")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="stego-controls")
