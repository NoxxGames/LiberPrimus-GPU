from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.experiment_execution.cpu_runner import run_cpu_execution_manifest
from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/cpu-execution/stage2f-blocked-unsolved-example.yaml"
OUT_DIR = REPO / "experiments/results/cpu-execution/stage2f"


def test_blocked_unsolved_manifest_fails_validation() -> None:
    with pytest.raises(ValueError, match="future_unsolved_page_candidate"):
        load_cpu_execution_manifest(MANIFEST)


def test_blocked_unsolved_manifest_cannot_run() -> None:
    with pytest.raises(ValueError, match="future_unsolved_page_candidate"):
        run_cpu_execution_manifest(MANIFEST, out_dir=OUT_DIR)


def test_cli_failure_explains_block() -> None:
    result = CliRunner().invoke(app, ["execution", "validate", "--manifest", str(MANIFEST)])

    assert result.exit_code != 0
    assert "future_unsolved_page_candidate" in result.output

