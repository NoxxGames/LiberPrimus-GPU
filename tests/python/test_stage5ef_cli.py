from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app
from test_stage5ef_common import ensure_stage5ef_built


def test_stage5ef_cli_validate_and_summary_work() -> None:
    ensure_stage5ef_built()

    runner = CliRunner()
    validate = runner.invoke(app, ["token-block", "validate-stage5ef"])
    summary = runner.invoke(app, ["token-block", "stage5ef-summary"])

    assert validate.exit_code == 0
    assert "token_block_stage5ef_valid=true" in validate.output
    assert summary.exit_code == 0
    assert "recommended_next_stage_id=stage-5eg" in summary.output


def test_stage5ef_consistency_cli_checks_work() -> None:
    ensure_stage5ef_built()

    runner = CliRunner()
    authority = runner.invoke(app, ["consistency", "check-current-truth-authority"])
    policy = runner.invoke(app, ["consistency", "check-doc-update-policy"])

    assert authority.exit_code == 0
    assert "current_truth_authority_valid=true" in authority.output
    assert policy.exit_code == 0
    assert "doc_update_policy_valid=true" in policy.output
