from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app


def test_observation_validate_visual_cli() -> None:
    result = CliRunner().invoke(
        app,
        [
            "observation",
            "validate-visual",
            "--records",
            "data/observations/visual/visual-numeric-observations-v0.yaml",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "visual_observation_count=5" in result.output


def test_observation_validate_cookies_cli() -> None:
    result = CliRunner().invoke(
        app,
        [
            "observation",
            "validate-cookies",
            "--records",
            "data/observations/web/cookie-hash-records-v0.yaml",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "cookie_hash_record_count=2" in result.output


def test_observation_summary_cli() -> None:
    result = CliRunner().invoke(
        app,
        [
            "observation",
            "summary",
            "--visual",
            "data/observations/visual/visual-numeric-observations-v0.yaml",
            "--cookies",
            "data/observations/web/cookie-hash-records-v0.yaml",
            "--sources",
            "data/observations/archive/source-archive-records-v0.yaml",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "source_record_count=12" in result.output
    assert "solve_claim=false" in result.output
