from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"
TARGET_ID = "stage3e_vig_history_key_pack_v1"


def test_stage3i_historical_vigenere_key_pack_cli_run_and_summary(tmp_path: Path) -> None:
    queue = load_bounded_queue(QUEUE).payload
    item = next(deepcopy(candidate) for candidate in queue["items"] if candidate["item_id"] == TARGET_ID)
    item["corpus_slice"]["slice_id"] = "stage3i-cli-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3i-cli-synthetic",
        "index29_values": [20, 10, 17, 18],
        "token_records": [
            {"token_kind": "rune", "index29": 20, "token_index_global": 0, "logical_line_index": 1},
            {"token_kind": "word_separator", "token_index_global": 1, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 10, "token_index_global": 2, "logical_line_index": 1},
            {"token_kind": "physical_newline", "token_index_global": 3, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 17, "token_index_global": 4, "logical_line_index": 2},
            {"token_kind": "rune", "index29": 18, "token_index_global": 5, "logical_line_index": 2},
        ],
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
            "run-vigenere-key-pack",
            "--policy",
            str(POLICY),
            "--queue",
            str(queue_path),
            "--item-id",
            TARGET_ID,
            "--out-dir",
            str(out_dir),
            "--top-k",
            "5",
            "--allow-warnings",
        ],
    )
    summary = runner.invoke(app, ["bounded-run", "summary", "--results-dir", str(out_dir)])

    assert run.exit_code == 0, run.output
    assert "expected_candidate_count=56" in run.output
    assert "executed_candidate_count=56" in run.output
    assert "deferred_candidate_count=0" in run.output
    assert "vigenere_candidate_count=56" in run.output
    assert "solve_claim=false" in run.output
    assert summary.exit_code == 0, summary.output
    assert "top_candidate_key_text=" in summary.output
    assert "top_candidate_reset_mode=" in summary.output
    assert "top_candidate_advance_mode=" in summary.output

