from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5t_cli_round_trip_no_cuda_execution(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5t"
    inventory = tmp_path / "inventory.yaml"
    matrix = tmp_path / "matrix.yaml"
    kernels = tmp_path / "kernels.yaml"
    gaps = tmp_path / "gaps.yaml"
    benchmarks = tmp_path / "benchmarks.yaml"
    guardrails = tmp_path / "guardrails.yaml"
    decisions = tmp_path / "decisions.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()
    commands = [
        [
            "cuda-solved-family-readiness",
            "build-solved-family-inventory",
            "--solved-family-inventory-out",
            str(inventory),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-solved-family-readiness",
            "build-parity-matrix",
            "--solved-family-inventory",
            str(inventory),
            "--parity-matrix-out",
            str(matrix),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-solved-family-readiness",
            "build-kernel-readiness",
            "--parity-matrix",
            str(matrix),
            "--kernel-readiness-out",
            str(kernels),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-solved-family-readiness",
            "build-batch-abi-gaps",
            "--batch-abi-gaps-out",
            str(gaps),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-solved-family-readiness",
            "build-benchmark-readiness",
            "--benchmark-readiness-out",
            str(benchmarks),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-solved-family-readiness",
            "build-no-unsolved-guardrail",
            "--no-unsolved-guardrail-out",
            str(guardrails),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-solved-family-readiness",
            "build-next-stage-decision",
            "--batch-abi-gaps",
            str(gaps),
            "--next-stage-decision-out",
            str(decisions),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-solved-family-readiness",
            "build-summary",
            "--solved-family-inventory",
            str(inventory),
            "--parity-matrix",
            str(matrix),
            "--kernel-readiness",
            str(kernels),
            "--batch-abi-gaps",
            str(gaps),
            "--benchmark-readiness",
            str(benchmarks),
            "--no-unsolved-guardrail",
            str(guardrails),
            "--next-stage-decision",
            str(decisions),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    validate = runner.invoke(
        app,
        [
            "cuda-solved-family-readiness",
            "validate-stage5t",
            "--solved-family-inventory",
            str(inventory),
            "--parity-matrix",
            str(matrix),
            "--kernel-readiness",
            str(kernels),
            "--batch-abi-gaps",
            str(gaps),
            "--benchmark-readiness",
            str(benchmarks),
            "--no-unsolved-guardrail",
            str(guardrails),
            "--next-stage-decision",
            str(decisions),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "cuda_solved_family_readiness_stage5t_valid=true" in validate.output

    printed = runner.invoke(app, ["cuda-solved-family-readiness", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "verified_existing_cuda_parity_count=3" in printed.output


def test_stage5t_cli_keeps_stage5s_command_registered() -> None:
    result = CliRunner().invoke(app, ["gematria-expanded-cuda-result-store", "summary", "--help"])
    assert result.exit_code == 0, result.output
