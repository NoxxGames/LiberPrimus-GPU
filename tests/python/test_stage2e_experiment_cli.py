from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml"
MANIFEST_DIR = REPO / "experiments/manifests/exploratory"


def test_validate_exploratory_works() -> None:
    result = CliRunner().invoke(
        app,
        ["experiment", "validate-exploratory", "--manifest", str(MANIFEST)],
    )

    assert result.exit_code == 0, result.output
    assert "Exploratory manifest validation OK" in result.output


def test_dry_run_works_to_tmp_path(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "experiment",
            "dry-run",
            "--manifest",
            str(MANIFEST),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert (tmp_path / "stage2e-caesar-preview-dry-run-dry-run-plan.json").is_file()
    assert "candidate_count_estimate=29" in result.output


def test_stage2e_dry_run_all_works(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "experiment",
            "stage2e-dry-run-all",
            "--manifest-dir",
            str(MANIFEST_DIR),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "dry_run_plan_count=5" in result.output
    assert (tmp_path / "summary.json").is_file()


def test_safety_failure_returns_nonzero(tmp_path: Path) -> None:
    payload = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    payload["execution_enabled"] = True
    bad_manifest = tmp_path / "bad.yaml"
    bad_manifest.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    result = CliRunner().invoke(
        app,
        ["experiment", "validate-exploratory", "--manifest", str(bad_manifest)],
    )

    assert result.exit_code != 0


def test_cli_does_not_require_raw_data(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "experiment",
            "dry-run",
            "--manifest",
            str(MANIFEST),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "data/raw" not in result.output
