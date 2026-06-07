from __future__ import annotations

import importlib.util
import subprocess
import sys

import pytest

from test_stage5dq_common import ROOT


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def test_operator_console_cli_validate_and_summary() -> None:
    validate = run_cli("operator-console", "validate-source-index").stdout
    assert "operator_console_source_index_valid=true" in validate

    manual = run_cli("operator-console", "validate-manual-entries").stdout
    assert "operator_console_manual_entries_valid=true" in manual

    summary = run_cli("operator-console", "summary").stdout
    assert "entries_loaded=" in summary
    assert "chatgpt_context=" in summary


def test_source_browser_alias_validate_index() -> None:
    output = run_cli("source-browser", "validate-index").stdout

    assert "source_browser_index_valid=true" in output


@pytest.mark.skipif(
    importlib.util.find_spec("PySide6") is not None,
    reason="operator-console run launches the GUI when optional dependencies are installed",
)
def test_operator_console_run_fails_gracefully_without_gui_dependency() -> None:
    result = run_cli("operator-console", "run", check=False)

    if result.returncode == 0:
        assert result.stdout or result.stderr
    else:
        assert "pip install -e .[gui]" in (result.stdout + result.stderr)
