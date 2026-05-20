from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


CONTRACT_MANIFEST = "experiments/manifests/cuda/stage5e-first-kernel-contract.yaml"
ADAPTER_MANIFEST = "experiments/manifests/cuda/stage5e-adapter-selection.yaml"
READINESS_MANIFEST = "experiments/manifests/cuda/stage5e-implementation-readiness.yaml"


def test_stage5e_cuda_kernel_contract_cli_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5e"
    contract = tmp_path / "contract.yaml"
    adapter = tmp_path / "adapter.yaml"
    native = tmp_path / "native.yaml"
    readiness = tmp_path / "readiness.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    selected = runner.invoke(
        app,
        [
            "cuda-kernel-contract",
            "select-first-kernel",
            "--manifest",
            CONTRACT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--contract-out",
            str(contract),
            "--adapter-selection-out",
            str(adapter),
            "--allow-warnings",
        ],
    )
    assert selected.exit_code == 0, selected.output
    assert "selected_kernel_id=shift_score_kernel" in selected.output

    native_map = runner.invoke(
        app,
        [
            "cuda-kernel-contract",
            "build-native-parity-map",
            "--manifest",
            ADAPTER_MANIFEST,
            "--contract",
            str(contract),
            "--out-dir",
            str(out_dir),
            "--native-parity-out",
            str(native),
            "--allow-warnings",
        ],
    )
    assert native_map.exit_code == 0, native_map.output
    assert "native_parity_mapped=true" in native_map.output

    readiness_result = runner.invoke(
        app,
        [
            "cuda-kernel-contract",
            "build-readiness",
            "--manifest",
            READINESS_MANIFEST,
            "--contract",
            str(contract),
            "--native-parity",
            str(native),
            "--out-dir",
            str(out_dir),
            "--readiness-out",
            str(readiness),
            "--allow-warnings",
        ],
    )
    assert readiness_result.exit_code == 0, readiness_result.output
    assert "implementation_readiness_status=ready_for_stage5f_synthetic_only_implementation" in readiness_result.output

    build_summary = runner.invoke(
        app,
        [
            "cuda-kernel-contract",
            "build-summary",
            "--contract",
            str(contract),
            "--adapter-selection",
            str(adapter),
            "--native-parity",
            str(native),
            "--readiness",
            str(readiness),
            "--out-dir",
            str(out_dir),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert build_summary.exit_code == 0, build_summary.output

    validate = runner.invoke(
        app,
        [
            "cuda-kernel-contract",
            "validate-stage5e",
            "--contract",
            str(contract),
            "--adapter-selection",
            str(adapter),
            "--native-parity",
            str(native),
            "--readiness",
            str(readiness),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "cuda_kernel_contract_stage5e_valid=true" in validate.output

    printed = runner.invoke(app, ["cuda-kernel-contract", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "selected_target_id=stage5a-caesar_mod29-cuda-target" in printed.output
