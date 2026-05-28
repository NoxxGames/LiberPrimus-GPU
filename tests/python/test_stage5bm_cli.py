from pathlib import Path

import pytest
from typer.testing import CliRunner

from libreprimus.cli import app

IDDQD_V2_STRING_SOURCE = Path("third_party/CiadaSolversIddqd_v2/byte-strings/byte-strings")


def test_stage5bm_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate_result = runner.invoke(app, ["token-block", "validate-stage5bm"])
    assert validate_result.exit_code == 0, validate_result.output
    assert "token_block_stage5bm_valid=true" in validate_result.output

    summary_result = runner.invoke(app, ["token-block", "stage5bm-summary"])
    assert summary_result.exit_code == 0, summary_result.output
    assert "string4_branch_membership_status=partial_branch_match" in summary_result.output


def test_stage5bm_cli_build_reconciliation_is_deterministic() -> None:
    if not IDDQD_V2_STRING_SOURCE.is_file():
        pytest.skip("local ignored iddqd-v2 String 4 source is not available")

    result = CliRunner().invoke(app, ["token-block", "build-stage5bm-string4-reconciliation"])

    assert result.exit_code == 0, result.output
    assert "string4_branch_membership_status=partial_branch_match" in result.output
    assert "string4_unsupported_position_count=1" in result.output
