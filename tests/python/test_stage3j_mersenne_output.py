from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.mersenne_stream_probe import run_mersenne_stream_probe_item

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3j-bounded-cpu-queue.yaml"


def _synthetic_item() -> dict:
    item = dict(load_bounded_queue(QUEUE).items[0])
    corpus_slice = dict(item["corpus_slice"])
    selector = dict(corpus_slice["selector"])
    selector["index29_values"] = [0, 1, 2, 3]
    selector["token_records"] = [
        {"token_kind": "rune", "index29": 0, "token_index_global": 0, "line_index": 0},
        {"token_kind": "rune", "index29": 1, "token_index_global": 1, "line_index": 0},
        {"token_kind": "rune", "index29": 2, "token_index_global": 2, "line_index": 1},
        {"token_kind": "rune", "index29": 3, "token_index_global": 3, "line_index": 1},
    ]
    corpus_slice["selector"] = selector
    item["corpus_slice"] = corpus_slice
    return item


def test_stage3j_candidate_records_include_required_fields(tmp_path: Path) -> None:
    run_mersenne_stream_probe_item(_synthetic_item(), out_dir=tmp_path, top_k=5)
    first_record = json.loads((tmp_path / "candidate_records.jsonl").read_text(encoding="utf-8").splitlines()[0])

    assert first_record["stream_variant"] in {"mersenne_mod29", "mersenne_minus_one_mod29", "perfect_number_mod29"}
    assert first_record["offset"] == 0
    assert first_record["direction"] == "forward"
    assert first_record["reset_mode"] == "none"
    assert len(first_record["stream_signature_sha256"]) == 64
    assert first_record["cuda_used"] is False
    assert first_record["solve_claim"] is False
    assert first_record["calibrated_confidence_label"]


def test_stage3j_generated_outputs_are_ignored() -> None:
    for path in [
        "experiments/results/bounded-auto-runs/stage3j/candidate_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3j/top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3j/summary.json",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False)
        assert result.returncode == 0
