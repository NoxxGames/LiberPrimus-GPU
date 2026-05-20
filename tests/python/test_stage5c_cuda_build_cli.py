from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


MANIFEST = "experiments/manifests/cuda/stage5c-cuda-build-device-detection.yaml"
NO_GPU_MANIFEST = "experiments/manifests/cuda/stage5c-cuda-no-gpu-ci-profile.yaml"


def test_stage5c_cuda_build_cli_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5c"
    profiles = tmp_path / "profiles.yaml"
    toolchain = tmp_path / "toolchain.yaml"
    devices = tmp_path / "devices.yaml"
    smoke = tmp_path / "smoke.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    profile_result = runner.invoke(
        app,
        [
            "cuda-build",
            "profile-toolchain",
            "--manifest",
            MANIFEST,
            "--out-dir",
            str(out_dir),
            "--profiles-out",
            str(profiles),
            "--toolchain-out",
            str(toolchain),
            "--allow-missing-cuda",
            "--allow-warnings",
        ],
    )
    assert profile_result.exit_code == 0, profile_result.output
    assert "build_profiles=3" in profile_result.output

    device_result = runner.invoke(
        app,
        [
            "cuda-build",
            "detect-device",
            "--manifest",
            MANIFEST,
            "--out-dir",
            str(out_dir),
            "--devices-out",
            str(devices),
            "--allow-no-gpu",
            "--allow-warnings",
        ],
    )
    assert device_result.exit_code == 0, device_result.output
    assert "device_records=3" in device_result.output

    smoke_result = runner.invoke(
        app,
        [
            "cuda-build",
            "smoke-build",
            "--manifest",
            NO_GPU_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--smoke-build-out",
            str(smoke),
            "--allow-missing-cuda",
            "--allow-no-gpu",
            "--allow-warnings",
        ],
    )
    assert smoke_result.exit_code == 0, smoke_result.output
    assert "smoke_test_executed=false" in smoke_result.output

    summary_result = runner.invoke(
        app,
        [
            "cuda-build",
            "build-summary",
            "--profiles",
            str(profiles),
            "--toolchain",
            str(toolchain),
            "--devices",
            str(devices),
            "--smoke-build",
            str(smoke),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert summary_result.exit_code == 0, summary_result.output

    validate_result = runner.invoke(
        app,
        [
            "cuda-build",
            "validate-stage5c",
            "--profiles",
            str(profiles),
            "--toolchain",
            str(toolchain),
            "--devices",
            str(devices),
            "--smoke-build",
            str(smoke),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate_result.exit_code == 0, validate_result.output
    assert "cuda_build_stage5c_valid=true" in validate_result.output

    summary_print = runner.invoke(app, ["cuda-build", "summary", "--summary", str(summary)])
    assert summary_print.exit_code == 0, summary_print.output
    assert "build_profile_records=3" in summary_print.output
