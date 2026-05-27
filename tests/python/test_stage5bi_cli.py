from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bi_validate_cli_reports_success() -> None:
    result = CliRunner().invoke(app, ["historical-route", "stage5bi-validate"])

    assert result.exit_code == 0, result.output
    assert "stage5bi_valid=true" in result.output
    assert "validation_error_count=0" in result.output
    assert "selected_next_stage_id=stage-5bj" in result.output


def test_stage5bi_summary_cli_reports_counts() -> None:
    result = CliRunner().invoke(app, ["historical-route", "stage5bi-summary"])

    assert result.exit_code == 0, result.output
    assert "stage_id=stage-5bi" in result.output
    assert "fandom_page_triage_count=30" in result.output


def test_stage5bi_build_cli_is_deterministic() -> None:
    result = CliRunner().invoke(app, ["historical-route", "stage5bi-build"])

    assert result.exit_code == 0, result.output
    assert "stage5bi_build=true" in result.output
    assert "item_source_lock_candidate_count=18" in result.output
