from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.prime_offset_sweep import run_prime_offset_sweep_item

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def _synthetic_item() -> dict:
    queue = load_bounded_queue(QUEUE)
    item = next(deepcopy(item) for item in queue.items if item["item_id"] == "stage3e_prime_minus_one_offsets_v1")
    item["corpus_slice"]["slice_id"] = "stage3g-output-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3g-output-synthetic",
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
    return item


def test_stage3g_candidate_output_records_include_prime_params(tmp_path: Path) -> None:
    summary = run_prime_offset_sweep_item(_synthetic_item(), out_dir=tmp_path, top_k=5)
    records = [
        json.loads(line)
        for line in Path(summary.output_paths["candidate_records"]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert len(records) == 256
    first = records[0]
    assert first["transform_family"] == "prime_stream_offset_sweep"
    assert first["transform_id"] == "prime_minus_one_stream"
    assert first["transform_parameters"]["offset"] == 0
    assert first["transform_parameters"]["direction"] in {"forward", "reverse"}
    assert first["transform_parameters"]["reset_mode"] in {"none", "line"}
    assert first["cuda_used"] is False
    assert first["solve_claim"] is False
    assert first["calibrated_confidence_label"]
    assert first["score_summary"]["no_solve_claim"] is True


def test_stage3g_run_summary_records_expected_executed_and_deferred_counts(tmp_path: Path) -> None:
    summary = run_prime_offset_sweep_item(_synthetic_item(), out_dir=tmp_path, top_k=5)
    payload = json.loads(Path(summary.output_paths["summary"]).read_text(encoding="utf-8"))

    assert payload["expected_candidate_count"] == 256
    assert payload["executed_candidate_count"] == 256
    assert payload["deferred_candidate_count"] == 0
    assert payload["prime_candidate_count"] == 256
    assert payload["confidence_distribution"]
    assert payload["cuda_used"] is False
    assert payload["solve_claim"] is False


def test_stage3g_generated_outputs_are_ignored() -> None:
    path = "experiments/results/bounded-auto-runs/stage3g/candidate_records.jsonl"
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=REPO, check=False)

    assert result.returncode == 0
