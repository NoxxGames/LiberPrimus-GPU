import sqlite3
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.result_store.jsonl_sink import read_jsonl
from libreprimus.result_store.summary import load_summary


REQUIRED_PATHS = [
    Path("data/transform-registry/cpu-reference-transforms-v0.json"),
    Path("experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml"),
    Path("experiments/manifests/result-store/stage2b-solved-baseline-import.yaml"),
]


def _have_real_inputs() -> bool:
    return all(path.exists() for path in REQUIRED_PATHS)


@pytest.mark.skipif(not _have_real_inputs(), reason="Stage 2B real-source inputs are not present.")
def test_stage2b_real_smoke_imports_stage2a_result(tmp_path: Path) -> None:
    solved_out = tmp_path / "solved-baseline"
    result_out = tmp_path / "result-store"
    result = CliRunner().invoke(
        app,
        [
            "result-store",
            "stage2b-smoke",
            "--solved-baseline-manifest",
            "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml",
            "--result-store-manifest",
            "experiments/manifests/result-store/stage2b-solved-baseline-import.yaml",
            "--solved-baseline-out-dir",
            str(solved_out),
            "--result-store-out-dir",
            str(result_out),
            "--replace",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    solved_summary = load_summary(solved_out)
    result_summary = load_summary(result_out)
    assert solved_summary["pass_count"] == 10
    assert (result_out / "run_records.jsonl").is_file()
    assert (result_out / "results.sqlite3").is_file()
    assert result_summary["search_performed_any"] is False
    assert result_summary["cuda_used_any"] is False
    assert result_summary["scoring_used_any"] is False
    assert result_summary["canonical_corpus_active_any"] is False
    runs = read_jsonl(result_out / "run_records.jsonl")
    assert len(runs) >= 1
    assert runs[0]["fixture_counts"]["pass"] == 10
    with sqlite3.connect(result_out / "results.sqlite3") as connection:
        assert connection.execute("SELECT COUNT(*) FROM runs").fetchone()[0] >= 1


@pytest.mark.skipif(not _have_real_inputs(), reason="Stage 2B real-source inputs are not present.")
def test_stage2b_generated_outputs_are_not_staged() -> None:
    status = subprocess.run(["git", "status", "--short"], check=True, capture_output=True, text=True)

    assert "experiments/results/result-store/stage2b/run_records.jsonl" not in status.stdout
    assert "experiments/results/result-store/stage2b/results.sqlite3" not in status.stdout
