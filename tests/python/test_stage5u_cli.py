from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5u_cli_round_trip_no_cuda_execution(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5u"
    paths = {
        "abi": tmp_path / "abi.yaml",
        "token": tmp_path / "token.yaml",
        "transform": tmp_path / "transform.yaml",
        "key": tmp_path / "key.yaml",
        "stream": tmp_path / "stream.yaml",
        "score": tmp_path / "score.yaml",
        "topk": tmp_path / "topk.yaml",
        "backend": tmp_path / "backend.yaml",
        "compat": tmp_path / "compat.yaml",
        "gap": tmp_path / "gap.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    runner = CliRunner()
    commands = [
        ["cuda-candidate-batch-abi", "build-candidate-batch-abi", "--candidate-batch-abi-out", str(paths["abi"]), "--out-dir", str(out_dir), "--allow-warnings"],
        ["cuda-candidate-batch-abi", "build-token-buffer-contract", "--token-buffer-contract-out", str(paths["token"]), "--out-dir", str(out_dir), "--allow-warnings"],
        [
            "cuda-candidate-batch-abi",
            "build-transform-parameter-contract",
            "--transform-parameter-contract-out",
            str(paths["transform"]),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        ["cuda-candidate-batch-abi", "build-key-schedule-contract", "--key-schedule-contract-out", str(paths["key"]), "--out-dir", str(out_dir), "--allow-warnings"],
        ["cuda-candidate-batch-abi", "build-stream-schedule-contract", "--stream-schedule-contract-out", str(paths["stream"]), "--out-dir", str(out_dir), "--allow-warnings"],
        ["cuda-candidate-batch-abi", "build-score-vector-contract", "--score-vector-contract-out", str(paths["score"]), "--out-dir", str(out_dir), "--allow-warnings"],
        ["cuda-candidate-batch-abi", "build-topk-output-contract", "--topk-output-contract-out", str(paths["topk"]), "--out-dir", str(out_dir), "--allow-warnings"],
        [
            "cuda-candidate-batch-abi",
            "build-backend-surface-contract",
            "--backend-surface-contract-out",
            str(paths["backend"]),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-candidate-batch-abi",
            "build-result-store-compatibility",
            "--result-store-compatibility-out",
            str(paths["compat"]),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-candidate-batch-abi",
            "build-gap-closure",
            "--stage5t-gaps",
            "data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml",
            "--gap-closure-out",
            str(paths["gap"]),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "cuda-candidate-batch-abi",
            "build-next-stage-decision",
            "--gap-closure",
            str(paths["gap"]),
            "--next-stage-decision-out",
            str(paths["decision"]),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    summary = runner.invoke(
        app,
        [
            "cuda-candidate-batch-abi",
            "build-summary",
            "--candidate-batch-abi",
            str(paths["abi"]),
            "--token-buffer-contract",
            str(paths["token"]),
            "--transform-parameter-contract",
            str(paths["transform"]),
            "--key-schedule-contract",
            str(paths["key"]),
            "--stream-schedule-contract",
            str(paths["stream"]),
            "--score-vector-contract",
            str(paths["score"]),
            "--topk-output-contract",
            str(paths["topk"]),
            "--backend-surface-contract",
            str(paths["backend"]),
            "--result-store-compatibility",
            str(paths["compat"]),
            "--gap-closure",
            str(paths["gap"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary-out",
            str(paths["summary"]),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert summary.exit_code == 0, summary.output

    validate = runner.invoke(
        app,
        [
            "cuda-candidate-batch-abi",
            "validate-stage5u",
            "--candidate-batch-abi",
            str(paths["abi"]),
            "--token-buffer-contract",
            str(paths["token"]),
            "--transform-parameter-contract",
            str(paths["transform"]),
            "--key-schedule-contract",
            str(paths["key"]),
            "--stream-schedule-contract",
            str(paths["stream"]),
            "--score-vector-contract",
            str(paths["score"]),
            "--topk-output-contract",
            str(paths["topk"]),
            "--backend-surface-contract",
            str(paths["backend"]),
            "--result-store-compatibility",
            str(paths["compat"]),
            "--gap-closure",
            str(paths["gap"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary",
            str(paths["summary"]),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "cuda_candidate_batch_abi_stage5u_valid=true" in validate.output


def test_stage5u_cli_keeps_stage5t_command_registered() -> None:
    result = CliRunner().invoke(app, ["cuda-solved-family-readiness", "summary", "--help"])
    assert result.exit_code == 0, result.output
