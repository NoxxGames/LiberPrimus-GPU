from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.token_block import stage5ei
from test_stage5ei_common import stage5ei_data


def test_stage5ei_cli_summary_and_validators_work() -> None:
    runner = CliRunner()

    for args in [
        ["token-block", "stage5ei-summary"],
        ["token-block", "validate-stage5ei"],
        ["token-block", "validate-stage5ei-triangle-transposition-geometry"],
        ["token-block", "validate-stage5ei-route-diagnostic-policy"],
        ["token-block", "validate-stage5ei-stage6-roadmap"],
        ["token-block", "validate-stage5ei-gate-closure"],
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output


def test_stage5ei_source_browser_loadability_is_preserved() -> None:
    payload = stage5ei_data("source_browser_loadability_summary")

    assert payload["source_browser_entries_loaded"] > 0
    assert payload["source_browser_records_scanned"] > 0
    assert payload["source_browser_validation_error_count"] == 0
    assert payload["source_browser_loadability_preserved"] is True


def test_stage5ei_handoff_is_ignored_noncommit_policy() -> None:
    payload = stage5ei_data("handoff_noncommit_proof")

    assert payload["completion_summary_path"] == "codex-output/stage5ei-codex-completion.md"
    assert payload["completion_summary_committed"] is False
    assert payload["codex_output_root_ignored"] is True
    assert stage5ei.validate_stage5ei_handoff().ok

