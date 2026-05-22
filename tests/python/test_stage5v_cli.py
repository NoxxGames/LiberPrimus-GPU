from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5v_cli_round_trip_no_gpu(tmp_path: Path) -> None:
    runner = CliRunner()
    out_dir = tmp_path / "stage5v"
    paths = {
        "adapter": tmp_path / "adapter.yaml",
        "fixtures": tmp_path / "fixtures.yaml",
        "token": tmp_path / "token.yaml",
        "schedule": tmp_path / "schedule.yaml",
        "score": tmp_path / "score.yaml",
        "topk": tmp_path / "topk.yaml",
        "result": tmp_path / "result.yaml",
        "status": tmp_path / "status.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    commands = [
        ["build-adapter-records", "--adapter-records-out", str(paths["adapter"])],
        ["build-conformance-fixtures", "--conformance-fixtures-out", str(paths["fixtures"])],
        ["run-native-conformance", "--conformance-fixtures", str(paths["fixtures"])],
        [
            "build-token-buffer-conformance",
            "--conformance-fixtures",
            str(paths["fixtures"]),
            "--token-buffer-conformance-out",
            str(paths["token"]),
        ],
        ["build-schedule-conformance", "--schedule-conformance-out", str(paths["schedule"])],
        ["build-score-vector-conformance", "--score-vector-conformance-out", str(paths["score"])],
        ["build-topk-conformance", "--topk-conformance-out", str(paths["topk"])],
        ["build-result-store-conformance", "--result-store-conformance-out", str(paths["result"])],
        ["build-implementation-status", "--implementation-status-out", str(paths["status"])],
        ["build-next-stage-decision", "--next-stage-decision-out", str(paths["decision"])],
    ]
    for command in commands:
        result = runner.invoke(
            app,
            ["native-candidate-batch-conformance", *command, "--out-dir", str(out_dir), "--allow-warnings"],
        )
        assert result.exit_code == 0, result.output

    summary = runner.invoke(
        app,
        [
            "native-candidate-batch-conformance",
            "build-summary",
            "--adapter-records",
            str(paths["adapter"]),
            "--conformance-fixtures",
            str(paths["fixtures"]),
            "--token-buffer-conformance",
            str(paths["token"]),
            "--schedule-conformance",
            str(paths["schedule"]),
            "--score-vector-conformance",
            str(paths["score"]),
            "--topk-conformance",
            str(paths["topk"]),
            "--result-store-conformance",
            str(paths["result"]),
            "--implementation-status",
            str(paths["status"]),
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
            "native-candidate-batch-conformance",
            "validate-stage5v",
            "--adapter-records",
            str(paths["adapter"]),
            "--conformance-fixtures",
            str(paths["fixtures"]),
            "--token-buffer-conformance",
            str(paths["token"]),
            "--schedule-conformance",
            str(paths["schedule"]),
            "--score-vector-conformance",
            str(paths["score"]),
            "--topk-conformance",
            str(paths["topk"]),
            "--result-store-conformance",
            str(paths["result"]),
            "--implementation-status",
            str(paths["status"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary",
            str(paths["summary"]),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "native_candidate_batch_conformance_stage5v_valid=true" in validate.output


def test_stage5v_cli_keeps_stage5u_group_registered() -> None:
    result = CliRunner().invoke(app, ["cuda-candidate-batch-abi", "summary", "--help"])
    assert result.exit_code == 0, result.output
