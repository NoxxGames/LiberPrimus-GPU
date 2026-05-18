from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_discord_ingest_cli_scan_validate_and_export(tmp_path: Path) -> None:
    source = tmp_path / "discord"
    source.mkdir()
    (source / "chat.html").write_text(
        '<a href="https://github.com/example/repo">repo</a> prime p56 3301 failed',
        encoding="utf-8",
    )
    out = tmp_path / "out"

    scan = CliRunner().invoke(
        app,
        [
            "discord-ingest",
            "scan",
            "--source-dir",
            str(source),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
    )
    assert scan.exit_code == 0, scan.output
    assert "html_file_count=1" in scan.output

    validate = CliRunner().invoke(
        app,
        ["discord-ingest", "validate-results", "--results-dir", str(out)],
    )
    assert validate.exit_code == 0, validate.output
    assert "Discord ingestion results OK" in validate.output

    export = CliRunner().invoke(
        app,
        [
            "discord-ingest",
            "export-aggregate",
            "--results-dir",
            str(out),
            "--archive-out",
            str(tmp_path / "archive.yaml"),
            "--observation-out",
            str(tmp_path / "observation.yaml"),
        ],
    )
    assert export.exit_code == 0, export.output
    assert "link_count=1" in export.output


def test_discord_ingest_cli_allow_missing(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "discord-ingest",
            "scan",
            "--source-dir",
            str(tmp_path / "missing"),
            "--out-dir",
            str(tmp_path / "out"),
            "--allow-missing",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "html_file_count=0" in result.output
