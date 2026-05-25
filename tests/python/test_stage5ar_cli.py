from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.token_block.cli import app


def test_stage5ar_validate_cli_works_on_committed_records() -> None:
    result = CliRunner().invoke(app, ["validate-stage5ar"])
    assert result.exit_code == 0, result.output
    assert "token_block_stage5ar_valid=true" in result.output
    assert "token_pixel_coordinate_records=256" in result.output
