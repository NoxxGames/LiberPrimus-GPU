from typer.testing import CliRunner

from libreprimus.cli import app


def test_cli_smoke() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["smoke"])
    assert result.exit_code == 0
    assert "LiberPrimus Python Stage 0A smoke OK" in result.output
