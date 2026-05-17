from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import yaml

from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_experiments.runner import run_all

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def _synthetic_queue(tmp_path: Path) -> Path:
    queue = load_bounded_queue(QUEUE).payload
    item = next(deepcopy(item) for item in queue["items"] if item["item_id"] == "stage3e_prime_minus_one_offsets_v1")
    item["corpus_slice"]["slice_id"] = "stage3g-run-all-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3g-run-all-synthetic",
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
    path = tmp_path / "queue.yaml"
    path.write_text(yaml.safe_dump(queue, sort_keys=False), encoding="utf-8")
    return path


def test_bounded_experiment_run_all_uses_stage3g_executor(tmp_path: Path) -> None:
    queue_path = _synthetic_queue(tmp_path)
    _checks, results, summary_path = run_all(POLICY, queue_path, tmp_path / "out", allow_warnings=True)

    assert len(results) == 1
    assert results[0].execution_performed is True
    assert results[0].summary["stage3g_run_id"]
    assert results[0].summary["prime_candidate_count"] == 256
    assert results[0].solve_claim_made is False
    assert json.loads(summary_path.read_text(encoding="utf-8"))["executed_count"] == 1


def test_policy_blocks_prime_offsets_expanded_without_count_update() -> None:
    policy = load_operator_policy(POLICY)
    queue = load_bounded_queue(QUEUE)
    item = next(deepcopy(item) for item in queue.items if item["item_id"] == "stage3e_prime_minus_one_offsets_v1")
    item["transform_plan"]["parameters"]["offsets"]["end"] = 64

    result = check_item(policy, item)

    assert "declared_exact_count_mismatch" in result.blocking_reasons
