from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bj_validate_cli_reports_success() -> None:
    result = CliRunner().invoke(app, ["historical-route", "stage5bj-validate"])

    assert result.exit_code == 0, result.output
    assert "stage5bj_valid=true" in result.output
    assert "validation_error_count=0" in result.output
    assert "selected_next_stage_id=stage-5bk" in result.output


def test_stage5bj_summary_cli_reports_counts() -> None:
    result = CliRunner().invoke(app, ["historical-route", "stage5bj-summary"])

    assert result.exit_code == 0, result.output
    assert "stage_id=stage-5bj" in result.output
    assert "crosswalk_closure_record_count=12" in result.output
    assert "exact_512_hex_surface_locked_count=3" in result.output


def test_stage5bj_build_command_is_registered_without_running_it() -> None:
    result = CliRunner().invoke(app, ["historical-route", "stage5bj-build", "--help"])

    assert result.exit_code == 0, result.output
    assert "stage5bj-build" in result.output or "Usage:" in result.output
