from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage3v_cli_detect_works_with_missing_tool(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "stego",
            "outguess-detect",
            "--outguess-path",
            str(tmp_path / "missing"),
            "--out-dir",
            str(tmp_path / "out"),
            "--allow-missing-tool",
        ],
    )

    assert result.exit_code == 0
    assert "tool_available=false" in result.output


def test_stage3v_cli_validate_manifest() -> None:
    result = CliRunner().invoke(
        app,
        [
            "stego",
            "outguess-validate-manifest",
            "--manifest",
            "experiments/manifests/stego/outguess-regression-v1.yaml",
            "--artifacts",
            "data/observations/stego/outguess-artifacts-v0.yaml",
        ],
    )

    assert result.exit_code == 0
    assert "outguess_manifest_valid=true" in result.output


def test_stage3v_cli_run_missing_tool_skips(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "stego",
            "outguess-run",
            "--manifest",
            "experiments/manifests/stego/outguess-regression-v1.yaml",
            "--artifacts",
            "data/observations/stego/outguess-artifacts-v0.yaml",
            "--outguess-path",
            str(tmp_path / "missing"),
            "--out-dir",
            str(tmp_path / "out"),
            "--allow-missing-tool",
            "--allow-missing-assets",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0
    assert "tool_available=false" in result.output
    assert "skipped_tool_missing_count=6" in result.output
