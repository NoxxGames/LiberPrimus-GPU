from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
MANIFEST_DIR = REPO / "experiments/manifests/cpu-execution"
DIRECT = MANIFEST_DIR / "stage2f-synthetic-direct-execution.yaml"
OUT_DIR = REPO / "experiments/results/cpu-execution/stage2f"


def test_execution_validate_works() -> None:
    result = CliRunner().invoke(app, ["execution", "validate", "--manifest", str(DIRECT)])

    assert result.exit_code == 0, result.output
    assert "CPU execution manifest validation OK" in result.output


def test_execution_plan_works() -> None:
    result = CliRunner().invoke(
        app,
        ["execution", "plan", "--manifest", str(DIRECT), "--out-dir", str(OUT_DIR), "--allow-warnings"],
    )

    assert result.exit_code == 0, result.output
    assert "safety_gate_fail_count=0" in result.output


def test_execution_run_works_on_synthetic_direct() -> None:
    result = CliRunner().invoke(
        app,
        ["execution", "run", "--manifest", str(DIRECT), "--out-dir", str(OUT_DIR), "--allow-warnings"],
    )

    assert result.exit_code == 0, result.output
    assert "pass_count=1" in result.output


def test_stage2f_run_all_reports_blocked_manifest() -> None:
    result = CliRunner().invoke(
        app,
        [
            "execution",
            "stage2f-run-all",
            "--manifest-dir",
            str(MANIFEST_DIR),
            "--out-dir",
            str(OUT_DIR),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "safe_manifest_count=6" in result.output
    assert "blocked_manifest_count=1" in result.output


def test_execution_summary_works() -> None:
    CliRunner().invoke(
        app,
        [
            "execution",
            "stage2f-run-all",
            "--manifest-dir",
            str(MANIFEST_DIR),
            "--out-dir",
            str(OUT_DIR),
            "--allow-warnings",
        ],
    )
    result = CliRunner().invoke(app, ["execution", "summary", "--results-dir", str(OUT_DIR)])

    assert result.exit_code == 0, result.output
    assert "result_count=6" in result.output


def test_missing_input_returns_nonzero(tmp_path: Path) -> None:
    payload = yaml.safe_load(DIRECT.read_text(encoding="utf-8"))
    del payload["synthetic_corpus_record"]["token_records"]
    bad_manifest = tmp_path / "missing-input.yaml"
    bad_manifest.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    result = CliRunner().invoke(
        app,
        ["execution", "run", "--manifest", str(bad_manifest), "--out-dir", str(OUT_DIR)],
    )

    assert result.exit_code != 0

