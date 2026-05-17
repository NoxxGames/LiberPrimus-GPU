from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3c-bounded-cpu-queue.yaml"


def test_stage3d_vigenere_cli_run_and_summary(tmp_path: Path) -> None:
    queue = load_bounded_queue(QUEUE).payload
    item = deepcopy(queue["items"][0])
    item["corpus_slice"]["slice_id"] = "stage3d-cli-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3d-cli-synthetic",
        "index29_values": [20, 10, 17, 18, 4, 13],
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    queue["items"] = [item]
    queue_path = tmp_path / "queue.yaml"
    queue_path.write_text(yaml.safe_dump(queue, sort_keys=False), encoding="utf-8")
    out_dir = tmp_path / "out"
    runner = CliRunner()

    run = runner.invoke(
        app,
        [
            "bounded-run",
            "run-vigenere-key-list",
            "--policy",
            str(POLICY),
            "--queue",
            str(queue_path),
            "--item-id",
            "stage3c-small-vigenere-known-motif-key-list",
            "--out-dir",
            str(out_dir),
            "--top-k",
            "4",
            "--allow-warnings",
        ],
    )
    summary = runner.invoke(app, ["bounded-run", "summary", "--results-dir", str(out_dir)])

    assert run.exit_code == 0, run.output
    assert "candidate_count=4" in run.output
    assert "vigenere_candidate_count=4" in run.output
    assert "solve_claim=false" in run.output
    assert summary.exit_code == 0, summary.output
    assert "top_candidate_key_text=" in summary.output
