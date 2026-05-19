from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4l_observation_promotion_cli_build_validate_summary(tmp_path) -> None:
    out_dir = tmp_path / "out"
    ledger = tmp_path / "ledger.yaml"
    readiness = tmp_path / "readiness.yaml"
    blockers = tmp_path / "blockers.yaml"
    manifests = tmp_path / "manifests.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    build = runner.invoke(
        app,
        [
            "observation-promotion",
            "build",
            "--out-dir",
            str(out_dir),
            "--ledger-out",
            str(ledger),
            "--readiness-out",
            str(readiness),
            "--blockers-out",
            str(blockers),
            "--manifest-readiness-out",
            str(manifests),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert build.exit_code == 0, build.output
    assert "ledger_records_created=96" in build.output

    validate = runner.invoke(
        app,
        [
            "observation-promotion",
            "validate",
            "--ledger",
            str(ledger),
            "--readiness",
            str(readiness),
            "--blockers",
            str(blockers),
            "--manifest-readiness",
            str(manifests),
            "--summary",
            str(summary),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "observation_promotion_valid=true" in validate.output

    report = runner.invoke(app, ["observation-promotion", "summary", "--summary", str(summary)])
    assert report.exit_code == 0, report.output
    assert "ready_for_manifest_count=0" in report.output
