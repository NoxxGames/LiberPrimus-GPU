from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

import libreprimus.cli as cli
from libreprimus.consistency.models import (
    ConsistencyCheckSuiteResult,
    fail_result,
    pass_result,
    warning_result,
)
from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]


def test_consistency_check_all_works() -> None:
    result = CliRunner().invoke(app, ["consistency", "check-all", "--allow-warnings"])

    assert result.exit_code == 0, result.output
    assert "Consistency checks OK" in result.output


def test_consistency_individual_subcommands_work() -> None:
    runner = CliRunner()
    for command in [
        "check-registry",
        "check-manifests",
        "check-schemas",
        "check-docs",
        "check-ignored-outputs",
        "check-result-store",
    ]:
        args = ["consistency", command, "--allow-warnings"]
        if command == "check-result-store":
            args.insert(2, "--allow-missing-generated")
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output


def test_consistency_out_writes_summary(tmp_path: Path) -> None:
    out = tmp_path / "summary.json"
    result = CliRunner().invoke(
        app,
        ["consistency", "check-all", "--out", str(out), "--allow-warnings"],
    )

    assert result.exit_code == 0, result.output
    assert out.is_file()
    assert "summary=" in result.output


def test_consistency_errors_return_nonzero(monkeypatch) -> None:
    def fake_suite(*args, **kwargs):
        return ConsistencyCheckSuiteResult("fake", [fail_result("group", "check", "bad")])

    monkeypatch.setattr(cli, "run_consistency_suite", fake_suite)
    result = CliRunner().invoke(app, ["consistency", "check-all", "--allow-warnings"])

    assert result.exit_code != 0


def test_consistency_warnings_allowed(monkeypatch) -> None:
    def fake_suite(*args, **kwargs):
        return ConsistencyCheckSuiteResult(
            "fake",
            [pass_result("group", "pass", "ok"), warning_result("group", "warn", "warn")],
        )

    monkeypatch.setattr(cli, "run_consistency_suite", fake_suite)
    result = CliRunner().invoke(app, ["consistency", "check-all", "--allow-warnings"])

    assert result.exit_code == 0, result.output


def test_ci_workflow_runs_consistency_checks() -> None:
    workflow = (REPO / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "consistency check-all --allow-warnings" in workflow
    assert "consistency check-result-store --allow-missing-generated --allow-warnings" in workflow


def test_consistency_scripts_exist() -> None:
    assert (REPO / "scripts/ci/run-consistency-checks.ps1").is_file()
    assert (REPO / "scripts/ci/run-consistency-checks.sh").is_file()
