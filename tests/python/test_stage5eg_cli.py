from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app
from test_stage5eg_common import ensure_stage5eg_built


def test_stage5eg_cli_validate_and_summary_work() -> None:
    ensure_stage5eg_built()

    runner = CliRunner()
    validate = runner.invoke(app, ["token-block", "validate-stage5eg"])
    summary = runner.invoke(app, ["token-block", "stage5eg-summary"])

    assert validate.exit_code == 0, validate.output
    assert "token_block_stage5eg_valid=true" in validate.output
    assert summary.exit_code == 0
    assert "recommended_next_stage_id=stage-5eh" in summary.output


def test_stale_current_claim_cli_passes_strict() -> None:
    ensure_stage5eg_built()

    runner = CliRunner()
    result = runner.invoke(app, ["consistency", "audit-stale-current-claims", "--strict"])

    assert result.exit_code == 0, result.output
    assert "stale_current_error_count=0" in result.output
