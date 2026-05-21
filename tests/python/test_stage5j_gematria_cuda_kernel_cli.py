from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


KERNEL_MANIFEST = "experiments/manifests/cuda/stage5j-gematria-cuda-kernel.yaml"
NO_GPU_MANIFEST = "experiments/manifests/cuda/stage5j-gematria-cuda-no-gpu-ci-skip.yaml"


def test_stage5j_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5j"
    build_dir = tmp_path / "build"
    implementation = tmp_path / "implementation.yaml"
    build_records = tmp_path / "build.yaml"
    parity = tmp_path / "parity.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "gematria-cuda-kernel",
            "build-implementation-records",
            "--manifest",
            KERNEL_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--implementation-out",
            str(implementation),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "implemented_kernel_name=gematria_mod29_shift_score_kernel" in result.output

    build_result = runner.invoke(
        app,
        [
            "gematria-cuda-kernel",
            "attempt-build",
            "--manifest",
            NO_GPU_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--build-records-out",
            str(build_records),
            "--build-dir",
            str(build_dir),
            "--skip-build",
            "--allow-warnings",
        ],
    )
    assert build_result.exit_code == 0, build_result.output
    assert "build_status=skipped_not_requested" in build_result.output

    parity_result = runner.invoke(
        app,
        [
            "gematria-cuda-kernel",
            "run-synthetic-parity",
            "--manifest",
            KERNEL_MANIFEST,
            "--build-records",
            str(build_records),
            "--out-dir",
            str(out_dir),
            "--parity-records-out",
            str(parity),
            "--build-dir",
            str(build_dir),
            "--allow-warnings",
        ],
    )
    assert parity_result.exit_code == 0, parity_result.output
    assert "parity_status=skipped_build_not_requested" in parity_result.output
    assert "gematria_cuda_synthetic_parity_verified=False" in parity_result.output

    summary_result = runner.invoke(
        app,
        [
            "gematria-cuda-kernel",
            "build-summary",
            "--implementation",
            str(implementation),
            "--build-records",
            str(build_records),
            "--parity-records",
            str(parity),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert summary_result.exit_code == 0, summary_result.output

    validate = runner.invoke(
        app,
        [
            "gematria-cuda-kernel",
            "validate-stage5j",
            "--implementation",
            str(implementation),
            "--build-records",
            str(build_records),
            "--parity-records",
            str(parity),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_cuda_kernel_stage5j_valid=true" in validate.output

    printed = runner.invoke(app, ["gematria-cuda-kernel", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "stage5k_ready=False" in printed.output
