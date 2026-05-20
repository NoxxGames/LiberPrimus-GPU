from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


KERNEL_MANIFEST = "experiments/manifests/cuda/stage5i-gematria-cuda-kernel-preparation.yaml"
ABI_MANIFEST = "experiments/manifests/cuda/stage5i-gematria-cuda-abi-plan.yaml"
VECTOR_MANIFEST = "experiments/manifests/cuda/stage5i-gematria-cuda-validation-vectors.yaml"


def test_stage5i_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5i"
    prep = tmp_path / "prep.yaml"
    abi = tmp_path / "abi.yaml"
    vectors = tmp_path / "vectors.yaml"
    checklist = tmp_path / "checklist.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    for args in (
        ["build-kernel-preparation", "--manifest", KERNEL_MANIFEST, "--preparation-out", str(prep)],
        ["build-abi-plan", "--manifest", ABI_MANIFEST, "--abi-plan-out", str(abi)],
        ["build-validation-vectors", "--manifest", VECTOR_MANIFEST, "--validation-vectors-out", str(vectors)],
        ["build-implementation-checklist", "--implementation-checklist-out", str(checklist)],
    ):
        result = runner.invoke(app, ["gematria-cuda-prep", *args, "--out-dir", str(out_dir), "--allow-warnings"])
        assert result.exit_code == 0, result.output

    summary_result = runner.invoke(
        app,
        [
            "gematria-cuda-prep",
            "build-summary",
            "--preparation",
            str(prep),
            "--abi-plan",
            str(abi),
            "--validation-vectors",
            str(vectors),
            "--implementation-checklist",
            str(checklist),
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
            "gematria-cuda-prep",
            "validate-stage5i",
            "--preparation",
            str(prep),
            "--abi-plan",
            str(abi),
            "--validation-vectors",
            str(vectors),
            "--implementation-checklist",
            str(checklist),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_cuda_prep_stage5i_valid=true" in validate.output
