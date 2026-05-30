from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5ca_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    commands = [
        ("validate-stage5ca-citation-contract", "token_block_stage5ca_citation_contract_valid=true"),
        (
            "validate-stage5ca-fail-closed-triggers",
            "token_block_stage5ca_fail_closed_triggers_valid=true",
        ),
        (
            "validate-stage5ca-activation-preconditions",
            "token_block_stage5ca_activation_preconditions_valid=true",
        ),
        (
            "validate-stage5ca-manifest-supersession-contract",
            "token_block_stage5ca_manifest_supersession_contract_valid=true",
        ),
        ("validate-stage5ca-sidecar-gates", "token_block_stage5ca_sidecar_gates_valid=true"),
        ("validate-stage5ca", "token_block_stage5ca_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5ca-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5ca" in summary.output
    assert "future_token_block_execution_remains_blocked=true" in summary.output
