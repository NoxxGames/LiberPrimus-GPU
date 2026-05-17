from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
STAGE2H = REPO / "experiments/proposals/stage2h"
SYNTHETIC_REQUEST = STAGE2H / "stage2h-approved-synthetic-direct-request.yaml"
NOOP_REQUEST = STAGE2H / "stage2h-noop-real-request.yaml"


def test_validate_works() -> None:
    result = CliRunner().invoke(app, ["approval-execution", "validate", "--request", str(SYNTHETIC_REQUEST)])

    assert result.exit_code == 0, result.output
    assert "Approval-gated execution request validation OK" in result.output


def test_plan_works(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        ["approval-execution", "plan", "--request", str(SYNTHETIC_REQUEST), "--out-dir", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output
    assert "approval_gate_status=pass" in result.output


def test_run_works_for_synthetic_direct(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        ["approval-execution", "run", "--request", str(SYNTHETIC_REQUEST), "--out-dir", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output
    assert "execution_status=pass" in result.output


def test_stage2h_run_all_works(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "approval-execution",
            "stage2h-run-all",
            "--request-dir",
            str(STAGE2H),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "request_count=3" in result.output
    assert "approved_synthetic_pass_count=1" in result.output
    assert "blocked_noop_real_count=1" in result.output


def test_noop_real_request_is_blocked(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        ["approval-execution", "run", "--request", str(NOOP_REQUEST), "--out-dir", str(tmp_path), "--allow-warnings"],
    )

    assert result.exit_code == 0, result.output
    assert "approval_gate_status=blocked" in result.output
    assert "execution_status=blocked" in result.output


def test_summary_works(tmp_path: Path) -> None:
    CliRunner().invoke(
        app,
        [
            "approval-execution",
            "stage2h-run-all",
            "--request-dir",
            str(STAGE2H),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )
    result = CliRunner().invoke(app, ["approval-execution", "summary", "--results-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "request_count=3" in result.output

