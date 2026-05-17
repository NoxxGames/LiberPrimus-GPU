from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def test_stage3e_dry_run_cli_writes_summary(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage3e"
    result = CliRunner().invoke(
        app,
        [
            "bounded-experiment",
            "dry-run-queue",
            "--policy",
            str(POLICY),
            "--queue",
            str(QUEUE),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "item_count=7" in result.output
    assert "total_candidate_estimate=972" in result.output
    assert "runnable_now_count=4" in result.output
    assert "needs_executor_count=2" in result.output
    assert "dry_run_only_count=1" in result.output
    payload = json.loads((out_dir / "stage3e_queue_dry_run_summary.json").read_text(encoding="utf-8"))
    assert payload["record_type"] == "stage3e_queue_dry_run_summary"
    assert payload["executed_count"] == 0
    assert payload["solve_claim"] is False
    assert payload["cuda_used"] is False


def test_stage3e_generated_dry_run_outputs_are_ignored() -> None:
    path = "experiments/results/bounded-auto-runs/stage3e/stage3e_queue_dry_run_summary.json"
    result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False)

    assert result.returncode == 0
