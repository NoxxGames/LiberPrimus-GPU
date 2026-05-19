from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4k_source_lock_cli_build_validate_summary_and_allowlist(tmp_path) -> None:
    out_dir = tmp_path / "out"
    cache_dir = tmp_path / "cache"
    snapshots = tmp_path / "snapshots.yaml"
    fetches = tmp_path / "fetches.yaml"
    copyrights = tmp_path / "copyrights.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    build = runner.invoke(
        app,
        [
            "source-lock-snapshots",
            "build",
            "--out-dir",
            str(out_dir),
            "--cache-dir",
            str(cache_dir),
            "--snapshot-records-out",
            str(snapshots),
            "--fetch-records-out",
            str(fetches),
            "--copyright-records-out",
            str(copyrights),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert build.exit_code == 0, build.output
    assert "sources_considered=" in build.output

    validate = runner.invoke(
        app,
        [
            "source-lock-snapshots",
            "validate",
            "--snapshot-records",
            str(snapshots),
            "--fetch-records",
            str(fetches),
            "--copyright-records",
            str(copyrights),
            "--summary",
            str(summary),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "source_lock_snapshots_valid=true" in validate.output

    report = runner.invoke(app, ["source-lock-snapshots", "summary", "--summary", str(summary)])
    assert report.exit_code == 0, report.output
    assert "committed_small_text_snapshots=0" in report.output

    allowlist = runner.invoke(app, ["source-lock-snapshots", "list-allowlist"])
    assert allowlist.exit_code == 0, allowlist.output
    assert "allowlisted_domain=github.com" in allowlist.output
