from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage3y_research_synthesis_validate_cli_works() -> None:
    result = CliRunner().invoke(
        app,
        [
            "research-synthesis",
            "validate",
            "--data-dir",
            "data/research",
            "--staged-plan",
            "docs/roadmap/staged-plan.md",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "research_synthesis_valid=true" in result.output


def test_stage3y_research_synthesis_summary_cli_works() -> None:
    result = CliRunner().invoke(app, ["research-synthesis", "summary", "--data-dir", "data/research"])

    assert result.exit_code == 0, result.output
    assert "method_family_count=25" in result.output


def test_stage3y_research_synthesis_check_retirement_cli_works() -> None:
    result = CliRunner().invoke(
        app,
        ["research-synthesis", "check-retirement", "--data-dir", "data/research", "--method-family", "caesar_affine"],
    )

    assert result.exit_code == 0, result.output
    assert "method_family_id=caesar_affine" in result.output
    assert "retirement_record=true" in result.output
