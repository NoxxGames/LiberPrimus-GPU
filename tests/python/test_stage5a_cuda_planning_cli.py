from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


TARGET_MANIFEST = "experiments/manifests/cuda/stage5a-cuda-target-plan.yaml"
SCAFFOLD_MANIFEST = "experiments/manifests/cuda/stage5a-cuda-parity-scaffold.yaml"
GATES_MANIFEST = "experiments/manifests/cuda/stage5a-cuda-implementation-gates.yaml"


def test_stage5a_cuda_planning_cli(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5a"
    target = tmp_path / "target.yaml"
    non_targets = tmp_path / "non-targets.yaml"
    scaffold = tmp_path / "scaffold.yaml"
    gates = tmp_path / "gates.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    target_result = runner.invoke(
        app,
        [
            "cuda-planning",
            "build-target-plan",
            "--manifest",
            TARGET_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--target-plan-out",
            str(target),
            "--non-targets-out",
            str(non_targets),
            "--allow-warnings",
        ],
    )
    assert target_result.exit_code == 0, target_result.output
    assert "ready_targets=9" in target_result.output

    scaffold_result = runner.invoke(
        app,
        [
            "cuda-planning",
            "build-parity-scaffold",
            "--manifest",
            SCAFFOLD_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--parity-scaffold-out",
            str(scaffold),
            "--allow-warnings",
        ],
    )
    assert scaffold_result.exit_code == 0, scaffold_result.output

    gate_result = runner.invoke(
        app,
        [
            "cuda-planning",
            "build-implementation-gates",
            "--manifest",
            GATES_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--implementation-gates-out",
            str(gates),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert gate_result.exit_code == 0, gate_result.output

    validate_result = runner.invoke(
        app,
        [
            "cuda-planning",
            "validate-stage5a",
            "--target-plan",
            str(target),
            "--parity-scaffold",
            str(scaffold),
            "--implementation-gates",
            str(gates),
            "--non-targets",
            str(non_targets),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate_result.exit_code == 0, validate_result.output
    assert "cuda_planning_stage5a_valid=true" in validate_result.output
