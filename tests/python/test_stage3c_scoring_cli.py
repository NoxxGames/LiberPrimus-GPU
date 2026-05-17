from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


runner = CliRunner()


def _write_candidate_outputs(stage3a: Path, stage3b: Path) -> None:
    stage3a.mkdir(parents=True)
    (stage3b / "reverse_direction").mkdir(parents=True)
    row = '{"output_normalized_text":"QXQXQXQXQXQX","transform_family":"affine_mod29","transform_parameters":{"a":1,"b":2}}\n'
    (stage3a / "top_candidates.jsonl").write_text(row, encoding="utf-8")
    (stage3b / "reranked_top_candidates.jsonl").write_text(row, encoding="utf-8")
    (stage3b / "reverse_direction" / "top_candidates.jsonl").write_text(row, encoding="utf-8")


def test_scoring_cli_crib_check() -> None:
    result = runner.invoke(app, ["scoring", "crib-check", "--text", "LIBER PRIMUS"])

    assert result.exit_code == 0
    assert "crib_hit_count=2" in result.output
    assert "solve_claim=false" in result.output


def test_scoring_cli_calibrate_and_summary(tmp_path: Path) -> None:
    stage3a = tmp_path / "stage3a"
    stage3b = tmp_path / "stage3b"
    out_dir = tmp_path / "out"
    _write_candidate_outputs(stage3a, stage3b)

    result = runner.invoke(
        app,
        [
            "scoring",
            "calibrate",
            "--stage3-results-dir",
            str(stage3a),
            "--stage3b-results-dir",
            str(stage3b),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    summary = runner.invoke(app, ["scoring", "calibration-summary", "--results-dir", str(out_dir)])

    assert result.exit_code == 0
    assert summary.exit_code == 0
    assert "positive_control_count=" in summary.output
    assert "solve_claim=false" in summary.output
