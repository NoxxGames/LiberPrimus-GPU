from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4j_observation_review_cli_build_validate_summary_and_paths(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    policy = tmp_path / "policy.yaml"
    decisions = tmp_path / "decisions.yaml"
    promotions = tmp_path / "promotions.yaml"
    quarantine = tmp_path / "quarantine.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    build = runner.invoke(
        app,
        [
            "observation-review",
            "build",
            "--out-dir",
            str(out_dir),
            "--policy-out",
            str(policy),
            "--decisions-out",
            str(decisions),
            "--promotions-out",
            str(promotions),
            "--quarantine-out",
            str(quarantine),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert build.exit_code == 0, build.output
    assert "decisions_created=96" in build.output

    validate = runner.invoke(
        app,
        [
            "observation-review",
            "validate",
            "--policy",
            str(policy),
            "--decisions",
            str(decisions),
            "--promotions",
            str(promotions),
            "--quarantine",
            str(quarantine),
            "--summary",
            str(summary),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "observation_review_valid=true" in validate.output

    report = runner.invoke(app, ["observation-review", "summary", "--summary", str(summary)])
    assert report.exit_code == 0, report.output
    assert "promoted_to_manifest_count=0" in report.output

    paths = runner.invoke(app, ["observation-review", "check-paths", "--repo-root", "."])
    assert paths.exit_code == 0, paths.output
    assert "path_sanitisation_valid=true" in paths.output
