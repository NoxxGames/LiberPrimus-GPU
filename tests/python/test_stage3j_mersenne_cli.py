from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3j-bounded-cpu-queue.yaml"


def _synthetic_queue(tmp_path: Path) -> Path:
    queue = load_bounded_queue(QUEUE).payload
    payload = dict(queue)
    item = dict(payload["items"][0])
    corpus_slice = dict(item["corpus_slice"])
    selector = dict(corpus_slice["selector"])
    selector["index29_values"] = [0, 1, 2, 3, 4, 5]
    selector["token_records"] = [
        {"token_kind": "rune", "index29": 0, "token_index_global": 0, "line_index": 0},
        {"token_kind": "rune", "index29": 1, "token_index_global": 1, "line_index": 0},
        {"token_kind": "line_separator", "token_index_global": 2},
        {"token_kind": "rune", "index29": 2, "token_index_global": 3, "line_index": 1},
        {"token_kind": "rune", "index29": 3, "token_index_global": 4, "line_index": 1},
        {"token_kind": "rune", "index29": 4, "token_index_global": 5, "line_index": 1},
        {"token_kind": "rune", "index29": 5, "token_index_global": 6, "line_index": 1},
    ]
    corpus_slice["selector"] = selector
    item["corpus_slice"] = corpus_slice
    payload["items"] = [item]
    path = tmp_path / "queue.yaml"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_stage3j_cli_run_works_on_synthetic_input(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage3j"
    result = CliRunner().invoke(
        app,
        [
            "bounded-run",
            "run-mersenne-stream-probe",
            "--policy",
            str(POLICY),
            "--queue",
            str(_synthetic_queue(tmp_path)),
            "--item-id",
            "stage3j_mersenne_prime_stream_tiny_v1",
            "--out-dir",
            str(out_dir),
            "--top-k",
            "5",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "expected_candidate_count=192" in result.output
    assert "executed_candidate_count=192" in result.output
    assert "unique_stream_signature_count=" in result.output
    assert (out_dir / "summary.json").is_file()
