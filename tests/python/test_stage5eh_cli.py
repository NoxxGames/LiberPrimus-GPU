from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app
from test_stage5eh_common import stage5eh_data


def test_stage5eh_cli_validate_and_summary_work() -> None:
    stage5eh_data("summary")

    runner = CliRunner()
    validate = runner.invoke(app, ["token-block", "validate-stage5eh"])
    summary = runner.invoke(app, ["token-block", "stage5eh-summary"])

    assert validate.exit_code == 0, validate.output
    assert "token_block_stage5eh_valid=true" in validate.output
    assert summary.exit_code == 0
    assert "recommended_next_stage_id=stage-5ei" in summary.output


def test_stage5eh_focused_cli_commands_work() -> None:
    runner = CliRunner()
    for command in [
        "validate-stage5eh-lag5-inventory",
        "validate-stage5eh-lp-outguessed-inventory",
        "validate-stage5eh-outguess03-context",
        "validate-stage5eh-byte-string-crosslinks",
        "validate-stage5eh-page54-55-red-number-context",
        "validate-stage5eh-page13-f5-context",
        "validate-stage5eh-number-fact-overlays",
        "validate-stage5eh-source-browser-loadability",
        "validate-stage5eh-current-truth-doc-staleness",
        "validate-stage5eh-sidecar-gates",
        "validate-stage5eh-handoff-continuity",
        "validate-stage5eh-governance-scope",
    ]:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
