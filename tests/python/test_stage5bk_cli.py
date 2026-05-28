from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bk_validate_cli_reports_success() -> None:
    result = CliRunner().invoke(app, ["historical-route", "validate-stage5bk"])
    assert result.exit_code == 0, result.output
    assert "stage5bk_valid=true" in result.output
    assert "validation_error_count=0" in result.output


def test_stage5bk_summary_cli_reports_counts() -> None:
    result = CliRunner().invoke(app, ["historical-route", "stage5bk-summary"])
    assert result.exit_code == 0, result.output
    assert "stage_id=stage-5bk" in result.output
    assert "iddqd_v2_byte_string_count=4" in result.output


def test_stage5bk_build_commands_are_registered() -> None:
    for command in [
        "locate-stage5bk-iddqd-v2",
        "inventory-stage5bk-iddqd-v2",
        "build-stage5bk-iddqd-v2-source-lock",
        "build-stage5bk-planning-constraints",
        "build-stage5bk-token-block-impact",
        "build-stage5bk-summary",
        "stage5bk-build",
    ]:
        result = CliRunner().invoke(app, ["historical-route", command, "--help"])
        assert result.exit_code == 0, result.output
