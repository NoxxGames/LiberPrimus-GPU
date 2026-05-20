from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


HARNESS_MANIFEST = "experiments/manifests/cuda/stage5b-cuda-parity-harness-plan.yaml"
BACKEND_MANIFEST = "experiments/manifests/cuda/stage5b-cuda-backend-capability.yaml"
MATRIX_MANIFEST = "experiments/manifests/cuda/stage5b-future-kernel-parity-matrix.yaml"


def test_stage5b_cuda_parity_cli_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5b"
    harness = tmp_path / "harness.yaml"
    fixtures = tmp_path / "fixtures.yaml"
    backend = tmp_path / "backend.yaml"
    matrix = tmp_path / "matrix.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    harness_result = runner.invoke(
        app,
        [
            "cuda-parity",
            "build-harness-plan",
            "--manifest",
            HARNESS_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--harness-plan-out",
            str(harness),
            "--parity-fixtures-out",
            str(fixtures),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert harness_result.exit_code == 0, harness_result.output
    assert "ready_for_future_kernel=9" in harness_result.output

    backend_result = runner.invoke(
        app,
        [
            "cuda-parity",
            "build-backend-capability",
            "--manifest",
            BACKEND_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--backend-capability-out",
            str(backend),
            "--allow-missing-cuda",
            "--allow-warnings",
        ],
    )
    assert backend_result.exit_code == 0, backend_result.output
    assert "cuda_hardware_required=false" in backend_result.output

    matrix_result = runner.invoke(
        app,
        [
            "cuda-parity",
            "build-future-kernel-matrix",
            "--manifest",
            MATRIX_MANIFEST,
            "--harness-plan",
            str(harness),
            "--parity-fixtures",
            str(fixtures),
            "--backend-capability",
            str(backend),
            "--out-dir",
            str(out_dir),
            "--future-kernel-matrix-out",
            str(matrix),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert matrix_result.exit_code == 0, matrix_result.output

    validate_result = runner.invoke(
        app,
        [
            "cuda-parity",
            "validate-stage5b",
            "--harness-plan",
            str(harness),
            "--parity-fixtures",
            str(fixtures),
            "--backend-capability",
            str(backend),
            "--future-kernel-matrix",
            str(matrix),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate_result.exit_code == 0, validate_result.output
    assert "cuda_parity_stage5b_valid=true" in validate_result.output

    summary_result = runner.invoke(app, ["cuda-parity", "summary", "--summary", str(summary)])
    assert summary_result.exit_code == 0, summary_result.output
    assert "future_kernel_matrix_records=9" in summary_result.output
